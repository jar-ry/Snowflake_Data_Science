import os
from snowflake.snowpark import Session, DataFrame, Window, WindowSpec
from os import listdir
from os.path import isfile, join
import json
import numpy as np
from snowflake.snowpark.version import VERSION
import snowflake.snowpark.functions as F
from snowflake.ml.dataset import Dataset
from snowflake.ml._internal.exceptions import (
    dataset_errors
)


def run_sql(sql_statement, session):
    """
    Create a function to simplify the execution of SQL text strings via Snowpark.
    sql_statement : SQL statement as text string
    session : Snowpark session.  If none, defaults session is assumed to be set in calling environmentß
    """
    result = session.sql(sql_statement).collect()
    print(sql_statement, '\n', result, '\n')
    return {sql_statement : result} 
    #result = session.sql(sql_statement).queries['queries'][0]
    #print(result)

import ast
def check_and_update(df, model_name):
    """
    Check and update the version numbering scheme for Model Registry 
    to get the next version number for a model.
    df         : dataframe from show_models
    model_name : model-name to acquire next version for
    """
    if "." in model_name:
        model_name = model_name.split(".")[-1]
    if df.empty:
        return "V_1"
    elif df[df["name"] == model_name].empty:
        return "V_1"
    else:
        # Increment model_version if df is not a pandas Series
        # The result is a Series where each element is a list (e.g., [ "V_1", "V_2" ])
        list_of_lists = df["versions"].apply(ast.literal_eval)

        # Step 2: Flatten the list of lists into a single list
        all_versions = [version for sublist in list_of_lists for version in sublist]

        # Step 3: Sort the resulting single list
        lst = sorted(all_versions)
        last_value = lst[-1]
        prefix, num = last_value.rsplit("_", 1)
        new_last_value = f"{prefix}_{int(num)+1}"
        lst[-1] = new_last_value
        return new_last_value 
    
def dataset_check_and_update(session, dataset_name):
    """
    Check and update the version numbering scheme for Dataset
    to get the next version number for a dataset.
    session         : current session
    dataset_name : dataset_name to acquire next version for
    """
    full_name = session.get_current_database() + "." + session.get_current_schema() + "." + dataset_name
    try:
        ds = Dataset.load(session=session, name=full_name)
        versions = ds.list_versions()
    except dataset_errors.DatasetNotExistError:
        return "V_1"

    if len(versions) == 0:
        return "V_1"
    else:
        # Step 3: Sort the resulting single list
        lst = sorted(versions)
        last_value = lst[-1]
        prefix, num = last_value.rsplit("_", 1)
        print(lst, last_value)
        new_last_value = f"{prefix}_{int(num)+1}"
        lst[-1] = new_last_value
        return new_last_value 

def get_latest(df, model_name):
    """
    Check and update the version numbering scheme for Model Registry 
    to get the next version number for a model.
    df         : dataframe from show_models
    model_name : model-name to acquire next version for
    """
    if df.empty:
        return "V_1"
    elif df[df["name"] == model_name].empty:
        return "V_1"
    else:
        # Increment model_version if df is not a pandas Series
        lst = sorted(ast.literal_eval(df["versions"][0]))
        last_value = lst[-1]
        prefix, num = last_value.rsplit("_", 1)
        new_last_value = f"{prefix}_{int(num)}"
        return new_last_value 

import sqlglot
import sqlglot.optimizer.optimizer
def formatSQL (query_in:str, subq_to_cte = False):
    """
    Prettify the given raw SQL statement to nest/indent appropriately.
    Optionally replace subqueries with CTEs.
    query_in    : The raw SQL query to be prettified
    subq_to_cte : When TRUE convert nested sub-queries to CTEs
    """
    expression = sqlglot.parse_one(query_in)
    if subq_to_cte:
        query_in = sqlglot.optimizer.optimizer.eliminate_subqueries(expression).sql()
    return sqlglot.transpile(query_in, read='snowflake', pretty=True)[0]

from snowflake.ml.registry import Registry
from snowflake.ml._internal.utils import identifier  
def create_ModelRegistry(session, database, mr_schema = 'MODEL_1'):
    """
    Create Snowflake Model Registry if not exists and return as reference.
    session   : Snowpark session
    database  : Database to use for Model Registry
    mr_schema : Schema name to create/use for Model Registry
    """

    try:
        cs = session.get_current_schema()
        session.sql(f''' create schema {mr_schema} ''').collect()
        mr = Registry(session=session, database_name= database, schema_name=mr_schema)
        session.sql(f''' use schema {cs}''').collect()
    except:
        print(f"Model Registry ({mr_schema}) already exists")   
        mr = Registry(session=session, database_name= database, schema_name=mr_schema)
    else:
        print(f"Model Registry ({mr_schema}) created")

    return mr   

from snowflake.ml.feature_store import (FeatureStore,CreationMode) 
def create_FeatureStore(session, database, fs_schema, warehouse):
    """
    Create Snowflake Feature Store if not exists and return reference
    session   : Snowpark session
    database  : Database to use for Feature Store
    fs_schema : Schema name to ceate/use to check for Feature Store
    warehouse : Warehouse to use as default for Feature Store
    """

    try:
        fs = FeatureStore(session, database, fs_schema, warehouse, creation_mode=CreationMode.FAIL_IF_NOT_EXIST)
        print(f"Feature Store ({fs_schema}) already exists") 
    except:
        print(f"Feature Store ({fs_schema}) created")   
        fs = FeatureStore(session, database, fs_schema, warehouse, creation_mode=CreationMode.CREATE_IF_NOT_EXIST)

    return fs

def create_SF_Session(schema, role = 'FS_QS_ROLE'):
    # Scale Factor
    scale_factor               = 'SF0001'

    # Database
    tpcxai_database_base       = f'TPCXAI_{scale_factor}_QUICKSTART'
    tpcxai_database            = f'{tpcxai_database_base}_INC'

    # Create Snowflake Session object
    with open('connection.json', 'r') as f:
        connection_parameters = json.load(f)
    
    session = Session.builder.configs(connection_parameters).create()
    session.sql_simplifier_enabled = True
    snowflake_environment = session.sql('SELECT current_user(), current_version()').collect()
    snowpark_version = VERSION

    # Set  Environment
    session.sql(f'''use database {tpcxai_database}''').collect()
    session.sql(f'''use schema {schema}''').collect()
    session.sql(f'''use role {role}''').collect()

    # Create a Warehouse
    #warehouse_env = f"""{tpcxai_database}_{schema}"""
    warehouse_sz = 'MEDIUM'
    warehouse_env = f'TPCXAI_{scale_factor}_QUICKSTART_WH'
    session.sql(f'''use warehouse {warehouse_env}''').collect()
    session.sql(f'''alter warehouse {warehouse_env} set warehouse_size = {warehouse_sz}''').collect()

    # Current Environment Details
    print('\nConnection Established with the following parameters:')
    print(f'User                        : {snowflake_environment[0][0]}')
    print(f'Role                        : {session.get_current_role()}')
    print(f'Database                    : {session.get_current_database()}')
    print(f'Schema                      : {session.get_current_schema()}')
    print(f'Warehouse                   : {session.get_current_warehouse()}')
    print(f'Snowflake version           : {snowflake_environment[0][1]}')
    print(f'Snowpark for Python version : {snowpark_version[0]}.{snowpark_version[1]}.{snowpark_version[2]} \n')

    return role, tpcxai_database, schema, session, warehouse_env

def get_spine_df(dataframe):
    spine_sdf =  dataframe.feature_df.group_by('O_CUSTOMER_SK').agg( F.max('LATEST_ORDER_DATE').as_('ASOF_DATE'))#.limit(10)
    spine_sdf = spine_sdf.with_column("col_1", F.lit("values1"))
    return spine_sdf