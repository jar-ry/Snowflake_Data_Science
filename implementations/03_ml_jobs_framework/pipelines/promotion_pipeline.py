from snowflake.ml.registry import Registry

from src.ml_engineering.promotion import get_best_model_version, promote_model, set_default_version


def run(session, conf: dict):
    print("=" * 60)
    print("PROMOTION PIPELINE")
    print("=" * 60)

    database = conf["snowflake"]["database"]
    mr_schema = conf["model_registry"]["schema"]
    model_name = conf["modelling"]["model_name"]

    mr = Registry(session=session, database_name=database, schema_name=mr_schema)

    print(f"\n[1/3] Finding best version for {model_name}...")
    metric = conf["modelling"].get("tuning_metric", "mean_absolute_percentage_error")
    mode = conf["modelling"].get("tuning_mode", "min")
    best_version, best_score = get_best_model_version(mr, model_name, metric=metric, mode=mode)
    if best_version is None:
        print("No model versions found. Skipping promotion.")
        return None

    version_name = best_version.version_name
    if best_score is not None:
        print(f"  Best: {version_name} ({metric}={best_score:.4f})")
    else:
        print(f"  Best: {version_name} (no metrics, using latest)")

    print("[2/3] Promoting model...")
    mv = promote_model(mr, model_name, version_name=version_name, alias="champion")

    print("[3/3] Setting default version...")
    set_default_version(mr, model_name, version_name)

    print(f"\nPromotion complete: {model_name}/{version_name}")
    return mv
