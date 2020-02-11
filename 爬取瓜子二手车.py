import requests
from lxml import etree

# 这个网站目前爬不了

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Encoding':'gzip, deflate,br',
           'Accept-Language':'zh-CN,zh;q=0.9',
           'Cache-Control':'no-cache',
           'Host':'www.guazi.com',
           'Pragma':'no-cache',
           'Cookie': 'uuid=8040d873-c01e-402e-88a9-0c86b47fdd37; ganji_uuid=8543645553582222444971; lg=1; cityDomain=qd; antipas=0y09863B27022Rs878MR18w5h0; clueSourceCode=%2A%2300; user_city_id=114; sessionid=61daf3fe-70c4-438b-9e42-c4ae8b987588; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1580909365,1580957323,1580957925,1581131129; close_finance_popup=2020-02-08; GZ_TOKEN=cb487402%2FCJR1Hg3F7rx8%2B7cjzo6tgIFLihJ8W0J2UGE3%2FmoXBRCwUMvuWSQExuXaxhA2ojQAwxTzBgv4Amnk%2BKE88I7S504u72%2FjDsq65OvfbKJJ3tUHAYKetey%2F8CHLk%2B%2Fps%2FyzHomDUxfEA; guaZiUserInfo=bMSBnNXmcehT4GDGuhRn2; userid=736798585; CHDSSO=cb487402%2FCJR1Hg3F7rx8%2B7cjzo6tgIFLihJ8W0J2UGE3%2FmoXBRCwUMvuWSQExuXaxhA2ojQAwxTzBgv4Amnk%2BKE88I7S504u72%2FjDsq65OvfbKJJ3tUHAYKetey%2F8CHLk%2B%2Fps%2FyzHomDUxfEA; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%228040d873-c01e-402e-88a9-0c86b47fdd37%22%2C%22ca_city%22%3A%22lianyungang%22%2C%22sessionid%22%3A%2261daf3fe-70c4-438b-9e42-c4ae8b987588%22%7D; preTime=%7B%22last%22%3A1581131162%2C%22this%22%3A1580903346%2C%22pre%22%3A1580903346%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1581131160',
            'Referer':'https://www.guazi.com/qd/?ca_kw&ca_n=default&ca_s=seo_baidu',
            'Sec-Fetch-User': '?1',
           'Upgrade-Insecure-Requests':'1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
}

cars = []
def spider(url):
    response = requests.get(url=url,headers=headers)
    response.encoding = 'utf-8'
    text = response.content.decode('utf-8')
    print(text)
    html = etree.HTML(text)
    uls = html.xpath("//ul[@class=\"carlist clearfix js-top\"]")[0]
    lis = uls.xpath("./li")

    for li in lis:
        title = li.xpath('./a/@title')[0]
        price = li.xpath('./a/div[@class="t-price"]/p/text()')[0]
        wangzhi = li.xpath('./a/@href')[0]
        year = li.xpath('./a/div/text()')[0]
        mile = li.xpath('./a/div/text()')[1]
        server = li.xpath('./a/div/text()')[2]


        car = {
            "车型":title,
            "年份":year,
            "里程数":mile,
            "价格":price+'万',
            "链接":'https://www.guazi.com'+wangzhi,
            "服务类型":server
              }
        print(car)
        with open('guazi.txt', 'a') as fp:
            fp.write(str(car))
            fp.write('\r\n')
        cars.append(car)
        fp.close()






def all_url():
    for i in range(50):
        url = 'https://www.guazi.com/lianyungang/buy/o'+str(i)+'/#bread'
        spider(url)


def main():
    all_url()



if __name__ == '__main__':
    main()