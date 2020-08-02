# 使用KMeans进行聚类
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn import preprocessing
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, ward
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# 数据加载
def file_decode(file_path):
    data = pd.read_csv(file_path)
    # column_name = pd.read_csv('./ProjectC/Data Dictionary - carprices.xlsx')
    # print(column_name[0])
    train_x = data[["fueltype", "aspiration", "doornumber", "carbody", "drivewheel", "enginelocation",
                    "wheelbase", "carlength", "carwidth", "carheight", "curbweight", "enginetype", "cylindernumber",
                    "enginesize", "fuelsystem", "boreratio", "stroke", "compressionratio", "horsepower", "peakrpm",
                    "citympg", "highwaympg", "price"]]
    # print(train_x)
    # LabelEncoder
    le = LabelEncoder()
    train_x['fueltype'] = le.fit_transform(train_x['fueltype'])
    train_x['aspiration'] = le.fit_transform(train_x['aspiration'])
    train_x['doornumber'] = le.fit_transform(train_x['doornumber'])
    train_x['carbody'] = le.fit_transform(train_x['carbody'])
    train_x['drivewheel'] = le.fit_transform(train_x['drivewheel'])
    train_x['enginelocation'] = le.fit_transform(train_x['enginelocation'])
    train_x['enginetype'] = le.fit_transform(train_x['enginetype'])
    train_x['cylindernumber'] = le.fit_transform(train_x['cylindernumber'])
    train_x['fuelsystem'] = le.fit_transform(train_x['fuelsystem'])
    # 规范化到 [0,1] 空间
    min_max_scaler = preprocessing.MinMaxScaler()
    train_x = min_max_scaler.fit_transform(train_x)
    # pd.DataFrame(train_x).to_csv('temp.csv', index=False)
    #print(train_x)
    return train_x


def kmeans_cluster(k, train_x, file_path):
    # 使用KMeans聚类
    data = pd.read_csv(file_path)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(train_x)
    predict_y = kmeans.predict(train_x)
    # 合并聚类结果，插入到原数据中
    result = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
    result.rename({0: u'聚类结果'}, axis=1, inplace=True)
    print(result)
    # 将结果导出到CSV文件中
    result.to_csv(file_path, index=False, encoding='gbk')


# K-Means 手肘法：统计不同K取值的误差平方和
def k_values(train_x):
    sse = []
    for k in range(1, 11):
        # kmeans算法
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(train_x)
        # 计算inertia簇内误差平方和
        sse.append(kmeans.inertia_)
    x = range(1, 11)
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.plot(x, sse, 'o-')
    plt.show()


# 使用层次聚类
def link_method(train_x, k):
    model = AgglomerativeClustering(linkage='ward', n_clusters=k)
    y = model.fit_predict(train_x)
    # print(y)
    linkage_matrix = ward(train_x)
    dendrogram(linkage_matrix)
    plt.show()


def main():
    file_path = './ProjectC/CarPrice_Assignment.csv'
    train_x = file_decode(file_path)
    k_values(train_x)
    k = int(input('请输入聚合分类数量：\n'))
    kmeans_cluster(k, train_x, file_path)
    link_method(train_x, k)


if __name__ == '__main__':
    main()
