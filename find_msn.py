import os, json, csv
from lxml import etree
import pandas
# dir_list = os.listdir(os.getcwd())
file_path = os.getcwd() + os.sep + '2019-03-20' 
print(file_path)
qq_file = open('qq_collect.csv', 'w', newline='')
qq_writer = csv.writer(qq_file)
qq_writer.writerow(['id', 'title','qq'])

tg_file = open('tg_collect.csv', 'w', newline='')
tg_writer = csv.writer(tg_file)
tg_writer.writerow(['id', 'title','tg'])

for file in os.listdir(file_path):
    # print(file)
    response = etree.parse(file_path + os.sep + file, etree.HTMLParser())
    qq = response.xpath('//*[contains(text(), "qq")]/text()')
    tg = response.xpath('//*[contains(text(), "tg")]/text()')
    title = response.xpath('//title/text()')
    if qq:
        # print(file, qq, tg)
        qq_writer.writerow([file] + title + [';'.join(qq).strip().replace('\n', '')])
    if tg:
        tg_writer.writerow([file] + title + [';'.join(tg).strip().replace('\n', '')])
qq_file.close()
tg_file.close()