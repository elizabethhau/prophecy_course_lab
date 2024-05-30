from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from enrich_accounts.config.ConfigStore import *
from enrich_accounts.udfs.UDFs import *

def enriched_accounts(spark: SparkSession, join_accounts_with_opportunities: DataFrame):
    join_accounts_with_opportunities.write\
        .format("delta")\
        .option("overwriteSchema", True)\
        .mode("overwrite")\
        .saveAsTable("`rainforest`.`silver`.`enriched_accounts`")
