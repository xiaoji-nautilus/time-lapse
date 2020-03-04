import os, sys
from datetime import datetime
import cv2
import yaml
import threading

class ControlDefine:
    def __init__(self,
        shotfrom = "2020/02/25 08:00:00",
        shotto = "2020/02/25 19:00:00",
        current = "2020/02/25 14:10:00",
        captureGap = 8,
        srcdir = "//192.168.0.1/XiaoMi/xiaomi_camera_videos/04cf8c6b0439"):
        self.shotfrom = shotfrom                        # 开始时间
        self.fromtime = datetime.strptime(self.shotfrom, "%Y/%m/%d %H:%M:%S")
        self.shotto = shotto                            # 结束时间
        self.totime = datetime.strptime(self.shotto, "%Y/%m/%d %H:%M:%S")
        self.current = current                          # 处理中断时间
        self.currenttime = datetime.strptime(self.current, "%Y/%m/%d %H:%M:%S")
        self.captureGap = captureGap                    # 延迟拍摄间隔时间(秒)
        self.srcdir = srcdir                            # 米家摄像机视频记录NAS存放位置

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

print(dirname, filename)

def loadConfig(configfile, withprint = False):
    if os.path.exists(configfile):
        configdata = yaml.load(open(configfile, 'r'))

        shotfrom = configdata['shotfrom']
        shotto = configdata['shotto']
        current = configdata['current']
        captureGap = configdata['captureGap']
        srcdir = configdata['srcdir']

        configobject = ControlDefine(shotfrom, shotto, current, captureGap, srcdir)
    else:
        configobject = ControlDefine()

    if withprint:
        print(configobject.shotfrom, configobject.shotto, configobject.current, configobject.captureGap, configobject.srcdir)

    return configobject

def saveConfig(configfile, configobject):
    configdata = {
        "shotfrom": configobject.shotfrom,
        "shotto": configobject.shotto,
        "current": configobject.current,
        "captureGap": configobject.captureGap,
        "srcdir": configobject.srcdir
    }

    with open(configfile, 'w') as f:
        yaml.dump(configdata, f)

    return True

def getUnixTimestamp(filename):
    filename_withoutext = filename.split('.')[0]
    return filename_withoutext.split('_')[1]

print("Starting capture images from video")

control = loadConfig("time-lapse.yml", True)

def capture(videofilename, videofile):
    unixtime = getUnixTimestamp(videofilename)
    cap = cv2.VideoCapture(videofile)

    isOpened = cap.isOpened

    fcs = cap.get(cv2.CAP_PROP_FRAME_COUNT)     # 帧数
    fps = cap.get(cv2.CAP_PROP_FPS)             # 帧率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(videofilename)

    i = 0

    while(isOpened):
        i += 1

        if i > fcs:     # 所有帧读完退出
            cap.release()
            break;

        (flag, frame) = cap.read() # 读取每一张 flag frame

        if i % int(control.captureGap * fps) == 1:
            fileName = dirname + "/tmp/" + unixtime + "_" + str(i).rjust(4, '0') + ".jpg"
            print(fileName)
            if flag == True:
                cv2.imwrite(fileName,frame,[cv2.IMWRITE_JPEG_QUALITY,100])

    # 当前处理完成的时间保存到配置文件
    filetime = datetime.fromtimestamp(int(unixtime))
    currenttime = filetime.strftime("%Y/%m/%d %H:%M:00")
    if control.current < currenttime:
        control.current = currenttime
        saveConfig("time-lapse.yml", control)

def dirfilter(dirname):
    dirtime = datetime.strptime(dirname, "%Y%m%d%H")
    currenttime = datetime.strptime(control.currenttime.strftime("%Y/%m/%d %H:00:00"), "%Y/%m/%d %H:%M:%S")

    delta = dirtime - currenttime

    if delta.days >= 0:
        return True
    else:
        return False

def filefilter(filename):
    unix = getUnixTimestamp(filename)
    filetime = datetime.fromtimestamp(int(unix))
    currenttime = datetime.strptime(control.currenttime.strftime("%Y/%m/%d %H:%M:00"), "%Y/%m/%d %H:%M:%S")

    delta = filetime - currenttime

    if delta.days >= 0:
        return True
    else:
        return False

# 多线程提取图像，加快处理速度
class captureThread(threading.Thread):
    def __init__(self, filename, filepath):
        threading.Thread.__init__(self)
        self.filename = filename
        self.filepath = filepath
    def run(self):
        print ("开始线程: " + self.filename)
        capture(self.filename, self.filepath)
        print ("退出线程: " + self.filename)

captureThreads = [None, None, None, None]

def walkdir(path, filterdir, fitlerfile):
    lsdir = os.listdir(path)

    dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
    dirs.sort(reverse=False)
    if dirs:
        for i in dirs:
            if filterdir(i):
                print(i)
                walkdir(os.path.join(path, i), filterdir, fitlerfile)

    files = [i for i in lsdir if os.path.isfile(os.path.join(path,i))]
    files.sort(reverse=False)
    if files:
        for i in files:
            if fitlerfile(i):
                runningTreads = 0

                for index in range(len(captureThreads)):
                    thread = captureThreads[index]

                    if thread is None or not thread.is_alive():
                        thread = captureThread(i, os.path.join(path, i))
                        captureThreads[index] = thread
                        thread.start()
                        runningTreads += 1
                        break
                    else:
                        runningTreads += 1

                if runningTreads == len(captureThreads):
                    for thread in captureThreads:
                        thread.join()

# tmp目录不存在则创建
if not(os.path.exists(dirname + "/tmp/")):
    os.mkdir(dirname + "/tmp/")

walkdir(control.srcdir, filterdir = dirfilter, fitlerfile = filefilter)
