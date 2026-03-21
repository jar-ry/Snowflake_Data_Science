# 03 - ML Jobs

**Maturity Level:** ⭐⭐⭐ Advanced | **Runs In:** Snowflake (Serverless)

## Overview

Run production ML workflows using Snowflake ML Jobs. Schedule training pipelines, automate retraining, and leverage serverless compute for scalable, managed execution.

## When to Use

- ✅ Production-grade ML pipelines and retraining cadences
- ✅ Cron/event-triggered jobs that need Snowflake-managed runtime
- ✅ Teams ready to integrate with the Model Registry + monitoring
- ⚠️ Requires knowledge of ML Jobs APIs and deployment workflow
- ⚠️ Less interactive than notebooks—treat jobs like production code

## Contents

```
03_ml_jobs/
├── README.md                    # This file
├── jobs/
│   ├── training_job.py          # Training job definition
│   ├── feature_job.py           # Feature computation job
│   └── inference_job.py         # Batch inference job
├── config/
│   ├── job_config.yaml          # Job configuration
│   └── schedule_config.yaml     # Schedule definitions
├── src/
│   ├── features.py              # Feature logic
│   ├── train.py                 # Training logic
│   └── evaluate.py              # Evaluation logic
└── notebooks/
    ├── deploy_jobs.ipynb        # Deploy and manage jobs
```

## Prerequisites

- Completed `Step01_Setup.ipynb` (data setup)
- Completed `02_snowpark_sessions/` (recommended)
- Understanding of Snowflake ML Jobs API

## Quick Start

1. Open `notebooks/deploy_jobs.ipynb`
2. Configure job parameters
3. Deploy job to Snowflake
4. Set up schedule (optional)
5. Monitor runs

## What's Covered

- [ ] ML Job definition and deployment
- [ ] Scheduled training pipelines
- [ ] Serverless compute configuration
- [ ] Model Registry integration
- [ ] Job monitoring and logging
- [ ] Batch inference jobs

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                      Snowflake                              │
│                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │  Schedule/  │      │   ML Job    │      │   Model     │ │
│  │  Trigger    │ ───► │  Execution  │ ───► │  Registry   │ │
│  └─────────────┘      └─────────────┘      └─────────────┘ │
│         │                   │                     │         │
│         │                   ▼                     │         │
│         │         ┌─────────────────┐            │         │
│         │         │   Serverless    │            │         │
│         │         │    Compute      │            │         │
│         │         │  (Auto-scaled)  │            │         │
│         │         └─────────────────┘            │         │
│         │                   │                     │         │
│         ▼                   ▼                     ▼         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Feature Store / Tables                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

| Feature | Why it matters |
|---------|----------------|
| Serverless compute | Snowflake manages scaling and infrastructure |
| Schedules & triggers | Automate retraining via cron or events |
| Model Registry ready | Register versions as part of your pipeline |
| Built-in monitoring | Job run history, logging, and metrics |
| Security & governance | Runs within Snowflake's perimeter |

## ML Job Example

```python
from snowflake.ml.jobs import Job

# Define job
job = Job(
    name="CLV_TRAINING_JOB",
    source="@MY_STAGE/training_job.py",
    compute_pool="ML_COMPUTE_POOL",
    schedule="0 0 * * 0"  # Weekly
)

# Deploy and run
job.deploy()
job.run()

# Check status
job.status()
```

## Typical Workflow

```
[Define Job] ──► [Deploy to Snowflake] ──► [Schedule/Trigger]
                                                  │
                                                  ▼
[Monitor] ◄── [Log Results] ◄── [Execute] ──► [Save Model]
```

## Production Considerations

- **Monitoring**: Set up alerts for job failures
- **Logging**: Review job logs for debugging
- **Versioning**: Use Model Registry for model versions
- **Testing**: Test jobs in dev before production
- **Rollback**: Have rollback procedures ready

## Skills Required

- Familiarity with Snowflake ML Jobs + Container Runtime
- Understanding of production ML patterns (deploy, monitor, retrain)
- Comfort working with scheduling concepts and Model Registry
