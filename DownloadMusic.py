from pytube import YouTube
import pandas as pd
import re



def DownloadYoutubeMusic(url):
    need_url=[url.split('&')[0] if url.find('&') else url][0]
    yt = YouTube(need_url)

    a=yt.streams.all()
    file=[]
    for i in a:
        file.append(str(i).split('"'))
    df=pd.DataFrame(file)
    res=df[df[3]=='audio/mp4']
    int_list = list(map(int,[re.findall(r'\d+',file)[0] for file in res[5]]))
    audioitag=res[res[5]==f'{max(int_list)}kbps'].iat[0,1]

    audio =yt.streams.get_by_itag(audioitag)

    name=yt.title.strip('/')
    name=re.sub('\/','',name)

    audio.download("./", f"{name}.mp3")

    print(f'finish:{name}')


print('請輸入網址(-1:exit)')

urls=[]
while True:
    url=input('')
    if url=='-1':
        break
    elif 'https://www.youtube.com/'  in url:
        urls.append(url)
    else:
        print('error')
        
        
for url in urls:
    try:
        DownloadYoutubeMusic(url)
    except:
        print('error url')