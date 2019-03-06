from lxml import etree

# f = open('temp').readlines()
# f.xpath()
# print(f)
# f.close()
response = etree.parse('temp', etree.HTMLParser())
title = response.xpath('//title/text()')
print(title)
autim = response.xpath('//*[contains(@class,"page_b1")]/text()')[-1]
print(autim)
table = response.xpath('//*[contains(@class,"m_area_a")]/tr[6]/td[2]/text()')
# for i in table:
#     print(table.xpath('/td[1]/text()'))
print(table)
# txt = response.xpath('//a[text()="打开"]/')
# print(txt)
pages = response.xpath('//button[contains(@class,"page_b2")]/text()')[0]
print(pages)
next = response.xpath('//button[contains(@class,"page_b2")]/following::a[1]/@href')
print(next)