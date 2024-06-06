from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from sol_module_6.config.ConfigStore import *
from sol_module_6.udfs.UDFs import *
from prophecy.utils import *
from sol_module_6.graph import *

def pipeline(spark: SparkSession) -> None:
    df_lab_malformed_products = lab_malformed_products(spark)
    df_reformat_lab_malformed_products = reformat_lab_malformed_products(spark, df_lab_malformed_products)
    df_Filter_NULL_price = Filter_NULL_price(spark, df_reformat_lab_malformed_products)
    cleaned_products(spark, df_Filter_NULL_price)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/lab_handle_malformed_json")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/lab_handle_malformed_json", config = Config)(
        pipeline
    )

if __name__ == "__main__":
    main()
