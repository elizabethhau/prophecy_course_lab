from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from bronzemarketing.config.ConfigStore import *
from bronzemarketing.udfs.UDFs import *

def bronze_marketing_events(spark: SparkSession, in0: DataFrame):
    from pyspark.sql.utils import AnalysisException

    try:
        desc_table = spark.sql("describe formatted {}".format(f"`rainforest`.`{Config.bronze}`.`marketing_events`"))
        table_exists = True
    except AnalysisException as e:
        table_exists = False

    in0.write\
        .format("delta")\
        .mode("overwrite")\
        .partitionBy("dt")\
        .saveAsTable(f"`rainforest`.`{Config.bronze}`.`marketing_events`")
