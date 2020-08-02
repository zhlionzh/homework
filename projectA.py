import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_soup(page):
    # 请求URL
    url = 'http://car.bitauto.com/xuanchegongju/?mid=8&page={}'.format(page+1)
    # 得到页面的内容
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    html = requests.get(url, headers=headers, timeout=10)
    content = html.text
    return content

def data_analysis(page):
    df = pd.DataFrame(columns=['car_model', 'lowest_price', 'hightest_price', 'picture_url'])
    for num in range(page):
        content = get_soup(num)
        # 通过content创建BeautifulSoup对象
        soup = BeautifulSoup(content, 'html.parser')
        # 找到完整的投诉信息框
        temp = soup.find('div', class_="search-result-list")
        # 创建DataFrame
        a_list = temp.find_all('a')
        for a in a_list:
            temp = {}
            temp['car_model'] = a.find_all('p', class_="cx-name text-hover")[0].text
            price = a.find_all('p', class_="cx-price")[0].text.split('-')
            if len(price)>1:
                temp['lowest_price'] = price[0]+'万'
                temp['hightest_price'] = price[1]
            else:
                temp['lowest_price'] = price[0]
                temp['hightest_price'] = price[0]
            temp['picture_url'] = a.find_all('img')[0]['src']
            df = df.append(temp, ignore_index= True)
    return df

def main():
    #page = int(input('请输入需采集页数：\n'))
    page = 3
    df = data_analysis(page)
    print(df)
    ab = input('数据是否导出（Y/N):')
    if ab == 'Y':
        csv_path = input('请输入导出文件名：\n')
        df.to_csv(csv_path)
        print('导出成功，谢谢使用！')
    else:
        print('操作完成，谢谢使用！')

if __name__ == '__main__':
    main()
