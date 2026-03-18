# Snowflake Data Science - Retail CLV Regression Demo

## ⚠️ Disclaimer

**All opinions, code, and implementation details in this repository are my own personal views and do not represent the views, policies, or recommendations of my employer or any organization I am affiliated with.**

This project is provided for educational and demonstration purposes only. It is not intended as professional advice or a recommendation for any specific use case. Use at your own risk.

A demonstration project for building a **Customer Lifetime Value (CLV) Regression Model** using Snowflake's ML capabilities, Feature Store, and Snowpark.

## 📋 Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/download) installed
- Snowflake account with ACCOUNTADMIN privileges (for initial setup)
- Git (optional, for cloning)

## 🚀 Quick Start

### 1. Create the Conda Environment

Run the setup script to create the conda environment:

```bash
# Make the script executable (first time only)
chmod +x setup_env.sh

# Run the setup script
./setup_env.sh
```

Or manually create the environment:

```bash
conda env create -f conda.yml
```

### 2. Activate the Environment

```bash
conda activate snowflake_ds
```

### 3. Configure Snowflake Connection

Create a `connection.json` file in the project root with your Snowflake credentials:

```json
{
    "account": "your_account_identifier",
    "user": "your_username",
    "password": "your_password",
    "warehouse": "your_warehouse",
    "role": "ACCOUNTADMIN"
}
```

> ⚠️ **Security Note**: The `connection.json` file is included in `.gitignore` to prevent accidental credential commits.

### 4. Run the Setup Notebook

Launch JupyterLab and run the setup notebook:

```bash
jupyter lab
```

Then open and run `Step01_Setup.ipynb` to:
- Create the demo role, warehouse, database, and schema
- Generate mock retail data (10,000 customers by default)
- Create the `CLV_TRAINING_DATA` view for ML training

## 📁 Project Structure

```
Snowflake_Data_Science/
├── README.md                        # This file
├── IMPLEMENTATION_GUIDE.md          # Guide to choose implementation approach
├── conda.yml                        # Conda environment specification
├── setup_env.sh                     # Environment setup script
├── connection.json                  # Snowflake credentials (not in git)
├── helper/                          # Helper modules
│   ├── __init__.py
│   └── useful_fns.py                # Helper functions (run_sql, etc.)
├── Step01_Setup.ipynb               # Database & data setup notebook
└── implementations/                 # Different implementation approaches
    ├── 01_snowflake_notebooks/      # ⭐ Beginner - Snowflake UI
    ├── 02_snowpark_sessions/        # ⭐⭐ Intermediate - Local IDE
    └── 03_ml_jobs/                  # ⭐⭐⭐ Advanced - Production
```

## 🧭 Choose Your Implementation Path

This repo intentionally mirrors the three maturity levels outlined in [`IMPLEMENTATION_GUIDE.md`](IMPLEMENTATION_GUIDE.md). Use the guide's decision tree plus the matrix below to pick the right entry point:

| Level | Approach | Best For | Complexity | Where It Runs |
|-------|----------|----------|------------|---------------|
| 1 ⭐ | Snowflake Notebooks | Learning, POCs, shareable demos | Low | Snowflake UI |
| 2 ⭐⭐ | Snowpark Sessions | Local development, testing, CI | Medium | Local IDE + Snowflake warehouse |
| 3 ⭐⭐⭐ | ML Jobs | Production pipelines, scheduling | High | Snowflake serverless runtime |

### Quick Decision Reminders
- Need zero local setup? Start with `01_snowflake_notebooks/`.
- Want full IDE + Git workflow? Move into `02_snowpark_sessions/`.
- Ready for scheduled, scalable training + Model Registry? Deploy `03_ml_jobs/`.

The approaches are complementary—prototype in notebooks, industrialize via Snowpark, then operationalize with ML Jobs as shown below:

```
Snowflake Notebooks ──► Snowpark Sessions ──► ML Jobs
     Learn & share           Develop & test          Production-ready
         ⭐                       ⭐⭐                       ⭐⭐⭐
```

For screenshots, decision trees, and transition tips, keep [`IMPLEMENTATION_GUIDE.md`](IMPLEMENTATION_GUIDE.md) handy while you work through each folder.

## 📊 Data Model

The demo creates two joinable tables for CLV prediction:

### CUSTOMER_DEMOGRAPHICS (4 features)
| Column | Type | Description |
|--------|------|-------------|
| CUSTOMER_ID | INTEGER | Primary key |
| AGE | INTEGER | Customer age (18-75) |
| ANNUAL_INCOME | DECIMAL | Estimated income ($20k-$200k) |
| LOYALTY_TIER | VARCHAR | Loyalty segment label (`low`, `medium`, `high`) |
| GENDER | VARCHAR | Customer gender label (`male`, `female`) |
| STATE | VARCHAR | Australian state/territory (NSW, VIC, QLD, WA, SA, TAS, NT, ACT) |
| TENURE_MONTHS | INTEGER | Months as customer (1-120) |

### PURCHASE_BEHAVIOR (3 features + target)
> **Note:** LIFETIME_VALUE represents **Expected Monthly Value** (AVG_ORDER_VALUE × PURCHASE_FREQUENCY with adjustments), not cumulative lifetime value. This enables fair comparison across customers regardless of tenure.

| Column | Type | Description |
|--------|------|-------------|
| CUSTOMER_ID | INTEGER | Foreign key |
| AVG_ORDER_VALUE | DECIMAL | Average transaction ($15-$500) |
| PURCHASE_FREQUENCY | DECIMAL | Orders per month (0.1-8) |
| RETURN_RATE | DECIMAL | % items returned (0-30%) |
| LIFETIME_VALUE | DECIMAL | **🎯 Expected Monthly Value** (regression target) |

### CLV_TRAINING_DATA (View)
A unified view joining both tables with derived features for ML training.

## 🔧 Configuration Options

Edit the configuration cell in `Step01_Setup.ipynb` to customize:

```python
admin_role = 'ACCOUNTADMIN'              # Admin role for setup
demo_role = 'RETAIL_REGRESSION_DEMO_ROLE' # Data scientist role
database_name = 'RETAIL_REGRESSION_DEMO'
schema_name = 'DS'
warehouse_name = 'RETAIL_REGRESSION_DEMO_WH'
warehouse_size = 'SMALL'
num_customers = 10000                     # Number of customers to generate
```

## 🧹 Cleanup

To remove all created Snowflake objects, uncomment and run the cleanup cell at the end of `Step01_Setup.ipynb`.

To remove the conda environment:

```bash
conda deactivate
conda env remove -n snowflake_ds
```

## 📦 Environment Packages

Key packages included in the conda environment:

| Package | Version | Purpose |
|---------|---------|---------|
| python | 3.10 | Runtime |
| snowflake-snowpark-python | 1.38.0 | Snowpark DataFrame API |
| snowflake-ml-python | 1.19.0 | ML functions & Feature Store |
| scikit-learn | 1.5.1 | ML algorithms |
| pandas | 2.3.1 | Data manipulation |
| jupyterlab | 4.4.4 | Notebook interface |
| matplotlib | 3.10.6 | Visualization |

## 📝 License

This project is for demonstration purposes.

## 📚 Additional Resources

- [Snowflake Notebooks Documentation](https://docs.snowflake.com/en/user-guide/ui-snowsight/notebooks)
- [Snowpark Python Developer Guide](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
- [Snowflake ML Jobs](https://docs.snowflake.com/en/developer-guide/snowpark-ml/jobs)
- [Snowflake Model Registry](https://docs.snowflake.com/en/developer-guide/snowpark-ml/model-registry/overview)

