import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import pymysql



def information_collection(url):
    conn = pymysql.connect(host='localhost', user='root', password='root', database='爬虫', port=3306)
    cursor = conn.cursor()
    movies = []
    headers={
        'user-agent': 'https://img3.doubanio.com/dae/accounts/resources/f5f3d66/movie/bundle.css',
        'Referer': 'https://img3.doubanio.com/dae/accounts/resources/f5f3d66/movie/bundle.css'
    }

    response = requests.get(url,headers=headers)

    text = response.content.decode('utf-8')

    bs = BeautifulSoup(text, 'lxml')
    ol = bs.find('ol', class_='grid_view')


    lis = ol.find_all('li')
    for li in lis:
        # 第一部分：由li标签下的a标签中的内容构成
        contents = li.find_all('a')
        a = contents[1]
        result = list(a.stripped_strings)
        title = result[0]
        english_name = result[1]
        english_name = english_name.replace(u'/\xa0',u'')
        # source = str(result[2])


        # 第二部分，由li标签下的<div class='bd'>中的内容构成
        divs = li.find_all('div', class_='bd')
        div = divs[0]
        q = div.find('p')
        actors = (list(q.stripped_strings))
        daoyan = actors[0].split(u'\xa0\xa0\xa0')[0]
        daoyan = daoyan.replace('导演:', '')
        try:
            zhuyan = actors[0].split(u'\xa0\xa0\xa0')[1]
            zhuyan = zhuyan.replace('主演:', '')
        except:
            pass
        leixing = actors[1]
        year = leixing.split(u'\xa0/\xa0')[0]
        # year取前4个字符
        year = year[0:4]
        conutry = leixing.split(u'\xa0/\xa0')[1]
        ticai = leixing.split(u'\xa0/\xa0')[2]

        # 插入数据库操作
        sql = '''
            insert into 豆瓣电影(id,片名,英文名,导演,主演,年份,国家,体裁) values (null,%s,%s,%s,%s,%s,%s,%s)
           '''
        片名=title
        英文名=english_name
        导演=daoyan
        主演=zhuyan
        年份=int(year)
        国家=conutry
        体裁=ticai
        cursor.execute(sql, (片名, 英文名, 导演, 主演, 年份, 国家, 体裁))
        conn.commit()
        movie={
            "片名":title,
            "英文名":english_name,
            '导演':daoyan,
            "主演":zhuyan,
            "年份":year,
            "国家":conutry,
            "体裁":ticai

        }
        movies.append(movie)
        print(movie)
        with open('豆瓣电影排名TOP250.txt','a',encoding='utf-8') as fp:
            fp.write(str(movie)+'\n')

    return movies
    conn.close()



def main():
    for i in range(10):
        url = 'https://movie.douban.com/top250?start='+str(i*25)+'&filter='
        information_collection(url)


if __name__=='__main__':
    main()