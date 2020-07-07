import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from efficient_apriori import apriori
from mlxtend.frequent_patterns import apriori as aps
from mlxtend.frequent_patterns import association_rules


def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


def get_transaction(data_set):
    # 将数据存放到transactions中
    transactions = []
    for i in range(0, data_set.shape[0]):
        temp = []
        for j in range(0, 20):
            if str(data_set.values[i, j]) != 'nan':
               temp.append(str(data_set.values[i, j]))
        transactions.append(temp)
    return transactions


def get_dataframe(transactions):
    #Transactions dataframe转化
    tp = []
    tq = []
    x = 0
    for list in transactions:
        for y in list:
            tp.append(x)
            tq.append(y)
        x = x+1
    data = zip(tp, tq)
    df = pd.DataFrame(data, columns=['Transaction', 'Items'])
    df.to_csv('temp1.csv')
    return df


def efficient_apr(transactions):
    #efficient_apr挖掘频繁项集和频繁规则
    itemsets, rules = apriori(transactions, min_support=0.02,  min_confidence=0.4)
    print("频繁项集：", itemsets)
    print("关联规则：", rules)


def mlx_apr(df):
    # mlx_apr挖掘频繁项集和频繁规则
    pd.options.display.max_columns = 100
    hot_encoded_df = df.groupby(['Transaction', 'Items'])['Items'].count().unstack().reset_index().fillna(0).set_index('Transaction')
    hot_encoded_df = hot_encoded_df.applymap(encode_units)
    frequent_itemsets = aps(hot_encoded_df, min_support=0.05, use_colnames=True)
    frequent_itemsets = frequent_itemsets.sort_values(by="support" , ascending=False)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    rules = rules.sort_values(by="lift", ascending=False)
    print("频繁项集：", frequent_itemsets)
    print("关联规则：", rules[(rules['lift'] >= 0.1) & (rules['confidence'] >= 0.2)])


def main():
    # header=None，不将第一行作为head
    data_set = pd.read_csv('./Market_Basket_Optimisation.csv', header=None)
    transactions = get_transaction(data_set)
    efficient_apr(transactions)
    df = get_dataframe(transactions)
    mlx_apr(df)


if __name__ == '__main__':
    main()