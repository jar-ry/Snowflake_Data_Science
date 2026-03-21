from snowflake.ml.jobs import submit_directory


def run(session, conf: dict):
    print("=" * 60)
    print("TRAINING PIPELINE (submit_directory)")
    print("=" * 60)

    compute = conf["compute"]
    modelling = conf["modelling"]
    mr_schema = conf["model_registry"]["schema"]
    fs_schema = conf["feature_store"]["schema"]
    dataset_fqn = f"{conf['snowflake']['database']}.{fs_schema}.{conf['feature_store']['dataset_name']}"

    args = [
        "--dataset",
        dataset_fqn,
        "--model-name",
        modelling["model_name"],
        "--mr-schema",
        mr_schema,
        "--experiment-name",
        modelling["experiment_name"],
        "--num-trials",
        str(compute["num_trials"]),
        "--tuning-metric",
        modelling.get("tuning_metric", "mean_absolute_percentage_error"),
        "--tuning-mode",
        modelling.get("tuning_mode", "min"),
    ]

    print(f"Submitting ML Job to pool '{compute['pool_name']}'")
    print("  Entrypoint : modelling/train.py")
    print(f"  Dataset    : {dataset_fqn}")
    print(f"  Trials     : {compute['num_trials']}")

    job = submit_directory(
        "./src/",
        compute["pool_name"],
        entrypoint="modelling/train.py",
        args=args,
        stage_name=compute["stage_name"],
        session=session,
        target_instances=compute.get("target_instances", 1),
    )

    print(f"Job submitted: {job.id}")
    print("Waiting for job completion...")
    job.wait()
    status = job.status
    print(f"Job status: {status}")
    if status != "DONE":
        logs = job.get_logs()
        print(f"\n--- JOB LOGS ---\n{logs}\n--- END LOGS ---")
        raise RuntimeError(f"Training job failed with status: {status}")
    return job
