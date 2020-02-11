import requests
import re
from bs4 import BeautifulSoup

def collect(url):
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    html = response.content.decode('utf-8')
    title = re.findall(r'<div\sclass="yizhu">.*?<b>(.*?)</b>', html, re.DOTALL)
    dynasty = re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>', html, re.DOTALL)
    authors = re.findall(r'<p\sclass="source">.*?<a.*?>.*?</a>.*?<a.*?>(.*?)</a>', html, re.DOTALL)
    conts = re.findall(r'<div\sclass="contson".*?>(.*?)</div>', html, re.DOTALL)
    contents = []
    for cont in conts:
        x = re.sub('<br />|<p>|</p>|\\n', '', cont)
        contents.append(x.strip())

    bs = BeautifulSoup(html,'lxml')
    tags = bs.find_all('div',class_='tag')
    emotions = []
    for tag in tags:
        stris = ''
        ems = tag.find_all('a')
        for em in ems:
            aa = em.string
            stris += aa
        emotions.append(stris)

    poems = []

    for value in zip(title, dynasty, authors, contents, emotions):
        title, dynasty, authors, contents, emotions = value
        poem = {
            "标题":title,
            "朝代":dynasty,
            "作者":authors,
            "正文":contents,
            "思想感情":emotions
        }
        poems.append(poem)
    return poems

def write(poems):
    with open('古诗词网.txt','a')as fp:
        for poem in poems:
            fp.write(str(poem))
            fp.write('\r\n')
            print(poem)
    fp.close()












def main():
    for i in range(11):
        url = 'https://www.gushiwen.org/default_'+str(i)+'.aspx'
        many = collect(url)
        write(many)


if __name__=='__main__':
    main()