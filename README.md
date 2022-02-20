# Installation and user guides



### Prepare Environments

Install anaconda navigator: [Official website](https://www.anaconda.com/products/individual)

Install Pycharm: [Official website](https://www.jetbrains.com/pycharm/download/#section=windows)

Install git: [Official website](https://git-scm.com/)

### Download alphapose

Alphapose can be retrieved from [here](https://github.com/MVIG-SJTU/AlphaPose/)

Windows：

- open anaconda

- select Powershell prompt

Paste and run the following codes

```
conda create -n alphapose python=3.6 -y
conda activate alphapose
conda install pytorch==1.1.0 torchvision==0.3.0
```

Open gitCMD and run `git clone https://github.com/MVIG-SJTU/AlphaPose.git`

Run the following codes with anaconda powershell prompt

```
cd AlphaPose
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

 

### Install dependencies

We created a [requirements](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/requirements.txt) file from a tested environment. Feel free to install those dependencies with pip install or conda install.



### Use anaconda environment in pycharm

Open pycharm，create a project，then select the right interpreter from Anaconda environments by referring to the pictures below:

![img](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/docs/clip_image002.png)

![img](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/docs/clip_image004.png)

![img](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/docs/clip_image006.png)

In the root of your system driver, you can find a folder named conda or Anaconda, select `envs/Alphapose/python.exe`

Click "create" to complete environment creation.

### Run

Our codes are mainly stored in the folder pythonProject.

You may download this folder and place it right under the `\Alphapose` folder

To run the program, pls follow the following instruction:

1. make sure all the files are under `c:\users\zyh\Alphapose\`
2. activate Anaconda environment "Alphapose"
3. run python `\Alphapose\ pythonproject\main.py`

We created 2 simple bat files to help on above steps. You can run it if you find it helpful. 

`CopyToRightPath.bat` [here](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/CopyToRightPath.bat)

`DemoWithMain.bat` [here](https://github.com/Hz-sw/CTB-sedentary-detection/blob/main/DemoWithMain.bat)
