import requests
from bs4 import BeautifulSoup
import os

def DowloadEynyVideo(url):
    resp=requests.post(url)
    soup=BeautifulSoup(resp.text,'lxml')
    video=soup.find('video')
    source=video.find_all('source')
    src=source[0].get('src')
    return src

print('請輸入網址(-1:exit)')

urls=[]
while True:
    url=input('')
    if url=='-1':
        break
    elif 'http://video.eyny.com/'  in url:
        urls.append(url)
    else:
        print('error')
        
        
for url in urls:
    try:
        os.system('you-get '+DowloadEynyVideo(url))
    except:
        print('error')