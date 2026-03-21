from snowflake.ml.registry import Registry


def get_best_model_version(
    mr: Registry,
    model_name: str,
    metric: str = "mean_absolute_percentage_error",
    mode: str = "min",
):
    model = mr.get_model(model_name)
    versions = model.versions()
    if not versions:
        return None, None

    best_version = None
    best_score = float("inf") if mode == "min" else float("-inf")
    compare = (lambda a, b: a < b) if mode == "min" else (lambda a, b: a > b)

    for v in versions:
        all_metrics = v.show_metrics()
        if not all_metrics or metric not in all_metrics:
            continue
        score = all_metrics[metric]
        if compare(score, best_score):
            best_score = score
            best_version = v

    if best_version is None:
        print(f"No versions have metric '{metric}'. Falling back to latest version.")
        best_version = versions[-1]
        best_score = None

    return best_version, best_score


def promote_model(mr: Registry, model_name: str, version_name: str = None, alias: str = "champion"):
    model = mr.get_model(model_name)
    if version_name is None:
        best_version, best_score = get_best_model_version(mr, model_name)
        if best_version is None:
            raise ValueError(f"No versions found for model {model_name}")
        version_name = best_version.version_name
        if best_score is not None:
            print(f"Best version: {version_name} (score={best_score:.4f})")
        else:
            print(f"Best version: {version_name} (no metrics available)")

    mv = model.version(version_name)
    mv.set_alias(alias)
    print(f"Alias '{alias}' set on {model_name}/{version_name}")

    mv.set_tag("stage", "production")
    mv.set_tag("promoted_by", "ml_framework")
    print(f"Tags set on {model_name}/{version_name}")
    return mv


def set_default_version(mr: Registry, model_name: str, version_name: str):
    model = mr.get_model(model_name)
    model.default = version_name
    print(f"Default version set to {version_name} for {model_name}")
