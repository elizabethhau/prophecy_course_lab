from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sol_gold_marketing.config.ConfigStore import *
from sol_gold_marketing.udfs.UDFs import *

def sol_gold_quarterly_campaign_revenue(spark: SparkSession, in0: DataFrame):
    from pyspark.sql.utils import AnalysisException

    try:
        desc_table = spark.sql(
            "describe formatted {}".format(f"`rainforest`.`{Config.gold}`.`quarterly_campaign_revenue`")
        )
        table_exists = True
    except AnalysisException as e:
        table_exists = False

    in0.write\
        .format("delta")\
        .mode("overwrite")\
        .saveAsTable(f"`rainforest`.`{Config.gold}`.`quarterly_campaign_revenue`")
