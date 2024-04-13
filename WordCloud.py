import jieba
import re
import collections
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud

import requests
from bs4 import BeautifulSoup

def get_news_content(link):
    # 發送請求獲取新聞頁面內容
    response = requests.get(link)
    # 如果請求成功
    if response.status_code == 200:
        # 解析新聞頁面內容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 找到新聞內容所在的元素
        content_element = soup.find('div', class_='article-content__paragraph')
        # 如果找到內容元素
        if content_element:
            # 獲取新聞內容並去除多餘空格和換行符
            news_content = re.sub(r'\s+', ' ', content_element.text)
            return news_content
    else:
        print(f'無法從 {link} 獲取新聞內容。狀態碼: {response.status_code}')
        return None

def scrape_udn_news(url):
    i=1
    # 發送請求獲取網頁內容
    response = requests.get(url)
    # 如果請求成功
    news_content = ''
    if response.status_code == 200:
        # 解析網頁內容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 找到所有新聞標題的容器
        news_containers = soup.find_all('div', class_='story-list__text')
        # 遍歷所有新聞容器
        for container in news_containers:
            # 獲取新聞標題
            title_element = container.find('h2')
            # 確保找到標題元素
            if title_element:
                title = title_element.text.strip()
                # 獲取新聞連結
                link = container.find('a')['href']
                # 如果連結不是完整的 URL（缺少協議部分），則添加協議部分
                if not link.startswith('http'):
                    link = 'https://udn.com' + link
                # 獲取新聞內容
                print("處理第",str(i),"則新聞")
                print("標題：",title)
                news_content += str(get_news_content(link))
                i+=1
    else:
        print(f'無法獲取網頁內容。狀態碼: {response.status_code}')
    return news_content

def jieba_sentence(url):
    # 設置繁體中文詞庫路徑
    jieba.set_dictionary("C:\\Users\\ACER\\Desktop\\WordCloud\\dict.txt.big.txt")
    
    # 呼叫爬蟲副程式
    sentence = scrape_udn_news(url)

    # 讀取停用詞表
    with open("C:\\Users\\ACER\\Desktop\\WordCloud\\stopWordList.txt", 'r', encoding="utf-8-sig") as f:
        stop = f.read().split("\n")
    
    # 使用 jieba 分詞
    breakword = jieba.cut(sentence, cut_all=False)
    words = []
    for word in breakword:
        if word not in stop:
            words.append(word)
    
    return words

# 爬取新聞的 URL
url = 'https://udn.com/news/breaknews/1'

# 進行 jieba 分詞
words = jieba_sentence(url)

# 使用 collections.Counter() 計算詞頻
diction = collections.Counter(words)

# 設置字體檔案路徑和遮罩圖片
font = "msyh.ttc"


# 生成文字雲
wordcloud1 = WordCloud(background_color="black", font_path=font)
wordcloud1.generate_from_frequencies(frequencies=diction)

# 顯示文字雲
plt.imshow(wordcloud1)
plt.axis("off")
plt.show()