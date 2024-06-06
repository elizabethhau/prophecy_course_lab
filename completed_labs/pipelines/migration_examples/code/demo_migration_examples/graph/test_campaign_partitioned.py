from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from demo_migration_examples.config.ConfigStore import *
from demo_migration_examples.udfs.UDFs import *

def test_campaign_partitioned(spark: SparkSession, in0: DataFrame):
    from pyspark.sql.utils import AnalysisException

    try:
        desc_table = spark.sql("describe formatted {}".format(f"`rainforest`.`{Config.silver}`.`test_campaign_base`"))
        table_exists = True
    except AnalysisException as e:
        table_exists = False

    in0.write\
        .format("delta")\
        .option("mergeSchema", True)\
        .mode("append")\
        .partitionBy("campaign_start")\
        .saveAsTable(f"`rainforest`.`{Config.silver}`.`test_campaign_base`")
