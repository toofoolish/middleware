from lxml import etree
import json
# f = open('temp').readlines()
# f.xpath()
# print(f)
# f.close()
response = etree.parse('temp', etree.HTMLParser())
title = response.xpath('//title/text()')
print(title)
# autim = response.xpath('//*[contains(@class,"page_b1")]/text()')[-1]
# print(autim)
# table = response.xpath('//*[contains(@class,"m_area_a")]/tr[6]/td[2]/text()')[0]
# for i in table:
#     print(table.xpath('/td[1]/text()'))
# print(table)
# txt = response.xpath('//a[text()="打开"]/')
# print(txt)
pages = response.xpath('//div[contains(@class,"content")]/text()')
print(pages)
content = ''
for line in pages:
    content += line.strip()
print(content)
# next = response.xpath('//button[contains(@class,"page_b2")]/following::a[1]/@href')
# print(next)
# txt = response.xpath('//td[text()="本单成交:"]/following::*[1]/text()')
# print(txt)
d = { 'a': 'ad', 'b': '34'}
# print(d)
# for i in d:
#     print(i + '=>' + d[i])
with open('data.json', 'a') as f:
    json.dump(d, f)
with open('data.json', 'r') as f:
    print(json.loads(f))