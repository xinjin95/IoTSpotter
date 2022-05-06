#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: test01.py
@time: 4/8/21 10:57 PM
@desc:
"""

from pyspark.sql import Row
from pyspark.sql import SQLContext
from pyspark import SparkFiles
import pyspark
from pyspark import SparkContext
from pyspark.sql.types import *


sc = SparkContext()

#from pyspark.sql import SQLContext
url = "https://raw.githubusercontent.com/guru99-edu/R-Programming/master/adult.csv"

sc.addFile(url)
sqlContext = SQLContext(sc)

df_string = sqlContext.read.csv(SparkFiles.get("adult.csv"), header=True, inferSchema=  False)
df_string.printSchema()

def convertColumn(df, names, newType):
    for name in names:
        df = df.withColumn(name, df[name].cast(newType))
    return df

CONTI_FEATURES  = ['age', 'fnlwgt','capital_gain', 'education_num', 'capital_loss', 'hours_week']

df_string = convertColumn(df_string, CONTI_FEATURES, FloatType())

print("")

from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler

stringIndexer = StringIndexer(inputCol="workclass", outputCol="workclass_encoded")
model = stringIndexer.fit(df)
indexed = model.transform(df)
encoder = OneHotEncoder(dropLast=False, inputCol="workclass_encoded", outputCol="workclass_vec")
encoded = encoder.transform(indexed)
encoded.show(2)

from pyspark.ml import Pipeline

pipeline = Pipeline(stages=stages)
pipelineModel = pipeline.fit(df_remove)
model = pipelineModel.transform(df_remove)