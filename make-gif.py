import os, sys
import yaml
from moviepy.editor import *

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

class ControlDefine:
    def __init__(self,
        capturesdir = "D:\\time-lapse\\output",
        targetdir = "D:\\time-lapse\\output",
        targetfile = "timelapse.gif",
        mergestep = 1):
        self.capturesdir = capturesdir                # 延时图像存储位置
        self.targetdir = targetdir                    # gif输出位置
        self.targetfile = targetfile                  # gif输出文件名
        self.mergestep = mergestep                    # 延时输出速度，默认为1，即输出gif的延时间隔与抓取间隔一致,2为抓取间隔的1倍

def loadConfig(configfile, withprint = False):
    if os.path.exists(configfile):
        configdata = yaml.load(open(configfile, 'r'))

        capturesdir = configdata['capturesdir']
        targetdir = configdata['targetdir']
        targetfile = configdata['targetfile']
        mergestep = configdata['mergestep']

        configobject = ControlDefine(capturesdir, targetdir, targetfile, mergestep)
    else:
        configobject = ControlDefine()

    if withprint:
        print(configobject.capturesdir, configobject.targetdir, configobject.targetfile, configobject.mergestep)

    return configobject

print("Starting make movies to gif")

control = loadConfig("make-gif.yml", True)

def mergeCapture(targetdir, targetvideo, srcdir, speed):
    # output目录不存在则创建
    if not(os.path.exists(targetdir)):
        os.mkdir(targetdir)

    filepath = targetdir + "/" + targetvideo

    lsdir = os.listdir(srcdir)

    files = [i for i in lsdir if os.path.isfile(os.path.join(srcdir,i))]
    files.sort(reverse=False)
    if files:
        for item in files:
            if item.endswith('.mp4'):
                print(item)
                gifitem = item[:-4] + ".gif"
                item = os.path.join(srcdir, item)
                # 512 * 384 标清 1920, 1080  960-+256=714,1216, 540-+192=348,732
                source = VideoFileClip(item)
                duration = source.duration
                print(duration)
                print(source.get_frame(0).shape)

                x = 1920 / 2 - 1
                y = 1080 / 2 - 1

                # 向右平移256像素
                x += 128
                y -= 0 # 192, 0

                x1 = int(x - 512 / 2)
                x2 = int(x + 512 / 2)
                y1 = int(y - 384 / 2)
                y2 = int(y + 384 / 2)

                print(x1, x2, y1, y2)

                target = VideoClip(lambda t: source.get_frame(t)[y1:y2][:,x1:x2], duration=duration).set_fps(source.fps)
                targetpath = os.path.join(targetdir, gifitem)
                target.write_gif(targetpath,fps=(source.fps * 0.125))
                target.close()

mergeCapture(control.targetdir, control.targetfile, control.capturesdir, control.mergestep)
