# 01 - Snowflake Notebooks

**Maturity Level:** ⭐ Beginner | **Runs In:** Snowflake UI

## Overview

Run ML workflows directly in the Snowflake UI using Snowflake Notebooks. No local setup required - everything runs in the browser with Snowflake-managed compute.

## When to Use

- ✅ Learning Snowflake ML capabilities quickly
- ✅ Rapid data exploration, prototyping, and sharing with stakeholders
- ✅ Ad-hoc analysis where you want zero environment management
- ⚠️ UI-first experience with lighter IDE features

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    Snowflake UI                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Snowflake Notebook                       │  │
│  │                                                       │  │
│  │   [Python Cell] ──► [SQL Cell] ──► [Python Cell]     │  │
│  │         │               │               │             │  │
│  │         ▼               ▼               ▼             │  │
│  │   Load Data      Query Tables    Train Model          │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│              Snowflake Warehouse (Compute)                  │
└─────────────────────────────────────────────────────────────┘
```

## Contents

```
01_snowflake_notebooks/
├── README.md                        # This file
└── CLV_Model_Notebook.sql           # Notebook export (importable to Snowflake)
```

## Prerequisites

- Completed `Step01_Setup.ipynb` (data setup)
- Access to Snowflake UI (Snowsight)

## Quick Start

1. Log into Snowflake (Snowsight)
2. Navigate to **Notebooks** in the left menu
3. Create a new notebook or import the provided `.sql` file
4. Select your warehouse and run cells

## What's Covered

- [ ] Data exploration with SQL cells
- [ ] Feature engineering with Python cells
- [ ] Model training with Snowflake ML
- [ ] Model evaluation and visualization
- [ ] Saving predictions to tables

## Key Benefits

| Benefit | Description |
|---------|-------------|
| No local setup | Everything runs in the browser |
| Mixed cells | Combine Python + SQL in one place |
| Collaboration | Share notebooks directly in Snowsight |
| Snowflake compute | Uses your warehouse for execution |

## Skills Required

- Basic Python + SQL
- Familiarity with Snowsight navigation

## Next Steps

Once comfortable, progress to `02_snowpark_sessions/` for local development with full IDE features.
