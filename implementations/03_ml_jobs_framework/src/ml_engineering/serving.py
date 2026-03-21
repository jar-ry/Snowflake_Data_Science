from snowflake.ml.registry import Registry


def deploy_inference_service(
    mr: Registry,
    model_name: str,
    version_name: str,
    pool_name: str,
    service_name: str,
    ingress_enabled: bool = True,
):
    model = mr.get_model(model_name)
    mv = model.version(version_name)
    mv.create_service(
        service_name=service_name,
        service_compute_pool=pool_name,
        ingress_enabled=ingress_enabled,
    )
    print(f"Service '{service_name}' deployed for {model_name}/{version_name}")
    return service_name


def run_batch_predictions(session, mr: Registry, model_name: str, input_table: str, output_table: str):
    model = mr.get_model(model_name)
    mv = model.default
    input_df = session.table(input_table)
    predictions = mv.run(input_df, function_name="predict")
    predictions.write.mode("overwrite").save_as_table(output_table)
    print(f"Predictions saved to {output_table}")
    return predictions
