from scrapy import cmdline

cmdline.execute('scrapy crawl qa_data -o tset.csv'.split())