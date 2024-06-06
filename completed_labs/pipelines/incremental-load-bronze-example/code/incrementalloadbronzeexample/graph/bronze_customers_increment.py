from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from incrementalloadbronzeexample.config.ConfigStore import *
from incrementalloadbronzeexample.udfs.UDFs import *

def bronze_customers_increment(spark: SparkSession, in0: DataFrame):
    from pyspark.sql.utils import AnalysisException

    try:
        desc_table = spark.sql("describe formatted {}".format(f"`rainforest`.`{Config.bronze}`.`customers`"))
        table_exists = True
    except AnalysisException as e:
        table_exists = False

    if table_exists:
        from delta.tables import DeltaTable, DeltaMergeBuilder
        updatesDF = in0.withColumn("is_original", lit("true")).withColumn("is_current", lit("true"))
        updateColumns = updatesDF.columns
        existingTable = DeltaTable.forName(spark, f"`rainforest`.`{Config.bronze}`.`customers`")
        existingDF = existingTable.toDF()
        cond = None
        scdHistoricColumns = ["signup_date",  "customer_name",  "phone_number",  "street_number",  "street_name",  "unit",  "city",                               "state",  "postcode",  "lat",  "lon"]

        for scdCol in scdHistoricColumns:
            if cond is None:
                cond = (~ (existingDF[scdCol]).eqNullSafe(updatesDF[scdCol]))
            else:
                cond = (cond | (~ (existingDF[scdCol]).eqNullSafe(updatesDF[scdCol])))

        stagedUpdatesDF = updatesDF\
                              .join(existingDF, ["customer_id"])\
                              .where((existingDF["is_current"] == lit("true")) & (cond))\
                              .select(*[updatesDF[val] for val in updateColumns])\
                              .withColumn("is_original", lit("false"))\
                              .withColumn("mergeKey", lit(None))\
                              .union(updatesDF.withColumn("mergeKey", concat("customer_id")))
        updateCond = None

        for scdCol in scdHistoricColumns:
            if updateCond is None:
                updateCond = (~ (existingDF[scdCol]).eqNullSafe(stagedUpdatesDF[scdCol]))
            else:
                updateCond = (updateCond | (~ (existingDF[scdCol]).eqNullSafe(stagedUpdatesDF[scdCol])))

        existingTable\
            .alias("existingTable")\
            .merge(stagedUpdatesDF.alias("staged_updates"), concat(existingDF["customer_id"]) == stagedUpdatesDF["mergeKey"])\
            .whenMatchedUpdate(
              condition = (existingDF["is_current"] == lit("true")) & updateCond,
              set = {
"is_current" : "false", "valid_to" : "staged_updates.valid_from"}
            )\
            .whenNotMatchedInsertAll()\
            .execute()
    else:
        in0.write.format("delta").mode("overwrite").saveAsTable(f"`rainforest`.`{Config.bronze}`.`customers`")
