import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType


### Creat spark sesssion
spark = SparkSession.builder.appName("Visualization").getOrCreate()

### read data from CVS file
df = spark.read.options(header=True, inferSchema=True).csv('All.csv')

### change the data tpye of coloums
df = df.withColumn('shop_comment', df['shop_comment'].cast('int'))
df = df.withColumn('shop_price', df['shop_price'].cast('int'))

### Delete rows which attributes shop_star, shop_price, shop_comment containing null values
df = df.na.drop(subset=['shop_star','shop_price','shop_comment'])

### Delete rows which attributes shop_star and shop_comment equals 0
df = df.filter((df['shop_star'] != 0) & (df['shop_comment'] != 0))

### delete rows which shop_category containing the stings below
ca = ['更多食品保健品', '保健品', '栗子/干果', '水果店', '水果生鲜', '生鲜','更多食品保健']
df = df.filter((df['shop_category'] != ca[0]) & (df['shop_category'] != ca[1]) &
               (df['shop_category'] != ca[2]) & (df['shop_category'] != ca[3]) &
               (df['shop_category'] != ca[4]) & (df['shop_category'] != ca[5]) &
               (df['shop_category'] != ca[6]))

### chage category based on Keyword
def changeCategory(x):
  if '泰式' in x:
    x = '泰国料理'
  elif '日式' in x:
    x = '日本料理'
  elif '韩式' in x:
    x = '韩国料理'
  elif '火锅' in x:
    x = '火锅'
  return x

### change shop name (use to find chain-store)
def changeName(x):
  x = x.split('(')[0]
  return x

### apply changeCategory function on shop_category
udf_changeCategory = udf(changeCategory, StringType())
df_all = df.withColumn("shop_category", udf_changeCategory(col("shop_category")))
# df_all.groupBy('shop_category_c').count().sort('count', ascending=False).show()


### apply changeName function on shop_name
udf_changeName = udf(changeName, StringType())
df_all = df_all.withColumn("shop_name", udf_changeName(col("shop_name")))
df_all.show()
# df_all.groupBy('shop_name_c').count().sort('count', ascending=False).show()

### store dataframe as csv file
df_all.write.csv('All_v.csv', header=True)