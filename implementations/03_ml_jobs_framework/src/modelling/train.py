"""
ML Job entrypoint for HPO training via submit_directory.

Usage (submitted by pipelines/training_pipeline.py):
    submit_directory("./src/", pool, entrypoint="modelling/train.py", args=[...])

When running inside the Snowflake Container Runtime, the submitted directory
root is added to sys.path automatically, so sibling package imports work.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from snowflake.ml.data.data_connector import DataConnector
from snowflake.ml.experiment import ExperimentTracking
from snowflake.ml.experiment.callback.xgboost import SnowflakeXgboostCallback
from snowflake.ml.model.model_signature import infer_signature
from snowflake.snowpark import Session

from modelling.evaluate import evaluate_model
from modelling.pipeline import build_pipeline
from modelling.splitter import create_data_connector, generate_train_val_set

FEATURE_COLUMNS = [
    "AGE",
    "GENDER",
    "LOYALTY_TIER",
    "TENURE_MONTHS",
    "AVG_ORDER_VALUE",
    "PURCHASE_FREQUENCY",
    "RETURN_RATE",
    "TOTAL_ORDERS",
    "ANNUAL_INCOME",
    "AVERAGE_ORDER_PER_MONTH",
    "DAYS_SINCE_LAST_PURCHASE",
    "DAYS_SINCE_SIGNUP",
    "EXPECTED_DAYS_BETWEEN_PURCHASES",
    "DAYS_SINCE_EXPECTED_LAST_PURCHASE_DATE",
]
NUMERICAL_COLUMNS = [
    "AGE",
    "TENURE_MONTHS",
    "AVG_ORDER_VALUE",
    "PURCHASE_FREQUENCY",
    "RETURN_RATE",
    "TOTAL_ORDERS",
    "ANNUAL_INCOME",
    "AVERAGE_ORDER_PER_MONTH",
    "DAYS_SINCE_LAST_PURCHASE",
    "DAYS_SINCE_SIGNUP",
    "EXPECTED_DAYS_BETWEEN_PURCHASES",
    "DAYS_SINCE_EXPECTED_LAST_PURCHASE_DATE",
]
CATEGORICAL_COLUMNS = ["GENDER"]
ORDINAL_COLUMNS = ["LOYALTY_TIER"]
ORDINAL_CATEGORIES = {"LOYALTY_TIER": ["low", "medium", "high"]}
TARGET_COLUMN = "LIFETIME_VALUE"


def train():
    from snowflake.ml.modeling import tune

    session = Session.builder.getOrCreate()
    tuner_context = tune.get_tuner_context()
    params = tuner_context.get_hyper_params()
    dm = tuner_context.get_dataset_map()
    model_name = params.pop("model_name")
    mr_schema_name = params.pop("mr_schema_name")
    experiment_name = params.pop("experiment_name")

    exp = ExperimentTracking(session=session, schema_name=mr_schema_name)
    exp.set_experiment(experiment_name)

    with exp.start_run() as run:
        train_data = dm["train"].to_pandas()
        val_data = dm["val"].to_pandas()

        X_train = train_data.drop(TARGET_COLUMN, axis=1)
        y_train = train_data[TARGET_COLUMN]
        X_val = val_data.drop(TARGET_COLUMN, axis=1)
        y_val = val_data[TARGET_COLUMN]

        sig = infer_signature(X_train, y_train)
        callback = SnowflakeXgboostCallback(
            exp,
            model_name=model_name,
            model_signature=sig,
        )
        params["callbacks"] = [callback]

        model = build_pipeline(
            model_params=params,
            numerical_columns=NUMERICAL_COLUMNS,
            categorical_columns=CATEGORICAL_COLUMNS,
            ordinal_columns=ORDINAL_COLUMNS,
            ordinal_categories=ORDINAL_CATEGORIES,
        )
        exp.log_params(params)

        print("Training model...", end="")
        model.fit(X_train, y_train)

        print("Evaluating model...", end="")
        metrics = evaluate_model(model, X_val, y_val)

        print("Log metrics...", end="")
        exp.log_metrics(metrics)
        metrics["run_name"] = run.name

        exp.log_model(
            model=model,
            model_name=model_name,
            version_name=run.name,
            sample_input_data=X_train,
        )

        tuner_context.report(metrics=metrics, model="model")


if __name__ == "__main__":
    from snowflake.ml.modeling import tune
    from snowflake.ml.modeling.tune.search import RandomSearch

    parser = argparse.ArgumentParser(description="HPO Training Job")
    parser.add_argument("--dataset", required=True, help="Fully qualified dataset name")
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--mr-schema", required=True)
    parser.add_argument("--experiment-name", required=True)
    parser.add_argument("--num-trials", type=int, default=10)
    parser.add_argument("--tuning-metric", default="mean_absolute_percentage_error")
    parser.add_argument("--tuning-mode", default="min")
    args = parser.parse_args()

    session = Session.builder.getOrCreate()

    print("Loading data...", end="", flush=True)
    dc = create_data_connector(session, dataset_name=args.dataset)
    df = dc.to_pandas()

    print("Building train/val data")
    train_df, val_df = generate_train_val_set(
        df,
        feature_columns=FEATURE_COLUMNS,
        target_column=TARGET_COLUMN,
    )

    dataset_map = {
        "train": DataConnector.from_dataframe(session.create_dataframe(train_df)),
        "val": DataConnector.from_dataframe(session.create_dataframe(val_df)),
    }

    search_space = {
        "mr_schema_name": args.mr_schema,
        "model_name": args.model_name,
        "experiment_name": args.experiment_name,
        "max_depth": tune.choice([1, 4, 6, 10]),
        "eta": tune.choice([0.01, 0.1, 0.8]),
        "n_estimators": tune.choice([10, 150, 500]),
        "subsample": tune.choice([0.5, 0.7, 1.0]),
        "reg_lambda": tune.choice([0.1, 1, 10]),
        "random_state": tune.choice([42]),
    }

    tuner_config = tune.TunerConfig(
        metric=args.tuning_metric,
        mode=args.tuning_mode,
        search_alg=RandomSearch(),
        num_trials=args.num_trials,
    )

    tuner = tune.Tuner(
        train_func=train,
        search_space=search_space,
        tuner_config=tuner_config,
    )

    print("HPO starting")
    results = tuner.run(dataset_map=dataset_map)
    print("HPO DONE")
    print(results.results)
