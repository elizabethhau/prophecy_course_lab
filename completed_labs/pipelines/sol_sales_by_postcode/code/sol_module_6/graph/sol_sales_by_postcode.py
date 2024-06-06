from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sol_module_6.config.ConfigStore import *
from sol_module_6.udfs.UDFs import *

def sol_sales_by_postcode(spark: SparkSession, in0: DataFrame):
    from pyspark.sql.utils import AnalysisException

    try:
        desc_table = spark.sql("describe formatted {}".format(f"`rainforest`.`{Config.gold}`.`sol_sales_by_postcode`"))
        table_exists = True
    except AnalysisException as e:
        table_exists = False

    in0.write.format("delta").mode("overwrite").saveAsTable(f"`rainforest`.`{Config.gold}`.`sol_sales_by_postcode`")