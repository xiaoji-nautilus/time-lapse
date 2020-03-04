import os, sys
import yaml
from moviepy.editor import *

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

class ControlDefine:
    def __init__(self,
        audiofile = "D:\\time-lapse\\audios\\The sky city.mp3",
        videofile = "D:\\time-lapse\\output\\timelapse.mp4",
        targetdir = "D:\\time-lapse\\output",
        targetfile = "timelapse-audio.mp4"):
        self.audiofile = audiofile                # 合成音频文件
        self.videofile = videofile                # 合成视频文件
        self.targetdir = targetdir                # 视频输出目录
        self.targetfile = targetfile              # 视频输出文件名

def loadConfig(configfile, withprint = False):
    if os.path.exists(configfile):
        configdata = yaml.load(open(configfile, 'r'))

        audiofile = configdata['audiofile']
        videofile = configdata['videofile']
        targetdir = configdata['targetdir']
        targetfile = configdata['targetfile']

        configobject = ControlDefine(audiofile, videofile, targetdir, targetfile)
    else:
        configobject = ControlDefine()

    if withprint:
        print(configobject.audiofile, configobject.videofile, configobject.targetdir, configobject.targetfile)

    return configobject

print("Starting merge audios to video")

control = loadConfig("merge-audio.yml", True)

def mergeAudio(audiofile, videofile, targetdir, targetfile):
    audio = AudioFileClip(audiofile)
    video = VideoFileClip(videofile)

    # 音频时长确保和视频长度一致
    aud = audio.duration
    vid = video.duration

    if aud > vid:       # 音频长度超过视频长度
        print('音频长度超过视频长度')
        fitableAudio = audio.cutout(0, vid)
    elif aud < vid:     # 音频长度小于视频长度
        print('音频长度小于视频长度')
        count = vid // aud
        gap = vid % aud

        audios = [audio] * count
        appendaudio = audio.cutout(0, gap)
        audios.append(appendaudio)
        fitableAudio = CompositeAudioClip(audios)
    else:               # 音视频长度一致
        print('音视频长度一致')
        fitableAudio = audio

    mergedfile = targetdir + "/" + targetfile

    mergedVideo = CompositeVideoClip([video]).set_audio(fitableAudio)
    mergedVideo.write_videofile(mergedfile, codec='libx264', fps=24)

mergeAudio(control.audiofile, control.videofile, control.targetdir, control.targetfile)
