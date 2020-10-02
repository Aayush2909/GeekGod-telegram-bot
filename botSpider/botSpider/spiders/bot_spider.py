import scrapy
from collections import deque

class BotSpider(scrapy.Spider):
    name = "bot"
    urls = []
    
    #constructor called when started crawling
    def __init__(self, category=None, *args, **kwargs):
        super(BotSpider, self).__init__(*args, **kwargs)
        self.urls.append('https://www.geeksforgeeks.org/%s'%category)
    
    
    #request started
    def start_requests(self):
        
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    #callback url while request started
    def parse(self, response):

        with open("article.txt", "w") as f:
            para = response.css("div.entry-content *::text").getall()           #getting text contents
            q = deque()
            for p in para:
                q.append(p)

            while len(q[0].strip())==0:
                q.popleft()

            lines = 0
            while q and lines<50:
                text = q[0]
                text = text.strip()
                q.popleft()

                if len(text)==0 and len(q[0].strip())==0 and q:
                    while len(q[0].strip())==0 and q:
                        q.popleft()
                    f.write('\n')
                    lines+=1

                elif len(text)>0:
                    f.write(text+'\n')
                    lines+=1

            
            
            
