# Snowflake Data Science - Retail CLV Regression Demo

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
├── README.md                    # This file
├── conda.yml                    # Conda environment specification
├── setup_env.sh                 # Environment setup script
├── connection.json              # Snowflake credentials (not in git)
├── helper/                      # Helper modules
│   ├── __init__.py
│   └── useful_fns.py            # Helper functions (run_sql, etc.)
├── Step01_Setup.ipynb           # Database & data setup notebook
└── Step01_TPCXAI_UC01_Setup.ipynb  # Original TPCXAI setup (reference)
```

## 📊 Data Model

The demo creates two joinable tables for CLV prediction:

### CUSTOMER_DEMOGRAPHICS (4 features)
| Column | Type | Description |
|--------|------|-------------|
| CUSTOMER_ID | INTEGER | Primary key |
| AGE | INTEGER | Customer age (18-75) |
| ANNUAL_INCOME | DECIMAL | Estimated income ($20k-$200k) |
| LOYALTY_TIER | INTEGER | 1=Bronze, 2=Silver, 3=Gold, 4=Platinum |
| TENURE_MONTHS | INTEGER | Months as customer (1-120) |

### PURCHASE_BEHAVIOR (3 features + target)
| Column | Type | Description |
|--------|------|-------------|
| CUSTOMER_ID | INTEGER | Foreign key |
| AVG_ORDER_VALUE | DECIMAL | Average transaction ($15-$500) |
| PURCHASE_FREQUENCY | DECIMAL | Orders per month (0.1-8) |
| RETURN_RATE | DECIMAL | % items returned (0-30%) |
| LIFETIME_VALUE | DECIMAL | **🎯 Regression target** |

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

