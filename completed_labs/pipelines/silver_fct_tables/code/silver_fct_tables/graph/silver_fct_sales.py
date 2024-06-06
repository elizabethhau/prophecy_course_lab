from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from silver_fct_tables.config.ConfigStore import *
from silver_fct_tables.udfs.UDFs import *

def silver_fct_sales(spark: SparkSession, in0: DataFrame):
    from pyspark.sql.utils import AnalysisException

    try:
        desc_table = spark.sql("describe formatted {}".format(f"`rainforest`.`{Config.silver}`.`fct_sales`"))
        table_exists = True
    except AnalysisException as e:
        table_exists = False

    in0.write\
        .format("delta")\
        .option("overwriteSchema", True)\
        .mode("overwrite")\
        .partitionBy("sale_date")\
        .saveAsTable(f"`rainforest`.`{Config.silver}`.`fct_sales`")
