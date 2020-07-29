import pandas as pd
from mlxtend.frequent_patterns import apriori as aps
from mlxtend.frequent_patterns import association_rules


def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


def mlx_apr(df):
    # mlx_apr挖掘频繁项集和频繁规则
    pd.options.display.max_columns = 100
    hot_encoded_df = df.groupby(['客户ID', '产品名称'])['产品名称'].count().unstack().reset_index().fillna(0).set_index('客户ID')
    hot_encoded_df = hot_encoded_df.applymap(encode_units)
    frequent_itemsets = aps(hot_encoded_df, min_support=0.08, use_colnames=True)
    frequent_itemsets = frequent_itemsets.sort_values(by="support", ascending=False)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    rules = rules.sort_values(by="lift", ascending=False)
    print("频繁项集：", frequent_itemsets)
    print("关联规则：", rules[(rules['lift'] >= 1) & (rules['confidence'] >= 0.2)])


def main():
    # 数据加载
    data = pd.read_csv('./ProjectB/订单表.csv', encoding='GBK')
    # 去掉none项
    data = data.drop(data[data.产品名称 == 'none'].index)
    df1 = pd.DataFrame(data, columns=['产品名称', '客户ID'])
    mlx_apr(df1)


if __name__ == '__main__':
    main()