from snowflake.ml.registry import Registry

from src.ml_engineering.monitoring import setup_monitor
from src.ml_engineering.promotion import get_best_model_version


def run(session, conf: dict):
    print("=" * 60)
    print("MONITORING PIPELINE")
    print("=" * 60)

    database = conf["snowflake"]["database"]
    mr_schema = conf["model_registry"]["schema"]
    model_name = conf["modelling"]["model_name"]

    mr = Registry(session=session, database_name=database, schema_name=mr_schema)

    best_version, _ = get_best_model_version(mr, model_name)
    if best_version is None:
        print("No model versions found. Skipping monitoring setup.")
        return None

    version_name = best_version.version_name
    print(f"Setting up monitor for {model_name}/{version_name}")

    monitor = setup_monitor(session, mr, model_name, version_name, conf)
    print("\nMonitoring pipeline complete.")
    return monitor
