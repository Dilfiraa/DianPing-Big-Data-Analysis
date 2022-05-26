from pyspark.mllib.fpm import FPGrowth
from pyspark import SparkContext, SparkConf
import itertools
import os

conf=SparkConf().setMaster("local").setAppName("local_test")
sc=SparkContext(conf=conf)
sc.setLogLevel("ERROR")

data = sc.textFile("/content/01_test.csv")

NUM_DATA = len(data.collect())
print('count_shop', NUM_DATA)

transactions = data.map(lambda line: line.strip().split(','))

model = FPGrowth.train(transactions, minSupport=0.01, numPartitions=10)

result = model.freqItemsets()
tmp = result.collect()

for fi in tmp:
    print(fi)
print('numberOf_frequents', len(tmp))

freqDict = result.map(lambda x:[tuple(sorted(x[0])), x[1]]).collectAsMap()
print(freqDict)


def subSet(listVariable):  # 求列表所有非空真子集的函数
    newList = []
    for i in range(1, len(listVariable)):
        newList.extend(list(itertools.combinations(listVariable, i)))
    return newList


def computeConfidence(freqItemset):
    itemset = freqItemset[0]  #频繁项集
    freq = freqItemset[1]     #该项集出现的频率
    subItemset = subSet(itemset)#该频繁项集的所有非空子集
    rules = []
    for i in subItemset:
        complement = tuple(set(itemset).difference(set(i)))  # 对于每一个非空子集取补集
        itemLink = str(complement) + '->' + str(i)
        confidence = float(freq) / freqDict[tuple(sorted(i))]  # 求置信度
        lift = float(freq) * NUM_DATA / (freqDict[tuple(sorted(i))] * freqDict[tuple(sorted(complement))])  #求提升度
        rule = [itemLink, freq, confidence, lift]
        rules.append(rule)
    return rules


confidence = result.flatMap(computeConfidence)
tmp_confidence = confidence.collect()
for i in tmp_confidence:
    print(i)
print('计算完成置信度', len(tmp_confidence))

# 保留置信度大于0.5，提升度于1的规则
minSupportConfidence = confidence.filter(lambda x: x[2] > 0.18).filter(lambda x: x[3] > 1)

for rules in (minSupportConfidence.collect()):
    print(rules)
