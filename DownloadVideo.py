from pytube import YouTube
import pandas as pd
import re
import ffmpeg 
import os


def DowloadYoutubeVideo(url):
    need_url=[url.split('&')[0] if url.find('&') else url][0]

    yt = YouTube(need_url)

    # 將大量字串DataFrame表格化
    youtubefiles=yt.streams.all()
    file=[]
    for i in youtubefiles:
        file.append(str(i).split('"'))
    df=pd.DataFrame(file)

    # 找畫質最好的itag號
    res=df[df[3]=='video/mp4']
    int_list = list(map(int,[re.findall(r'\d+',file)[0] for file in res[5]]))
    mp4itag=res[res[5]==f'{max(int_list)}p'].iat[0,1]

    # 找音質最好的itag號
    res=df[df[3]=='audio/mp4']
    int_list = list(map(int,[re.findall(r'\d+',file)[0] for file in res[5]]))
    audioitag=res[res[5]==f'{max(int_list)}kbps'].iat[0,1]

    # 影音getitag
    video =yt.streams.get_by_itag(mp4itag)
    audio =yt.streams.get_by_itag(audioitag)

    # 影音下載合併
    video.download("./", "video_download.mp4")
    audio.download("./", "audio_download.mp4")
    video_stream = ffmpeg.input('video_download.mp4') 
    audio_stream = ffmpeg.input('audio_download.mp4')

    # 名字裡不能有/\符號
    name=yt.title.strip('/')
    name=re.sub('\/','',name)

    ffmpeg.output(audio_stream,video_stream, f'{name}.mp4').run()

    # 删除音频和视频
    os.remove("video_download.mp4")
    os.remove("audio_download.mp4")

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
        DowloadYoutubeVideo(url)
    except:
        print('url error')