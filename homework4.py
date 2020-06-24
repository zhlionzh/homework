import requests
from bs4 import BeautifulSoup
import pandas as pd
def get_content(page):
    #网址获取
    url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-{}.shtml'.format(page+1)
    #网站爬取 requests 请求参数 headers获取（目标网页，右键检查，network->doc 中name列表选择对应网页，查看headers)
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

    #requests解析结构
    html=requests.get(url,headers=headers,timeout=10)
    #将网页内容赋值给content
    content = html.text
    return(content)
def analysis_data(page):
    df = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'problem', 'desc', 'datetime', 'status'])
    for num in range(page):
        content = get_content(num)
        #BeautifulSoup初始化
        #初始化BeautifulSoup类时，需要加入两个参数，第一个参数即是我们爬到html源码，第二个参数是html解析器，常用的有三个解析器，分别是”html.parser”,”lxml”,”html5lib”，官网推荐用lxml，因为效率高，当然需要pip install lxml一下。
        soup = BeautifulSoup(content,'html.parser')
        # 找到完整的投诉信息框
        temps = soup.find('div',class_="tslb_b")
        # 创建DataFrame

        tr_list = temps.find_all('tr')

        for tr in tr_list:
            td_list = tr.find_all('td')
            temp={}
            if len(td_list)>0:
                id,brand,car_model,type,problem,desc,datetime,status = td_list[0].text,td_list[1].text,td_list[2].text,td_list[3].text,td_list[4].text,td_list[5].text,td_list[6].text,td_list[7].text
                temp['id'], temp['brand'], temp['car_model'], temp['type'], temp['problem'], temp['desc'], temp['datetime'], temp['status'] = id,brand,car_model,type,problem,desc,datetime,status
                df = df.append(temp,ignore_index= True)
    return df
def main():

    page = int(input('请输入需要爬取的页数：\n'))
    data=analysis_data(page)
    print(data)
    file_name = input('请输入转存文件名：\n')
    data.to_csv(file_name, encoding="utf_8")

if __name__ == '__main__':
    main()
