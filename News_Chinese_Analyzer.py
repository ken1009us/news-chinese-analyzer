import requests
from bs4 import BeautifulSoup
import jieba
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt 

from matplotlib.font_manager import _rebuild
_rebuild()

plt.rcParams['font.sans-serif'] = 'SimHei'


header={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

print('-'*70)

def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

def GenKeywords(s, threshold):
    result = jieba.cut(s, cut_all = False)  #精準模式
    dictWord = {}

    for word in result:
        if word in dictWord:
            dictWord[word] += 1
        else:
            dictWord[word] = 1

    KeywordsList = list()

    for k in dictWord:
        if len(k) > 1 and dictWord[k] >= threshold:
            Element = [dictWord[k], k]
            KeywordsList.append(Element)
    
    KeywordsList.sort()
    KeywordsDict = {}

    for i in KeywordsList:
        KeywordsDict[i[1]] = i[0]
    return KeywordsDict

def GetNewsContent(WebAddr):
    html = requests.get(WebAddr, headers = header)
    WebSoup = BeautifulSoup(html.text, 'html.parser')

    NewsBody = ''
    WebItems = WebSoup.select('.article-body')
    for item in WebItems:
        result = item.find_all('p')
        for i in result:
            if i.text !='':
                NewsBody += i.text
    return NewsBody

def ListKeywords(KeywordsDict):
    for k in KeywordsDict:
        if len(k) > 1 and KeywordsDict[k] >= threshold:
            print(k, KeywordsDict[k])
            
            if __name__ == '__main__':
                plt.title('關鍵字出現次數', fontproperties=getChineseFont())
                x = k
                y = KeywordsDict[k]
                plt.ylabel('次數', fontproperties = getChineseFont())
                plt.xlabel('關鍵字', fontproperties = getChineseFont())
                plt.bar(x, y)

threshold = 4
urlPrefix = 'https://www.chinatimes.com/'
urlSuffix = '?chdtv'

url = 'https://www.chinatimes.com/realtimenews/?chdtv'
r = requests.get(url, headers = header)

soup = BeautifulSoup(r.text, 'html.parser')

items = soup.select('.title')

for item in items[0:5]:
    
    addr = item.find('a')
    if (addr.get('href').find('http')==-1):
        FullAddr = urlPrefix + addr.get('href')[1:len(addr.get('href'))] + urlSuffix
    else:
        FullAddr = addr.get('href') + urlSuffix
    
    print(FullAddr)
    print(addr.string)
    Newsbody = GetNewsContent(FullAddr)
    KeywordsDict = GenKeywords(Newsbody, threshold)
    ListKeywords(KeywordsDict)
    print('-'*70)

