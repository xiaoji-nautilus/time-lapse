import os, sys
import cv2
import shutil
import yaml

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

class ControlDefine:
    def __init__(self,
        capturesdir = "D:\\time-lapse\\tmp",
        targetdir = "D:\\time-lapse\\output",
        targetfile = "timelapse.mp4",
        mergestep = 1):
        self.capturesdir = capturesdir                # 延时图像存储位置
        self.targetdir = targetdir                    # 视频输出位置
        self.targetfile = targetfile                  # 视频输出文件名
        self.mergestep = mergestep                    # 延时输出速度，默认为1，即输出视频的延时间隔与抓取间隔一致,2为抓取间隔的1倍

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

print("Starting merge captures to video")

control = loadConfig("merge-captures.yml", True)

def mergeCapture(targetdir, targetvideo, srcdir, speed):
    # output目录不存在则创建
    if not(os.path.exists(targetdir)):
        os.mkdir(targetdir)

    filepath = targetdir + "/" + targetvideo
    size = (1920, 1080)
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    #fourccx264 = cv2.VideoWriter_fourcc('X','2','6','4')

    if os.path.exists(filepath):
        print("video file exits")
        backup = targetdir + "/backup_" + targetvideo
        shutil.copyfile(filepath, backup)
        cap = cv2.VideoCapture(backup)
        isOpened = cap.isOpened

        target = cv2.VideoWriter(filepath, fourcc, 24, size)

        if isOpened:
            success, frame = cap.read()
            while success:  # 循环直到没有帧了
                target.write(frame)
                success, frame = cap.read()
    else:
        target = cv2.VideoWriter(filepath, fourcc, 24, size)

    lsdir = os.listdir(srcdir)

    files = [i for i in lsdir if os.path.isfile(os.path.join(srcdir,i))]
    files.sort(reverse=False)
    if files:
        i = 0
        for item in files:
            i = i + 1
            if i % speed == 0 and item.endswith('.jpg'):
                print(item)
                item = os.path.join(srcdir, item)
                img = cv2.imread(item)
                target.write(img)
                #os.remove(item)
        target.release()

mergeCapture(control.targetdir, control.targetfile, control.capturesdir, control.mergestep)
