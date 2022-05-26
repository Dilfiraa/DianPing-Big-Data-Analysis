from pyspark.sql import SparkSession
from pyspark import SparkContext
spark = SparkSession.builder.master("local").getOrCreate()
sc = SparkContext.getOrCreate()

from google.colab import drive
drive.mount('/content/gdrive')

import os
os.chdir("/content/gdrive/My Drive/")

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import udf
from pyspark.sql.functions import col, expr, when

spark = SparkSession.builder.appName("MyCSVLoad").getOrCreate()
    
df = spark.read.csv(path='/content/All.csv',
            sep=',',
            header=True,
            quote='"',
            inferSchema=True
            )

def isExist(str):
  for item in str:
    if item == '(':
      return 1
  else:
    return 0

func_udf = udf(isExist, IntegerType())
df = df.withColumn('if_multiple',func_udf(df['shop_name']))

shop_evaluation = when(col('shop_star') > 4, 1).otherwise(0)
df = df.withColumn('shop_evaluation',shop_evaluation)

df = df.drop('shop_region','shop_category','shop_district')
df = df.withColumn('shop_comment',df.shop_comment.astype('double'))
df = df.withColumn('if_multiple',df.if_multiple.astype('double'))
df = df.withColumn('shop_price',df.shop_price.astype('double'))
df = df.withColumn('shop_evaluation',df.shop_evaluation.astype('double'))
df = df.na.drop()

df.printSchema()
df.show()

df.groupBy('if_multiple').count().show()
df.groupBy('shop_evaluation').count().show()

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# transformer
assembler = VectorAssembler(inputCols=['if_multiple','shop_price','shop_comment'],
               outputCol='features')
output = assembler.transform(df)

model_df = output.select('features','shop_evaluation')
model_df.printSchema()

# data splitting
(training_df, test_df) = model_df.randomSplit([0.7, 0.3])

# train our model using training data
df_classifier = DecisionTreeClassifier(labelCol='shop_evaluation',featuresCol='features')
model = df_classifier.fit(training_df)

# test our model and make predictions using testing data
df_predictions = model.transform(test_df)

df_predictions.groupBy('prediction').count().show()

df_precision = MulticlassClassificationEvaluator(labelCol='shop_evaluation',metricName='weightedPrecision').evaluate(df_predictions)
print(df_precision)

df_accuracy = MulticlassClassificationEvaluator(labelCol='shop_evaluation',metricName='accuracy').evaluate(df_predictions)
print(df_accuracy)

importance = model.featureImportances
print(importance)