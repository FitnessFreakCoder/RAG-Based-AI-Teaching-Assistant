import os
import subprocess

file = os.listdir('videos')

for f in file:
    name = f.replace('｜', '|').split('|')[0]
    print('Converting...to mp3....')
    subprocess.run(['ffmpeg', '-i', f'videos/{f}', f'audios/{name}.mp3'])
    print('Done!')
    