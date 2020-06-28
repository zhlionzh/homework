# 使用KMeans进行聚类

from sklearn import preprocessing
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# 数据加载
data = pd.read_csv('car_data.csv', encoding='gbk')
train_x = data[["人均GDP", "城镇人口比重", "交通工具消费价格指数", "百户拥有汽车量"]]
# 规范化到 [0,1] 空间
train_x = preprocessing.MinMaxScaler().fit_transform(train_x)
# 使用KMeans聚类，n_clusters这个参数是订聚类个数，默认为8
km = KMeans(n_clusters=3)
# 训练
km.fit(train_x)
# 预测
predict_y = km.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
result.rename({0: u'KMeans聚类'}, axis=1, inplace=True)
print(result)
result.to_csv("car_result.csv", index=False)
#分层目视化
linkage_matrix = ward(train_x)
dendrogram(linkage_matrix)
plt.show()
