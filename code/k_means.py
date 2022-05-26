from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import StructField, LongType
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
import matplotlib.pyplot as plt
from __future__ import print_function
from mpl_toolkits.mplot3d import Axes3D
from pyspark.sql import SQLContext
from pyspark import SparkContext
import libarchive
import pydot
import cartopy
import pyspark


spark = SparkSession.builder \
    .appName('compute_customer_age') \
    .config('spark.executor.memory','2g') \
    .enableHiveSupport() \
    .getOrCreate()

df=spark.read.csv(
    path="All.csv",
    sep=",",
    header=True,
    quote=",",
    inferSchema=True
    )


df1=df.withColumn("shop_star",df.shop_star.astype("double"))
df2=df1.withColumn("shop_comment",df.shop_comment.astype("double"))
df3=df2.withColumn("shop_price",df.shop_price.astype("double"))
df3.printSchema()

df3.na.drop() 
df_new=df3.drop('shop_name','shop_region','shop_category','shop_district')


df = spark.read.options(header=True, inferSchema=True).csv('All.csv')
df = df.withColumn('shop_comment', df['shop_comment'].cast('int'))
df = df.withColumn('shop_price', df['shop_price'].cast('int'))
df = df.na.drop()


feature_cols=["shop_star","shop_comment","shop_price"]
assembler = VectorAssembler(inputCols=feature_cols , outputCol="features")
dataset= assembler.transform(df).select('features')


schema = df.schema.add(StructField("id", LongType()))
rdd = df.rdd.zipWithIndex()

def flat(l):
    for k in l:
        if not isinstance(k, (list, tuple)):
            yield k
        else:
            yield from flat(k)

rdd = rdd.map(lambda x: list(flat(x)))
df = spark.createDataFrame(rdd, schema)


feature_cols=["shop_star","shop_comment","shop_price"]
assembler = VectorAssembler(inputCols=feature_cols , outputCol="features")
final_df = assembler.transform(df).select('id','features')


kmeans = KMeans().setK(2).setSeed(1)
model = kmeans.fit(dataset)

predictions = model.transform(dataset)
evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(predictions)
print("Silhouette with squared euclidean distance = " + str(silhouette))

centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)

for k in range(2,20):
  kmeans = KMeans().setK(k).setSeed(1)
  model = kmeans.fit(dataset)
  predictions = model.transform(dataset)
  silhouette = evaluator.evaluate(predictions)
  Silhouette_score=str(silhouette)+str(k)
  print(Silhouette_score)


fig, ax = plt.subplots(1,1, figsize =(8,6))
ax.plot(range(2,20),Silhouette_score)
ax.set_xlabel('k')
ax.set_ylabel('cost')


k =10
kmeans = KMeans().setK(k).setSeed(1).setFeaturesCol("features")
model = kmeans.fit(final_df)
centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)

transformed = model.transform(final_df).select('id','prediction')
rows = transformed.collect()


sparkContext = SparkContext.getOrCreate()
sqlContext = SQLContext(sparkContext)
df_pred = sqlContext.createDataFrame(rows)


df_pred = df_pred.join(df,'id')
pddf_pred = df_pred.toPandas().set_index('id')


# Commented out IPython magic to ensure Python compatibility.
threedee = plt.figure(figsize=(15,15)).gca(projection='3d')
threedee.axes.set_xlim3d(xmin=0, xmax=5)
threedee.axes.set_ylim3d(ymin=0, ymax=10000)
threedee.axes.set_zlim3d(zmin=0, zmax=500)
threedee.scatter(pddf_pred.shop_star, pddf_pred.shop_comment, pddf_pred.shop_price, c=pddf_pred.prediction)
threedee.set_xlabel('shop_star')
threedee.set_ylabel('shop_comment ')
threedee.set_zlabel('shop_price')
 
plt.rcParams['savefig.dpi'] = 400  
plt.rcParams['figure.dpi'] = 400  
plt.show()





