import os
try:
    os.system("torsocks scrapy crawl spider_10001")
except:
    print("sonething is wrong!")