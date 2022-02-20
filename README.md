# 环境配置

Install anaconda navigator: [Official website](https://www.anaconda.com/products/individual)

Install Pycharm: [Official website](https://www.jetbrains.com/pycharm/download/#section=windows)

 

### Download alphapose

alphapose can be retrieved from [here](https://github.com/MVIG-SJTU/AlphaPose/)

Windows 系统：

- open anaconda

- select Powershell prompt

paste and run the following codes

```
conda create -n alphapose python=3.6 -y
conda activate alphapose
conda install pytorch==1.1.0 torchvision==0.3.0
git clone https://github.com/MVIG-SJTU/AlphaPose.git
cd AlphaPose
export PATH=/usr/local/cuda/bin/:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:$LD_LIBRARY_PATH
python -m pip install cython
sudo apt-get install libyaml-dev
python setup.py build develop
conda install pyqt
```

Download object recognition model "yolov3-spp.weights"，move it to `detector/yolo/data`

[Baidu netdisk](https://pan.baidu.com/s/1Zb2REEIk8tcahDa8KacPNA)

Download pose recognition model, move it to `pretrained_models` 

[Baidu netdisk](https://pan.baidu.com/s/1lvzMhoYgS6o6n8lVDx3GtQ)

Download tracking model，move to `AlphaPose/detector/tracker/data/`

[Baidu netdisk](https://pan.baidu.com/s/1Ifgn0Y_JZE65_qSrQM2l-Q)

 

### Use anaconda environment in pycharm

打开pycharm，新建项目，在窗口中选择这里

![img](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/docs/clip_image002.png)

![img](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/docs/clip_image004.png)

![img](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/docs/clip_image006.png)

在根目录中找到一个叫conda或者Anaconda的文件夹，选择envs/Alphapose/python.exe

然后点击确定-确定-创建，完成环境搭建。

### Run



