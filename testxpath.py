from lxml import etree

# f = open('temp').readlines()
# f.xpath()
# print(f)
# f.close()
response = etree.parse('temp', etree.HTMLParser())
title = response.xpath('//title/text()')
print(title)
autim = response.xpath('//*[@name="autim"]/@value')[0]
print(autim)
sid = response.xpath('//*[@name="sid"]/@value')[0]
print(sid)