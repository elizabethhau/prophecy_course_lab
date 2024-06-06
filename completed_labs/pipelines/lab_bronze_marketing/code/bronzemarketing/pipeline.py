from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from bronzemarketing.config.ConfigStore import *
from bronzemarketing.udfs.UDFs import *
from prophecy.utils import *
from bronzemarketing.graph import *

def pipeline(spark: SparkSession) -> None:
    df_raw_marketing_events = raw_marketing_events(spark)
    df_raw_marketing_campaigns = raw_marketing_campaigns(spark)
    marketing_campaigns(spark, df_raw_marketing_campaigns)
    marketing_events(spark, df_raw_marketing_events)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/lab_bronze_marketing")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/lab_bronze_marketing", config = Config)(pipeline)

if __name__ == "__main__":
    main()
