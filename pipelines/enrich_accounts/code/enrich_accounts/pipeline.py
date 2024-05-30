from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from enrich_accounts.config.ConfigStore import *
from enrich_accounts.udfs.UDFs import *
from prophecy.utils import *
from enrich_accounts.graph import *

def pipeline(spark: SparkSession) -> None:
    df_salesforce_account = salesforce_account(spark)
    df_salesforce_opportunity = salesforce_opportunity(spark)
    df_SelectFields = SelectFields(spark, df_salesforce_opportunity)
    df_byAccount = byAccount(spark, df_SelectFields)
    df_join_accounts_with_opportunities = join_accounts_with_opportunities(spark, df_salesforce_account, df_byAccount)
    enriched_accounts(spark, df_join_accounts_with_opportunities)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("enrich_accounts")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/enrich_accounts")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/enrich_accounts", config = Config)(pipeline)

if __name__ == "__main__":
    main()
