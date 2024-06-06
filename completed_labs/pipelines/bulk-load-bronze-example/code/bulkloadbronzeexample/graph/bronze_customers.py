from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from bulkloadbronzeexample.config.ConfigStore import *
from bulkloadbronzeexample.udfs.UDFs import *

def bronze_customers(spark: SparkSession, in0: DataFrame):
    from pyspark.sql.utils import AnalysisException

    try:
        desc_table = spark.sql("describe formatted {}".format(f"`rainforest`.`{Config.bronze}`.`customers`"))
        table_exists = True
    except AnalysisException as e:
        table_exists = False

    in0.write\
        .format("delta")\
        .option("overwriteSchema", True)\
        .mode("overwrite")\
        .saveAsTable(f"`rainforest`.`{Config.bronze}`.`customers`")
