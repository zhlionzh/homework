
# 使用Prophet预测jetrail未来7个月213天的交通流量
# 从2012年8月25日开始
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt

#ip.get_ipython().run_line_magic('matplotlib', 'inline')

# 读入数据集
df = pd.read_csv('./train.csv')
#转化datetime为pd中格式
df['Datetime'] = pd.to_datetime(df.Datetime, format='%d-%m-%Y %H:%M')
df.index = df['Datetime']
df.drop(['ID', 'Datetime'], axis=1, inplace=True)
df['Count'].astype(int)
#print(df.head())
#print(df.tail())
#按day进行采样
daily_df = df.resample('D').sum()
#print(daily_df.head())
daily_df['ds'] = daily_df.index
daily_df['y'] = daily_df.Count
daily_df.drop(['Count'], axis=1, inplace=True)
#print(daily_df.head())
# 拟合模型,以day为单位聚合数据集
model = Prophet(yearly_seasonality=True, seasonality_prior_scale=0.1)
model.fit(daily_df)
future = model.make_future_dataframe(periods=213)
forecast = model.predict(future)
#print(forecast)
model.plot(forecast)
plt.show()
model.plot_components(forecast)
plt.show()

