from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap

from UISedentaryDetection3 import Ui_MainWindow
import cv2
import os
import sys
import json
import math
import time
import threading


def from_camera_get_image(output_path):
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        cv2.imwrite(output_path + "0" + ".jpg", frame)

    else:
        print("Camera is not found")
        return True


def from_video_get_image(path, output_path, skip_frame=20):
    """
    从视频中截图，一次一张
    三个参数依次为 视频路径、图像输出路径和开始帧
    """
    cap = cv2.VideoCapture(path)
    count = 0
    frame_count = 1
    while count <= 0:  # 截图数量上限 - 1
        if cap.grab():
            frame_count += 1
        else:
            print("End of the video")
            return True
        if frame_count >= skip_frame:
            ret, frame = cap.retrieve()
            cv2.imwrite(output_path + str(count) + ".jpg", frame)
            count += 1
    cap.release()


def detect_pose():
    os.chdir('C:/Users/zyh/AlphaPose/')
    os.system("python scripts/demo_inference.py --cfg configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml --checkpoint pretrained_models/fast_res50_256x192.pth --indir tests/RawImg --save_img --outdir tests/res/ --vis_fast")


def distance(x, y):  # Calculates the distant between 2 points
    return math.sqrt((x[1] - y[1]) ** 2 + (x[0] - y[0]) ** 2)


def read_result(threshold, point_order, file_path):  # 读取 json 文件中的内容
    """
    输入阈值、关键点序号和json路径
    输出关键点坐标 [x, y]
    输入文件路径、图片名称和关键点序号来获得那个点的坐标
    """
    x = []
    f = open(file_path)
    line = f.readline()
    json_data = json.loads(line)

    for n in range(0, len(json_data)):
        y = []
        for i in range(0, len(point_order)):
            if json_data[n]["keypoints"][3 * point_order[i] + 2] >= threshold:
                y.append(json_data[n]["keypoints"][3 * point_order[i]: 3 * point_order[i] + 2])
            else:
                y.append(None)
        x.append(y)

    f.close()
    return x


def find_angle(points):  # Calculate angles with cosine rule
    """
    根据三点坐标计算夹角
    返回 ∠AOB 的值，角度制浮点数
    """
    if (points[0] is None) or (points[1] is None) or (points[2] is None):
        return None
    a = distance(points[1], points[2])
    b = distance(points[1], points[0])
    o = distance(points[0], points[2])

    try:
        alpha = math.degrees(math.acos((a * a + b * b - o * o) / (2 * a * b)))
    except ZeroDivisionError:
        print("Division by zero")
        return None
    else:
        return alpha


def stand_or_sit(conf_threshold, ang_threshold, file_path):  # stand: return False; sit: return True

    results = read_result(conf_threshold, range(0, 17), file_path)
    output = []

    for i in results:
        angleslh = find_angle([i[3], i[12], i[14]])
        angleslk = find_angle([i[11], i[13], i[15]])
        anglesrh = find_angle([i[3], i[11], i[13]])
        anglesrk = find_angle([i[12], i[14], i[16]])

        if angleslh and angleslk:  # 左腿
            suml = (angleslh + angleslk)
        elif not (angleslh and angleslk):
            suml = None
        elif angleslh:
            suml = 2 * angleslk
        else:
            suml = 2 * angleslh

        if anglesrh and anglesrk:  # 右腿
            sumr = (anglesrh + anglesrk)
        elif not (anglesrh and anglesrk):
            sumr = None
        elif angleslh:
            sumr = 2 * anglesrk
        else:
            sumr = 2 * anglesrh

        if suml and sumr:  # 平均角度
            average = (suml + sumr) / 2
        elif not (suml and sumr):
            average = None
        elif suml:
            average = suml
        else:
            average = sumr

        if average is None or average >= ang_threshold:
            output = False
        else:
            output = True

    return output


def find_box(result_path):
    """输出文件名和yolo选择框上下左右的坐标"""
    f = open(result_path)
    line = f.readline()
    f.close()
    json_data = json.loads(line)
    image_id = []
    box = []

    for i in json_data:
        image_id.append(i["image_id"])
        for j in range(len(i["box"])):
            i["box"][j] = int(i["box"][j])
        box.append(i["box"])

    return image_id, box


def save_result(path, result_path, time_input, sit):  # Label and save result with opencv2
    """
    :param path: Path of the snapshots form video
    :param result_path: Absolute path of json
    :param time_input: Sedentary time
    :param sit: sit = True, stand = False
    :return:
    """
    font = cv2.FONT_HERSHEY_COMPLEX

    # Text preparation
    time_inputm = (time_input % 3600) // 60
    time_inputh = time_input // 3600
    text = ""
    if time_inputh > 1:
        text += str(time_inputh) + " hours "
    elif time_inputh == 1:
        text += str(time_inputh) + " hour "
    if time_inputm > 1:
        text += str(time_inputm) + " minutes"
    else:
        text += str(time_inputm) + " minute"

    # Retrieve alphapose results from json file
    filenames = os.listdir(path)
    image_id, box = find_box(result_path)

    # Draw the selection box
    if box and sit:
        for i in range(len(box)):
            left, top, right, bottom = box[i]  # 遍历所有选择框，取出上下左右
            index = filenames.index(image_id[i])  # 从现有文件名中找到识别过的照片
            fullpath = os.path.join(path, filenames[index])  # 合成完整路径
            frame = cv2.imread(fullpath)  # read image

            if frame is not None:  # 画矩形选择框
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 50, 30), 3)
                left = frame.shape[1] - right
                frame = cv2.flip(frame, 1)  # Mirror the image

                # 写字
                if time_input <= 5400:
                    cv2.putText(frame, text, (left + 7, top + 33), font, 1, (64, 128, 4), 2)  # 颜色为 BGR 格式
                else:
                    cv2.putText(frame, text, (left + 7, top + 33), font, 1, (1, 50, 210), 2)

                height = frame.shape[0]
                width = frame.shape[1]
                if height >= width:
                    scale = 500 / height
                else:
                    scale = 500 / width

                frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
                top = (500 - frame.shape[0]) // 2
                side = (500 - frame.shape[1]) // 2
                frame = cv2.copyMakeBorder(frame, top, top, side, side, cv2.BORDER_CONSTANT, value=[0, 0, 0])

                # save edited image to local
                cv2.imwrite("C:/Users/zyh/AlphaPose/tests/res/vis/labelledResult.jpg", frame)
            else:
                print("Image not found")
    else:
        fullpath = os.path.join(path, "0.jpg")
        frame = cv2.imread(fullpath)
        height = frame.shape[0]
        width = frame.shape[1]
        if height >= width:
            scale = 500 / height
        else:
            scale = 500 / width

        frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        top = (500 - frame.shape[0]) // 2
        side = (500 - frame.shape[1]) // 2
        frame = cv2.copyMakeBorder(frame, top, top, side, side, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # save edited image to local
        cv2.imwrite("C:/Users/zyh/AlphaPose/tests/res/vis/labelledResult.jpg", frame)


def wait(start):
    """Wait until 10 sec"""
    if time.time() - start <= 10:  # end of timing
        time.sleep(10 + start - time.time())  # end of timing
    else:
        print("Overtime\nduration =", time.time() - start)


def start_detection(flag_run_detection):
    global sed_time
    global start_frame


def set_flag_of_detection():
    global flag_run_detection
    global ui
    flag_run_detection = True
    ui.label_2.setText("开始久坐检测......")

    th1 = threading.Thread(target=start_detection)
    th1.start()


def clear_flag_of_detection():
    # global flag_run_detection
    # flag_run_detection = False
    # 关闭事件设为触发，关闭视频播放
    global stopEvent
    global ui
    stopEvent.set()
    ui.label_2.setText("久坐检测终止......")


def start_detection():
    global ui
    # video_path = "C:/Users/zyh/AlphaPose/tests/Videos/Internal_test.MOV"  # 视频输入路径
    img_path = "C:/Users/zyh/AlphaPose/tests/RawImg/"  # 截图输出
    yolo_output = "C:/Users/zyh/AlphaPose/tests/res/vis"  # 加好标识的图片的输出目录
    json_path = "C:/Users/zyh/AlphaPose/tests/res/alphapose-results.json"  # alphapose识别结果的输出目录
    sed_time = 0  # starting time in seconds
    start_frame = 600  # 仅在读取视频时使用

    while flag_run_detection:
        start_time = time.time()  # timing init
        if from_camera_get_image(img_path):
            break  # If the video reaches the end, break the loop
        start_frame += 300

        # 用 alphapose 找到关键点坐标
        detect_pose()

        status = stand_or_sit(0, 300, json_path)
        if status:
            sed_time += 10  # 时间加十秒
        else:
            sed_time = 0  # 发现人不是坐着就重置时间

        # 判断关闭事件是否已触发
        if stopEvent.is_set():
            # 关闭事件置为未触发，清空显示label
            stopEvent.clear()
            # self.ui.DisplayLabel.clear()
            # self.ui.Close.setEnabled(False)
            # self.ui.Open.setEnabled(True)
            break

        save_result(yolo_output, json_path, sed_time, status)

        pix_result = QPixmap("C:/Users/zyh/AlphaPose/tests/res/vis/labelledResult.jpg")
        ui.DispalyLabel.setPixmap(pix_result)
        ui.label_2.setText("久坐检测进行中。该时段输出如下：")

        wait(start_time)

    if not stopEvent.is_set():
        pix_result = QPixmap("C:/Users/zyh/AlphaPose/tests/res/vis/labelledResult.jpg")
        ui.DispalyLabel.setPixmap(pix_result)
        ui.label_2.setText("久坐检测完成。输出如下：")


if __name__ == "__main__":

    flag_run_detection = True
    stopEvent = threading.Event()
    stopEvent.clear()

    app = QApplication(sys.argv)
    mainWnd = QMainWindow()
    ui = Ui_MainWindow()
    # 可以理解成将创建的 ui 绑定到新建的 mainWnd 上
    ui.setupUi(mainWnd)

    # init window
    ui.ButtonStart.setEnabled(True)
    ui.ButtonReset.setEnabled(True)

    ui.ButtonStart.clicked.connect(set_flag_of_detection)
    ui.ButtonReset.clicked.connect(clear_flag_of_detection)
    ui.label_2.setText("久坐检测未开始......以下图片为范例")

    mainWnd.show()

    sys.exit(app.exec_())