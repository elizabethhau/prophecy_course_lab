from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sol_module_6.config.ConfigStore import *
from sol_module_6.udfs.UDFs import *

def reformat_lab_malformed_products(spark: SparkSession, lab_malformed_products: DataFrame) -> DataFrame:
    return lab_malformed_products.select(
        to_date(col("date_introduced")).alias("date_introduced"), 
        col("extra_field"), 
        col("main_category"), 
        col("name"), 
        col("price_usd_cents").cast(LongType()).alias("price_usd_cents"), 
        col("product_id"), 
        col("sub_category")
    )
