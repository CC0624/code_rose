# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIL import Image
import numpy as np
import os
import time
import cv2
import platform
import argparse
import zipfile



    
def print_photo(photo_file, width=140, height_auto=True, reverse=True, outfile=None):
    """

    :param photo_file: The file path of your picture.
    :param width: Print width, different monitor sizes may require different values. [default: 140]
    :param height_auto: Auto set the print height according to original aspect ratio. [default: False]
    :param reverse: Invert the image: 255-x. [default: True]
    :param outfile: save the output to txt file.
    :return:
    """

    im = Image.open(photo_file).convert('L')  # 打开图片文件，转为灰度格式
    if height_auto:
        height = int(width * im.size[1] / im.size[0])  # 打印图像高度
    else:
        height = 70
    arr = np.array(im.resize((width, height)))  # 转为NumPy数组
    if reverse:  # 反色处理
        arr = 255 - arr

    chs = np.array([' ', '.', '-', '+', '=', '*', '#', '@'])  # 灰度-字符映射表
    # chs = np.array([' ', '人', '小', '舌', '乐', '节', '快', '情'])  # 灰度-字符映射表
    # chs = np.array([' ', '.', '-', 'I', 'U', '♥', '小', '舌'])  # 灰度-字符映射表
    arr = chs[(arr / 32).astype(np.uint8)]  # 灰度转为对应字符

    if outfile:
        with open(outfile, 'w') as fp:
            for row in arr.tolist():
                fp.write(''.join(row))
                fp.write('\n')

    for i in range(arr.shape[0]):  # 逐像素打印

        for j in range(arr.shape[1]):
            print(arr[i, j], end=' ')
        print()


def video_to_picture(video_path, frame_interval=5, eps=0):
    """
    This function is used to save the video frame by frame as a series of pictures.
    :param video_path: the path of your video.
    :param frame_interval: output picture every frame_interval frame.
    :param eps: if eps > 0, ignore the current frame if it diff with last frame less than eps.
    :return:
    """
    vc = cv2.VideoCapture(video_path)
    rval, frame = vc.read()

    fps = vc.get(cv2.CAP_PROP_FPS)
    frame_all = vc.get(cv2.CAP_PROP_FRAME_COUNT)
    print("[INFO] 视频FPS: {}".format(fps))
    print("[INFO] 视频总帧数: {}".format(frame_all))
    print("[INFO] 视频时长: {}s".format(frame_all / fps))
    dir, file = os.path.split(video_path)
    file_name = file.split('.')
    outputPath = os.path.join(dir, file_name[0])
    if os.path.exists(outputPath) is False:
        print("[INFO] 创建文件夹,用于保存提取的帧")
        os.mkdir(outputPath)
    frame_count = 1
    count = 0
    last_frame = frame
    while rval:
        rval, frame = vc.read()
        if frame_count % frame_interval == 0:
            filename = os.path.sep.join([outputPath, "rose_{}.jpg".format(count)])
            # print(all(frame == last_frame))
            # if not (frame == last_frame).all():
            print(sum(sum(sum(abs(frame - last_frame)))))
            if sum(sum(sum(abs(frame - last_frame)))) >= eps:
                cv2.imwrite(filename, frame)
                count += 1
                print("保存图片:{}".format(filename))
            last_frame = frame
        frame_count += 1

img_path = './pic'
num_figs = 1124
video_path = 'pic.mp4'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Some param for print.')
    parser.add_argument('--width', default=90, type=int,
                        help='Print width, different monitor sizes may require different values. [default: 90]')
    parser.add_argument('--zip_password', type=str)
    args = parser.parse_args()
    if not os.path.exists('./pic'):
        zip_file = zipfile.ZipFile('./pic.zip')  # 文件的路径与文件名
        zip_list = zip_file.namelist()  # 得到压缩包里所有文件
        for f in zip_list:
            zip_file.extract(f, './', pwd=args.zip_password.encode("utf-8"))  # 循环解压文件到指定目录
        zip_file.close()  # 关闭文件，必须有，释放内存

    # video_to_picture(video_path=video_path)
    
    for i in range(num_figs):
        try:
            im = os.path.join(img_path, 'rose_' + str(i) + '.jpg')
            if i < 1123:
                sleep_time = 0.1
                width = 90
            else:
                sleep_time = 6
                width = 90
            print_photo(im, width=args.width)
            # print_photo(im, outfile=str(i) + '.txt', width=width)
            time.sleep(sleep_time)
        except:
            None
        
        if platform.system().lower() == 'windows':
            os.system('cls')
        elif platform.system().lower() == 'linux':
            os.system('clear')

