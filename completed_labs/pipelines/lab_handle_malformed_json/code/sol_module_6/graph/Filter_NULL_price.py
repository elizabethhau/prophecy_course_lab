from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sol_module_6.config.ConfigStore import *
from sol_module_6.udfs.UDFs import *

def Filter_NULL_price(spark: SparkSession, reformat_lab_malformed_products: DataFrame) -> DataFrame:
    return reformat_lab_malformed_products.filter(col("price_usd_cents").isNotNull())
