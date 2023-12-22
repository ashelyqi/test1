# -*- coding: utf-8 -*-

import uiautomator2 as u2
import os
import time
import re
import serial
import string
import datetime
import sys
import serial
import csv
import threading
import requests
from common.logformat import log_format

class tool:

    def initNoDevice(self):
        log_path=os.path.dirname(os.path.dirname(__file__))
        # print(log_path)

        self.file = log_path+'\Logdir\\'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '自动化数据.csv'

    # 初始化函数，定义文件名和设备名，连接手机
    def init(self,device_name):
        self.host='https://test2-tc-lockin-cloud-biz.dding.net'
        self.session=requests.session()
        #日志保存路径,如果没有存在文件夹则创建
        path=os.path.dirname(__file__)
        # print(path)
        errorfile=os.getcwd()+"\\common\\Logdir\\error"
        # print(errorfile)
        # print(os.path.exists("Logdir\\errordir"))
        if os.path.exists("common\\Logdir\\error"):
            # print("文件已存在，无须创建")
            pass
        else:
            os.makedirs("common\\Logdir\\error")
                    
        self.save_path=path+'\Logdir\\'

        # 保存的文件名
        # 根据调用的函数的不同，来调整数据的文件名
        self.file = self.save_path+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '自动化数据.csv'
        
        # 设备的名称，此处命名后续修改名称方便且不会乱
        self.device_name = device_name
        self.appname = "com.lockin.loock"
        # 压测的软件名称。提前传入参数，增加代码的复用性
        # 连接手机,默认为adb devices获取到的第一个设备序号
        self.d = u2.connect_usb()
        self.d.implicitly_wait(10)
        log_format()
        

    #重新写记录数据的方法，以前的方法太过于死板
    #按照函数传多少数据，就往csv文件中写入几个参数，这样就不会受参数个数的限制了
    def write_csv(self,*args):
        with open(self.file, 'a', newline='',encoding='utf-8') as f:
            row=[]
            for i in args:
                row.append(i)
            print(row)
            file = csv.writer(f)
            file.writerow(row)

        #红外切换截图
    def IRcard_Screenshot(self, Picturename):
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        image = self.d.screenshot()
        
        # print(path)
        image.save(self.save_path + now + Picturename + ".jpeg")

    # 主要功能：截屏
    def App_Screenshot(self, Picturename):
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        image = self.d.screenshot()
        # print(self.save_path+'error\\'+ now + Picturename + ".jpeg")
        image.save(self.save_path+'error\\'+ now + Picturename + ".jpeg")

    # # 主要功能：截屏
    # def App_Screenshot(self, Picturename):
    #     now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    #     image = self.d.screenshot()
    #     image.save("D:/失败截屏/" + now + Picturename + ".jpeg")

    # 重启软件，并进入插件首页
    def restart(self):
        self.d.app_stop(self.appname)
        time.sleep(3)
        # 启动目标程序
        self.d(description="鹿客管家").click()
        # self.d(resourceId="com.miui.home:id/icon_icon", description="鹿客管家").click()
        
        # time.sleep(3)
        # # 进入设备页面
        # self.d(text='设备').click()
        # if self.d(text=self.device_name).exists(20):
        #     self.d(text=self.device_name).click()
        # else:
        #     print("未发现设备，请检查app")


    # 重启软件，并进入插件首页
    def restartApp(self):
        self.d.app_stop(self.appname)
        time.sleep(5)
        # 启动目标程序
        self.d(resourceId="com.miui.home:id/icon_icon", description="鹿客管家").click()
        print("打开鹿客了")
        time.sleep(3)
        



    # ----------------------------------------------------继电器使用----------------------------------------------------------
# 连接串口
# com_number为串口端口
def strSendPort_First(strCmd, strPort="com8", fTime=0.5):
    try:
        ser = serial.Serial(strPort, 9600, timeout=float(fTime))
        if strCmd != "":
            ser.write(strCmd)
            strInfo = ser.readlines()
        return strInfo
    except Exception as e:
        print(e)

        # 连接串口
        # com_number为串口端口


# def strSendPort_First(strCmd, strPort="com10", fTime=0.5):
#     try:
#         ser = serial.Serial(strPort, 9600, timeout=float(fTime))
#         if strCmd != "":
#             ser.write(strCmd)
#             strInfo = ser.readlines()
#         return strInfo
#     except Exception as e:
#         print(e)

# 控制继电器
def cin_passwd(intInput,strPort):
    if intInput == 79:
        tool.strSendPort_First("O".encode(),strPort)
        # vShowForm("All On")
        # 1111
    elif intInput == 1:
        # 1110
        tool.strSendPort_First("N".encode(),strPort)
    elif intInput == 2:
        # 1101
        tool.strSendPort_First("M".encode(),strPort)
    elif intInput == 3:
        # 1011
        tool.strSendPort_First("K".encode(),strPort)
    elif intInput == 4:
        # 0111
        tool.strSendPort_First("G".encode(),strPort)
    elif intInput == 80:
        tool.strSendPort_First("P".encode(),strPort)
        # vShowForm("All Off")
        # 0000
    else:
        print("Input fail,pleas input 0 or 1!")
        return False
    return True



