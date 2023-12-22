import logging
from common.logformat import log_format
from common.tool import tool
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
import subprocess
import threading
from elements import deviceSetting
# -*- coding: utf-8 -*-

class bleSpeek:

    def __init__(self,device_name):
        tool.init(self,device_name)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)
        tool.write_csv(self,"时间","压测次数","压测结果", "APP启动加载时长","蓝牙连接时长","点击开门到已解锁时长","蓝牙开锁总时长")
        for i in range(10000):
            try:
                self.ble_openDoor(i)
                time.sleep(1)
            except Exception as e:
                print(e)



    # 蓝牙连接速率统计
    def ble_speed(self):
        # 进入插件首页
        tool.restart(self)

        # 计时开始
        time_Start= time.time()
        if self.d(text="首页").exists(5):
            time_first=time.time()
            time_Loading=time_first-time_Start

        # #为了兼容APP加载慢，导致置灰点击之后无响应问题
        # time.sleep(3)

        # # 进入设备页面
        # if self.d(text='鹿客智能').exists(5):
            self.d(text='鹿客智能').click()

            #为了兼容APP加载慢，导致置灰点击之后无响应问题
            for i in range(5):
                if self.d(text="相册").exists(0.1):
                    break
                else:
                    self.d(text='鹿客智能').click()
                    self.logger.info(f"出现了点击鹿客智能，没有进入设备功能页面，第{i+1}次点击")


        if self.d(text="安全守护中").exists(60):
            time_Ble = time.time()
            # connect_time = time_Ble - time_first

            # app优化了蓝牙连接逻辑：app一启动就发起蓝牙连接
            connect_time = time_Ble - time_Start

            self.logger.info("进入门锁首页，并连上蓝牙了")
            return time_Loading,connect_time

        elif self.d(text = "相册").exists(5):
            tool.App_Screenshot(self,"蓝牙连接失败")
            self.logger.error("蓝牙连接失败")
            # print("蓝牙连接失败")
            return 0
        else:
            # print("未进入门锁主页")
            self.logger.error("未进入门锁鹿客智能页")
            tool.App_Screenshot(self,"未进入门锁鹿客智能页")
            return -1

    # 蓝牙开锁
    def ble_openDoor(self,i):
        bleTime = self.ble_speed()
        # if bleTime == -1:
        #     bleTime = self.ble_speed()
        # print(bleTime)
        # # print(bleTime != 0 & int(bleTime != -1))

        if bleTime != 0 and int(bleTime != -1):
            # print(bleTime != 0 | int(bleTime != -1))
            # self.d.swipe(0.212, 0.95, 0.864, 0.95)
            
            #点击开门
            self.d(text="开门").click()
            time1=time.time()
            
            if self.d(text='已解锁').exists(20):
                time2=time.time()
                open_time=time2-time1
                result="开锁成功"
                # print("开锁成功")
                self.logger.info("开锁成功")
                # 手动计算多次，平均点击开们后1.2s左右开锁成功
                
                Ble_Opentime=bleTime[1]+1.2
                record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                # 记录时间：app加载时长，蓝牙连接时长，点击开锁到APP弹窗解锁时长，蓝牙连接+实际开锁时长
                tool.write_csv(self,record_time,i + 1,result, bleTime[0],bleTime[1],open_time,Ble_Opentime)
                return
            else:
                
                self.logger.error("开锁失败")
                result="开锁失败"
                tool.App_Screenshot(self,"开锁失败")
        elif int(bleTime == -1):
            result="未进入门锁鹿客智能页"
            tool.App_Screenshot(self,"未进入门锁鹿客智能页")
            self.logger.error("未进入门锁鹿客智能页")
            record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            tool.write_csv(self,record_time,i + 1,result)
        else:
            result="蓝牙连接失败"
            tool.App_Screenshot(self,"蓝牙连接失败")
            self.logger.error("蓝牙连接失败")
            record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            tool.write_csv(self,record_time,i + 1,result)
        
            
