from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from lxml import etree
from nltk.tokenize import word_tokenize


def get_transaction(data1):
	# 将数据存放到transactions中
	transaction = []
	for i in range(0, data1.shape[0]):
		temp = []
		for j in range(0, 20):
			item = str(data1.values[i, j])
			if item != 'nan':
				temp.append(item)
		transaction.append(temp)
	return transaction


# 去掉停用词
def remove_stop_words(f):
	stop_words = ['Nan']
	for stop_word in stop_words:
		f = f.replace(stop_word, '')
	return f


# 生成词云
def create_word_cloud(f):
	print('根据词频，开始生成词云!')
	#f = remove_stop_words(f)
	cut_text = word_tokenize(f)
	#print(cut_text)
	cut_text = " ".join(cut_text)
	wc = WordCloud(
		max_words=100,
		width=2000,
		height=1200,
    )
	wordcloud = wc.generate(cut_text)
	# 写词云图片
	wordcloud.to_file("wordcloud.jpg")
	# 显示词云文件
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()


# 主函数
def main():
	# 数据加载
	data = pd.read_csv('./Market_Basket_Optimisation.csv', header=None)
	transactions = get_transaction(data)
	all_word = " ".join('%s' %item for item in transactions)
	# 生成词云
	create_word_cloud(all_word)


if __name__ == '__main__':
	main()
