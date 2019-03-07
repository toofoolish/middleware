from lxml import etree
import json
import re
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
time = response.xpath('//dd[contains(@class, "profile-joined")]/text()')[0]
print(time)
patten = re.compile('[0-9]+')
# reg = '' += i for i in patten.findall(time)
reg = ''.join(patten.findall(time))
print(reg + '00')

time = response.xpath('//p[contains(@class, "author")]/text()')[-1]
print(time)
yy = time[:4]
mm = time.split('-')[1][:-1]
if len(mm) == 1:
    mm = '0' + mm
dd = time.split('-')[-1][:2]
tt = time.split(':')[0][-2:]
ff = time.split(':')[1].rstrip()
print(yy+mm+dd+tt+ff+'00')