# 02 - Snowpark Sessions

**Maturity Level:** ⭐⭐ Intermediate | **Runs In:** Local IDE

## Overview

Develop and run ML workflows locally using Snowpark Python sessions. Connect from your favorite IDE (VS Code, PyCharm, Jupyter) to Snowflake and execute code that runs on Snowflake compute.

## When to Use

- ✅ Local development with full IDE debugging + extensions
- ✅ Configuration-driven projects that live in Git
- ✅ Teams that need unit tests, CI, and modular code
- ⚠️ Requires managing Python/conda environments yourself
- ⚠️ You own Snowflake connection files/credentials

## Contents

```
02_snowpark_sessions/
├── README.md                    # This file
├── config/
│   └── config.yaml              # Configuration
├── src/
│   ├── __init__.py
│   ├── data_loader.py           # Data loading utilities
│   ├── features.py              # Feature engineering
│   ├── train.py                 # Model training
│   └── evaluate.py              # Evaluation metrics
├── notebooks/
│   └── development.ipynb        # Development notebook
├── tests/
│   └── test_features.py         # Unit tests
└── main.py                      # CLI entry point
```

## Prerequisites

- Completed `Step01_Setup.ipynb` (data setup)
- Activated conda environment (`conda activate snowflake_ds`)
- Configured `connection.json`

## Quick Start

```bash
# Activate environment
conda activate snowflake_ds

# Run via notebook
jupyter lab notebooks/development.ipynb

# Or run via CLI
python main.py --config config/config.yaml
```

## What's Covered

- [ ] Snowpark session management
- [ ] Configuration-driven pipelines
- [ ] Modular code organization
- [ ] Feature engineering functions
- [ ] Model training and evaluation
- [ ] Unit testing

## How It Works

```
┌─────────────────────────┐         ┌─────────────────────────┐
│     Local Machine       │         │       Snowflake         │
│  ┌───────────────────┐  │         │  ┌─────────────────┐    │
│  │   Your IDE        │  │         │  │    Warehouse    │    │
│  │  (VS Code, etc.)  │  │         │  │    (Compute)    │    │
│  │                   │  │         │  └────────┬────────┘    │
│  │  ┌─────────────┐  │  │         │           │             │
│  │  │  Snowpark   │  │  │ ──────► │           ▼             │
│  │  │  Session    │──┼──┼─────────┼──►  Execute Query       │
│  │  └─────────────┘  │  │         │           │             │
│  │        │          │  │         │           ▼             │
│  │        ▼          │  │ ◄────── │     Return Results      │
│  │   Local Results   │  │         │                         │
│  └───────────────────┘  │         └─────────────────────────┘
└─────────────────────────┘
```

## Key Features

| Feature | Why it matters |
|---------|----------------|
| Full IDE workflows | Debug, lint, refactor with your favorite tools |
| Git + CI ready | Treat the project like any Python repo |
| Modular code | Organize into packages, tests, and configs |
| Mixed compute | Develop locally, execute in Snowflake |
| Testing support | Run unit/integration tests before deployment |
| Flexibility | Extend with any Python libs compatible with Snowpark |

## Snowpark Session Example

```python
from snowflake.snowpark import Session

# Create session
session = Session.builder.configs(connection_params).create()

# Use Snowpark DataFrames
df = session.table("CUSTOMER_DEMOGRAPHICS")
df.filter(df["AGE"] > 30).show()

# Close session
session.close()
```

## Skills Required

- Solid Python development fundamentals
- Comfort with IDE tooling (VS Code, PyCharm, etc.)
- Git basics + environment (conda) management

## Next Steps

Once comfortable, progress to `03_ml_jobs/` for production-ready scheduled pipelines.
