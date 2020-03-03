# 使用监控摄像头制作延迟拍摄视频
一直想把开花的过程拍摄下来，使用相机延迟拍摄功能的困难在于，不知道花儿什么时候开，而相机存储卡容量有限。
2020年的2019-nCov疫情让我有时间来琢磨这件事情
我手上有一个米家1080P智能**摄像机**（一般用于监控用途，130度广角，支持网络存储监控录像），一个小米路由器（带1T硬盘存储，支持**NAS**<sup>[注1](#note1)</sup>），一个**放大镜**（**可选**），一台Windows**电脑**。还有两盆即将开花的**橡皮花**。

于是我拍摄并制作了下面的视频

[![延时摄影视频](https://pluto.guobaa.com/cal/img/time-lapse-sample.jpg)](https://pluto.guobaa.com/cal/img/follower6mix.mp4)

有朋友看到了这段视频，非常喜欢，于是询问制作过程和制作难度
下面便是我的制作教程，希望对有兴趣延迟拍摄的朋友们提供帮助


* [准备](#准备)
  * [1、前提](#1、前提)
  * [2、路由器/NAS网络存储准备](#2、路由器/NAS网络存储准备)
  * [3、摄像机准备](#3、摄像机准备)
  * [4、电脑准备](#4、电脑准备)
* [拍摄视频](#拍摄视频)
* [视频处理](#视频处理)
  * [1、视频处理前准备](#1、视频处理前准备)
    * [安装Python](#安装Python)
    * [安装pip](#安装pip)
    * [使用pip安装其它组件](#使用pip安装其它组件)
    * [下载程序](#下载程序)
  * [2、运行延时图像抓取程序](#2、运行延时图像抓取程序)
    * [设置运行参数](#设置运行参数)
    * [运行](#运行)
  * [3、运行视频合并程序](#3、运行视频合并程序)
    * [设置运行参数](#设置运行参数)
    * [运行](#运行)
  * [4、给视频增加音乐](#4、给视频增加音乐)
    * [安装组件](#安装组件)
    * [设置运行参数](#设置运行参数)
    * [运行](#运行)
  * [5、剪辑视频](#5、剪辑视频)
* [写在最后](#写在最后)
* [附录](#附录)



<h2 id="准备">准备</h2>

开始拍摄前需要将摄像头、NAS和电脑进行设置，确保摄像头记录下来的视频可以自动且连续的保存到NAS上，并确保电脑可以访问到视频在NAS上的存放位置。

### 1、前提

网络摄像机已经连上网络，电脑也连上网络并可以通过Windows资源管理器访问NAS网络硬盘。设置方法参考相关硬件的使用说明书。

### 2、路由器/NAS网络存储准备

我这次使用了小米路由器自带的NAS网络存储，所以，在小米路由器的网页管理界面上进行如下设置就可以了

![image-20200302101831199](https://pluto.guobaa.com/cal/img/router-nas-controller.png)

如上图所示，我们找到已经连接上网络的米家智能摄像机，然后，把它的全盘访问权限加上，设置就完成了

### 3、摄像机准备

我这次使用的是米家智能摄像机（1080P），手机上打开摄像机设置的米家App，在主截面中点击右上角的**...** ，弹出如第二张截图所示的菜单，选择**存储管理** ，如第三张截图所示，进入存储管理页面，选择**NAS网络存储**

为了防止网络异常无法完成存储，导致视频丢失，我同时使用了存储卡（16G/32G的都可以），一般摄像机都不带，需要自己准备，可以使用淘汰下来的手机扩展存储卡（如果有的话）

<img src="https://pluto.guobaa.com/cal/img/camera-settings-01.jpg" alt="camera-settings-01" style="zoom:20%;" /><img src="https://pluto.guobaa.com/cal/img/camera-settings-02.jpg" alt="camera-settings-02" style="zoom:20%;" /><img src="https://pluto.guobaa.com/cal/img/camera-settings-03.jpg" alt="camera-settings-03" style="zoom:20%;" />

接下来设置NAS网络存储，首先如下第一张图所示，打开视频存储

视频存储时长设置根据自己NAS的可用存储空间大小选择；上传时间间隔我选择了实时，这样会对其它设备使用WIFI产生一定影响

点击存储器设置，进入如下第二张图所示，需要先选择存储器，设置好存储器之后，选择存储视频的目录

<img src="https://pluto.guobaa.com/cal/img/camera-settings-04.jpg" alt="camera-settings-04" style="zoom:25%;" /><img src="https://pluto.guobaa.com/cal/img/camera-settings-05.jpg" alt="camera-settings-05" style="zoom:25%;" />

进入修改存储器界面，第一次会通过网络自动扫描可以使用的NAS网络存储器，让你选择，有的存储器设置了访问用户和密码，可以在如下第一张图所示的用户名和密码框中输入，点完成后验证是否可以读写访问（我的网络存储器设置了匿名访问，并通过路由器直接把全盘访问权限付给了这个摄像机，所以不需要设置用户名密码）

NAS网络存储器设置好了之后，需要选择一个存储位置，从上面的存储器设置画面选择修改存储目录，进入如下第二张图所示，App将自动扫描可用目录，点击目录名称进行选择

<img src="https://pluto.guobaa.com/cal/img/camera-settings-06.jpg" alt="camera-settings-06" style="zoom:25%;" /><img src="https://pluto.guobaa.com/cal/img/camera-settings-07.jpg" alt="camera-settings-07" style="zoom:25%;" />

以上所有设置完成之后，摄像机的设置就完成了

### 4、电脑准备

电脑我使用的是一台老的一体机，4G内存，集成显卡，CPU是i7-4510U 2.60GHz，安装了Windows 7操作系统（苹果MacOS也可以，只是我手边没有苹果电脑没法制作教程），因为需要比较大的存储空间用于缓存，通过USB接了一块250G的移动硬盘。

电脑连接上网络之后，打开Windows的资源管理器（快捷键 Win + E），如下图所示，在地址栏中输入NAS网络硬盘的访问地址（一般是这样的格式 \\192.168.0.1）

看到NAS上的目录之后，查找一下摄像头存储在NAS上的位置，后面通过程序对视频进行处理的时候需要使用到（我的位置在\\192.168.0.1\XiaoMi\xiaomi_camera_videos\04cf8c6b0439下面）

![image-20200302101146292](https://pluto.guobaa.com/cal/img/nas-storage.png)

找到视频存储位置，并确认视频可以正常存储之后，电脑的设置就完成了

## 拍摄视频

将摄像头放置到最佳拍摄位置，需要考虑长时间拍摄的情况下，电源不会被意外踢断等情况发生；

另外需要考虑上午、中午和下午的阳光不会造成光线直射，导致部分时间无法清洗的看清被拍摄的物体，一般选择角度和窗户平行的位置。

如果需要获得比较好的晚上拍摄效果，需要考虑使用辅助光源，一般室内光源的光线无法满足拍摄的需要，我这次没有考虑晚上拍摄，所以没有使用辅助光源。

## 视频处理

为了做到延时摄影<sup>[注2](#note2)</sup>效果，我们需要把摄像机记录下来的连续的视频，按照一定的时间间隔（我设置了时间间隔为24秒），取出相应时间点的图像，以图片的形式存储到本地磁盘上；

然后，将上面取出的图像，按照时间顺序，合并到一个视频文件中，合并后的视频文件没有音轨；

最后，使用视频剪辑软件，加上音轨或者字幕等内容之后，导出最终的视频文件。

### 1、视频处理前准备

为了快速完成这个视频处理程序，我使用了Python语言，原因很简单，因为它是脚本语言，写完代码不需要编译，直接可以运行；另外也是最主要的原因，它的图像和视频处理模块很成熟，目前流行的人工智能所使用的视觉功能学习和实现都是使用它来完成的；所以，Python是处理我们需要的功能的最佳选择。

#### 安装Python

如果你的电脑上已经安装了Python，就可以跳过这一步。

访问Python官网（https://www.python.org/），下载最新的安装程序（https://www.python.org/downloads/release/python-382/）

[Windows x86-64 executable installer](https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe)
[macOS 64-bit installer](https://www.python.org/ftp/python/3.8.2/python-3.8.2-macosx10.9.pkg)

具体安装过程略... (如果有疑问的地方，可以单独联系我)

安装完成之后，确认一下是否安装成功，可以使用了

打开命令行窗口（快捷键 Win + R），点确定按钮打开

![image-20200302155856742](https://pluto.guobaa.com/cal/img/win+r.png)

打开后，获得如下窗口

![image-20200302160031387](https://pluto.guobaa.com/cal/img/win-cmd.png)

输入py，然后回车，获得如下内容表示安装成功了

![image-20200302160122830](https://pluto.guobaa.com/cal/img/win-cmd-py.png)

输入Ctrl + Z，然后回车，可以退出上述功能，返回命令行窗口



#### 安装pip

下载[get-pip.py](https://pluto.guobaa.com/cal/img/get-pip.py)，通过脚本安装pip

首先在移动硬盘上创建一个目录（我的移动硬盘盘符是D盘，目录命名为time-lapse），然后把下载下来的get-pip.py文件放到该目录下面

打开命令行窗口，执行以下命令，进入到time-lapse目录，然后，通过get-pip.py脚本进行安装，如果安装失败，可以重新输入最后以行命令，再次执行安装程序，直到安装成功为止

```CMD
> D:
> cd time-lapse
> py get-pip.py --user
```

安装成功后，输入pip命令，可以获得以下内容，就可以确认安装成功了

![image-20200302162257522](https://pluto.guobaa.com/cal/img/win-cmd-pip.png)



#### 使用pip安装其它组件

通过pip我们需要安装三个组件（opencv-python、pytest-shutil、pyyaml），用于实现我们的功能

在命令行窗口中，进入time-lapse目录，然后分别执行以下三个命令

```CMD
pip install opencv-python
pip install pytest-shutil
pip install pyyaml
```

以上命令可以重复执行，直到没有出现红色的错误为止，就说明安装成功了



#### 下载程序

通过github将[time-lapse](https://github.com/xiaoji-nautilus/time-lapse)源代码下载到本地，或者直接下载[time-lapse.zip](https://pluto.guobaa.com/cal/img/time-lapse.zip)文件到本地，然后文件解压到移动硬盘（我的盘符是D盘），覆盖刚才创建的time-papse目录，解压后如下图所示

![image-20200302164238258](https://pluto.guobaa.com/cal/img/time-lapse-storage.png)




#### 2、运行延时图像抓取程序


##### 设置运行参数

使用文本编辑器（记事本、Notepad++或者Atom等）打开time-lapse.yml文件，编辑参数

![image-20200302165029097](https://pluto.guobaa.com/cal/img/time-lapse-params.png)

[^srcdir]: 视频文件目录，需要指向NAS网络存储视频存储位置
[^captureGap]: 延时间隔（单位：秒），24表示间隔24秒，延时间隔不能大于60秒，需要更大的延时间隔，可以通过合并视频的程序控制
[^shotfrom]: 抓取开始时间，时间精度可以控制到分钟，秒设置无效
[^shotto]: 抓取截止时间，暂时无效
[^current]: 当前处理时间，默认和开始时间设置为一致，抓取过程中会更新此参数，用于重复执行的时候从上次抓取位置开始抓取




##### 运行
运行参数设置好之后，在命令行窗口执行以下命令执行延时图像抓取程序

```CMD
> py time-lapse.py
```

运行显示如下图所示

![image-20200302172036679](https://pluto.guobaa.com/cal/img/win-cmd-time-lapse.png)

当所有视频都被处理完之后，该程序将结束并退出

有新的视频存储上来之后，可以重新执行上面的命令，程序将从上次结束的位置开始处理新增加的视频

所有的延时图像将被存储到tmp目录，如下图所示

![image-20200302172653276](https://pluto.guobaa.com/cal/img/time-lapse-storage-tmp.png)

处理速度大约是1小时可以处理2小时40分钟的视频



#### 3、运行视频合并程序

视频抓取处理完成之后，或者是需要的时间段已经抓取完成之后，就可以运行视频合并程序，将处理好的图像合并成视频。

##### 设置运行参数

使用文本编辑器（记事本、Notepad++或者Atom等）打开merge-captures.yml文件，编辑参数

![image-20200302200858362](https://pluto.guobaa.com/cal/img/merge-captures-params.png)

[^capturesdir]: 抓取图像文件存储目录
[^targetdir]: 合并后视频文件输出目录
[^targetfile]: 合并后视频文件存储名称
[^mergestep]: 合并视频速度，默认为1，表示和抓取的速度一致，设置为2，则表示抓取速度的1倍合并成视频


##### 运行

运行参数设置好之后，在命令行窗口执行以下命令执行视频合并程序

```CMD
> py merge-captures.py
```

运行显示如下图所示



![image-20200302195633191](https://pluto.guobaa.com/cal/img/win-cmd-merge-captures.png)

当所有抓取的图像都被处理完之后，该程序将结束并退出

调整运行参数或者有新的抓取图像，需要重新处理，建议每次运行修改一下输出文件名，否则，将会在上次输出的视频后面继续合并图片，因为抓取图片目录中的图片存在上次已经合并过的图片，可能会造成重复。

合并后的视频文件被存放到output目录下，如下图所示

![image-20200302202442483](https://pluto.guobaa.com/cal/img/time-lapse-storage-output.png)

处理速度大约是每分钟可以合并312张图片，或者是每分钟视频大约需要5分钟以上的时间合并处理。

#### 4、给视频增加音乐

##### 安装组件

给视频添加音乐，需要增加一个组件（moviepy）
在命令行窗口中，进入time-lapse目录，然后执行以下命令

```CMD
> pip install moviepy
```

以上命令可以重复执行，直到没有出现红色的错误为止，就说明安装成功了

##### 设置运行参数

使用文本编辑器（记事本、Notepad++或者Atom等）打开merge-audio.yml文件，编辑参数

![image-20200303104002949](https://pluto.guobaa.com/cal/img/merge-audio-params.png)


[^audiofile]: 合成音频文件
[^videofile]: 合成视频文件
[^targetdir]: 视频输出目录
[^targetfile]: 视频输出文件名

##### 运行

运行参数设置好之后，在命令行窗口执行以下命令执行视频和音乐合并程序

```CMD
> py merge-audio.py
```

运行显示如下图所示

![image-20200303122424582](https://pluto.guobaa.com/cal/img/win-cmd-merge-audio.png)

#### 5、剪辑视频

合并完成的视频只有视频轨，没有音频轨，所以播放的时候没有声音，或者希望把片头和片尾，以及字幕等效果加入进去，你就需要使用视频剪辑工具来帮你完成后续的工作了。

我使用了开放源代码，免费的Shotcut视频剪辑软件，也可以使用其它软件，Windows 10自带视频剪辑工具。

具体怎么剪辑视频，这里就不介绍了，可以查阅相关的视频剪辑软件的帮助说明。



## 写在最后

1、后面会考虑把视频图像抓取和合并视频的功能，放到树莓派(Raspberry Pi)中，这样就不需要将电脑一直开着来处理视频了

2、使用MacOS的朋友如果希望使用这个程序来处理，可以联系我，并帮助我完成MacOS的教程

3、欢迎大家把制作出来的视频分享出来，并告诉我地址，我会单独开一页来汇总大家的视频



## 附录

<a name="note1">注1</a>: NAS（Network Attached Storage：网络附属存储）按字面简单说就是连接在网络上，具备资料存储功能的装置，因此也称为“[网络存储器](https://baike.baidu.com/item/网络存储器/9485387)”。

<a name="note2">注2</a>: 延时摄影又称“[定时摄影](https://baike.baidu.com/item/定时摄影)”或“延时摄影”，[特殊摄影](https://baike.baidu.com/item/特殊摄影/10402998)方法之一。延时摄影是以一种较低的[帧率](https://baike.baidu.com/item/帧率/1052590)拍下图像或者视频，然后用正常或者较快的速率播放画面的摄影技术。利用延时控制器，每隔一定的时间间隔之后快门拍摄一次，一段时间后拍摄得到的若干张照片进行连续放映。经常在电视上看到的例子就是花朵开放，天亮过程，风起云涌。
