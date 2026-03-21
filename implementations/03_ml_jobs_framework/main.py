import argparse
import sys

import yaml

from pipelines import feature_pipeline, monitoring_pipeline, promotion_pipeline, training_pipeline

PIPELINES = {
    "feature": feature_pipeline,
    "training": training_pipeline,
    "promotion": promotion_pipeline,
    "monitoring": monitoring_pipeline,
}


def load_config(config_path: str = "conf/parameters.yml") -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def run_all(conf: dict):
    session, mr, fs, fv = feature_pipeline.run(conf)
    training_pipeline.run(session, conf)
    promotion_pipeline.run(session, conf)
    monitoring_pipeline.run(session, conf)
    print("\n" + "=" * 60)
    print("ALL PIPELINES COMPLETE")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="CLV Model Pipeline Runner",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "pipeline",
        nargs="?",
        default="all",
        choices=["all", *PIPELINES.keys()],
        help="Pipeline to run (default: all)\n"
        "  all        - Run full end-to-end pipeline\n"
        "  feature    - Feature engineering & Feature Store\n"
        "  training   - Submit HPO training ML Job\n"
        "  promotion  - Promote best model version\n"
        "  monitoring - Set up model monitoring",
    )
    parser.add_argument(
        "--config",
        "-c",
        default="conf/parameters.yml",
        help="Path to parameters YAML (default: conf/parameters.yml)",
    )
    args = parser.parse_args()

    conf = load_config(args.config)
    print(f"Config loaded from: {args.config}")
    print(f"Database: {conf['snowflake']['database']}")
    print(f"Pipeline: {args.pipeline}\n")

    if args.pipeline == "all":
        run_all(conf)
    elif args.pipeline == "feature":
        feature_pipeline.run(conf)
    elif args.pipeline in ("training", "promotion", "monitoring"):
        from src.session import create_session

        session, *_ = create_session(conf)
        PIPELINES[args.pipeline].run(session, conf)
    else:
        print(f"Unknown pipeline: {args.pipeline}")
        sys.exit(1)


if __name__ == "__main__":
    main()
