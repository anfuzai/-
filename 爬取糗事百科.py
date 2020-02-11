import requests
import re


def collect(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    html = response.text
    # 这里有个关键：正则表达式中的.*可以匹配任意字符但不包含换行符，这里可以使用[\s\S]*代替之
    jokes_source = re.findall(r'<div class="content">[\s\S]*?<span>([\s\S]*?)</span>', html)

    jokes = []
    for i in jokes_source:
        joke = re.sub(r'<br/>|\n|(,+)|&quot', '', i)
        jokes.append(joke)

    return jokes


def write(list):
    for i in list:
        print(i)
        with open('糗事百科.txt', 'a', encoding='utf-8')as fp:
            fp.write(i)
            fp.write('\r\n')
    fp.close()


def main():
    for i in range(1,14):
        url = 'https://www.qiushibaike.com/hot/page/'+str(i)+'/'
        write(collect(url))


if __name__=='__main__':
    main()