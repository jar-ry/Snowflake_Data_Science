import snowflake.snowpark.functions as F
from snowflake.snowpark import DataFrame


def pre_process(data: DataFrame) -> DataFrame:
    data = data.with_column("ANNUAL_INCOME", F.round(F.col("ANNUAL_INCOME"), 0))

    data = data.with_columns(
        [
            "AVERAGE_ORDER_PER_MONTH",
            "DAYS_SINCE_LAST_PURCHASE",
            "DAYS_SINCE_SIGNUP",
            "EXPECTED_DAYS_BETWEEN_PURCHASES",
            "DAYS_SINCE_EXPECTED_LAST_PURCHASE_DATE",
        ],
        [
            F.col("TOTAL_ORDERS") / F.col("TENURE_MONTHS"),
            F.datediff("day", F.col("LAST_PURCHASE_DATE"), F.col("BEHAVIOR_UPDATED_AT")),
            F.datediff("day", F.col("SIGNUP_DATE"), F.col("BEHAVIOR_UPDATED_AT")),
            F.lit(30) / F.col("PURCHASE_FREQUENCY"),
            F.round(
                F.datediff("day", F.col("LAST_PURCHASE_DATE"), F.col("BEHAVIOR_UPDATED_AT"))
                - F.lit(F.lit(30) / F.col("PURCHASE_FREQUENCY")),
                0,
            ),
        ],
    )

    return data
