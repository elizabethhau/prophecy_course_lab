from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from silvermarketing.config.ConfigStore import *
from silvermarketing.udfs.UDFs import *
from prophecy.utils import *
from silvermarketing.graph import *

def pipeline(spark: SparkSession) -> None:
    df_bronze_marketing_events = bronze_marketing_events(spark)
    df_IsClick = IsClick(spark, df_bronze_marketing_events)
    df_bronze_marketing_campaigns = bronze_marketing_campaigns(spark)
    df_JoinProductId = JoinProductId(spark, df_IsClick, df_bronze_marketing_campaigns)
    df_silver_fct_sales = silver_fct_sales(spark)
    df_JoinSalesDate = JoinSalesDate(spark, df_JoinProductId, df_silver_fct_sales)
    df_SumRevenue = SumRevenue(spark, df_JoinSalesDate)
    df_SumCosts = SumCosts(spark, df_bronze_marketing_events)
    df_campaign_join = campaign_join(spark, df_SumCosts, df_SumRevenue, df_bronze_marketing_campaigns)
    dim_campaign(spark, df_campaign_join)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/lab_silver_marketing")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/lab_silver_marketing", config = Config)(pipeline)

if __name__ == "__main__":
    main()
