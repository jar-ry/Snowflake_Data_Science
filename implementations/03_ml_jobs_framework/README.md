# 03 — ML Jobs Framework

A Kedro/Cookiecutter-inspired boilerplate for building production ML pipelines on Snowflake, using **ML Jobs `submit_directory`** for serverless compute.

## Project Structure

```
03_ml_jobs_framework/
├── main.py                          # CLI entrypoint — run one or all pipelines
├── conda.yml                        # Conda environment (runtime dependencies)
├── pyproject.toml                   # Project metadata, black/ruff/isort config
├── .pre-commit-config.yaml          # Pre-commit hooks (black, ruff, isort, etc.)
├── conf/
│   └── parameters.yml               # Single YAML config for all pipelines
├── pipelines/
│   ├── feature_pipeline.py          # Feature Store: load → preprocess → register → dataset
│   ├── training_pipeline.py         # Submit HPO training job via submit_directory
│   ├── promotion_pipeline.py        # Promote best model version (alias, tags, default)
│   └── monitoring_pipeline.py       # Set up ModelMonitor for drift detection
└── src/
    ├── session.py                   # Snowpark session factory (local execution)
    ├── feature_engineering/
    │   ├── data_loader.py           # Join CUSTOMERS + PURCHASE_BEHAVIOR
    │   ├── preprocessing.py         # Feature derivation (Snowpark DataFrame ops)
    │   └── feature_store.py         # Entity, FeatureView, Dataset registration
    ├── modelling/
    │   ├── pipeline.py              # sklearn Pipeline (ColumnTransformer + XGBRegressor)
    │   ├── splitter.py              # Train/val split, DataConnector utilities
    │   ├── evaluate.py              # MAE, MAPE, R² evaluation
    │   └── train.py                 # ML Job entrypoint — HPO with Tuner (submit_directory)
    ├── ml_engineering/
    │   ├── promotion.py             # Best version selection, alias/tag/default promotion
    │   ├── serving.py               # Inference service deployment, batch predictions
    │   └── monitoring.py            # ModelMonitor setup
    └── utils/
        └── versioning.py            # Auto-increment version helpers for models & datasets
```

## Snowflake Services Used

| Service | Purpose |
|---|---|
| **ML Jobs (`submit_directory`)** | Submits `src/` directory to a compute pool; `modelling/train.py` is the entrypoint |
| **Feature Store** | Managed FeatureViews backed by Dynamic Tables with scheduled refresh |
| **Model Registry** | Versioned model storage with aliases, tags, and default versions |
| **Experiment Tracking** | Per-trial parameter/metric/model logging during HPO |
| **HPO Tuner** | RandomSearch over XGBoost hyperparameters across distributed trials |
| **Datasets & DataConnectors** | Immutable, versioned snapshots for reproducible training |
| **Model Monitor** | Continuous drift and performance monitoring |

## Quick Start

```bash
# Run the full pipeline end-to-end
python main.py all

# Run individual pipelines
python main.py feature      # Feature engineering + Feature Store
python main.py training     # Submit HPO training ML Job
python main.py promotion    # Promote best model
python main.py monitoring   # Set up monitoring

# Use custom config
python main.py all --config conf/parameters.yml
```

## How `submit_directory` Works

Unlike the `@remote` decorator (used in `02_ml_jobs_notebook`), this framework submits the entire `src/` directory to a Snowflake compute pool:

```python
from snowflake.ml.jobs import submit_directory

job = submit_directory(
    "./src/",                          # directory to upload
    "CLV_MODEL_POOL_CPU",              # compute pool
    entrypoint="modelling/train.py",   # script to execute
    args=["--dataset", "...", ...],    # CLI arguments
    stage_name="payload_stage",
    session=session,
)
job.wait()
```

Inside the container, `Session.builder.getOrCreate()` provides the Snowpark session automatically — no credentials needed.

## Configuration

All parameters live in `conf/parameters.yml`. Key sections:

- **snowflake** — connection, database, schema, warehouse
- **feature_store** — entity, feature view, refresh frequency, dataset name
- **model_registry** — schema for versioned models
- **modelling** — model name, feature/target columns, encoders, train/test split
- **compute** — pool name, stage, trial count, instance count
- **serving** — inference service config
- **monitoring** — prediction/baseline tables, refresh intervals

## Environment Setup

```bash
# Create conda environment
conda env create -f conda.yml
conda activate clv_ml_framework

# Install pre-commit hooks
pre-commit install

# Run linters manually
black .
ruff check . --fix
isort .
```

## Dev Tooling

| Tool | Config | Purpose |
|---|---|---|
| **black** | `pyproject.toml` | Code formatting (line-length=120) |
| **ruff** | `pyproject.toml` | Fast linting (pyflakes, pycodestyle, isort, bugbear) |
| **isort** | `pyproject.toml` | Import sorting (black-compatible profile) |
| **pre-commit** | `.pre-commit-config.yaml` | Git hooks: black, ruff, isort, trailing whitespace, YAML check, large file guard |

## Comparison with Other Implementations

| Aspect | 01 (Notebooks) | 02 (ML Jobs Notebook) | **03 (Framework)** |
|---|---|---|---|
| Execution | Interactive cells | `@remote` decorator | `submit_directory` |
| Structure | Single notebook | Notebook + helper `.py` | Modular packages |
| Config | Hardcoded | Hardcoded | `parameters.yml` |
| Reusability | Low | Medium | **High** |
| CI/CD Ready | No | Partial | **Yes** |
| HPO | In-notebook Tuner | In-notebook Tuner | **Entrypoint script** |
| Best For | Exploration | Prototyping | **Production** |
