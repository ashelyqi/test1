# # # # # # # # # import allure
# # # # # # # # # # 动态定制测试报告
# # # # # # # # # allure.dynamic.title('用例编号')
# # # # # # # # # allure.dynamic.description('用例标题')


# # # # # # # # class num:

# # # # # # # #     def test(self):
# # # # # # # #         count=1

# # # # # # # # n=num()

# # # # # # # # n.count=1
# # # # # # # # print(num.test())

# # # # # # # import logging
# # # # # # # import logging.config
# # # # # # # import logging.handlers
# # # # # # # import json
# # # # # # # import yaml

# # # # # # # logging.basicConfig(
# # # # # # #     filename='log.txt',
# # # # # # #     level=logging.INFO,
# # # # # # #     filemode='a',
# # # # # # #     encoding='utf-8',
# # # # # # #     format='%(asctime)s %(levelname)-8s %(name)s [%(funcName)s(%(module)s:%(lineno)s)] %(message)s'
# # # # # # # )

# # # # # # # logger=logging.getLogger("login")
# # # # # # # logger_code=logging.getLogger("login.code")
# # # # # # # logger_test=logging.getLogger("login.test")

# # # # # # # def add(a,b):
# # # # # # #     logger_code.info(f'收到的参数，a={a},b={b}')

# # # # # # #     c=a+b
# # # # # # #     logger_code.error(f'输出结果c={c}')

# # # # # # # if __name__=="__main__":
# # # # # # #     add(1,2)
# # # # # # import time
# # # # # # import uiautomator2 as u2
# # # # # # d = u2.connect_usb()
# # # # # # # # d(text="设备").click()
# # # # # # # d(index=3).click()
# # # # # # # time.sleep(1)
# # # # # # # wifitext=d(textContains="已连接").get_text()
# # # # # # # result = "wifi更换成功"+wifitext
# # # # # # # print(result)
# # # # # # before_wifi_Name=d(textContains= "Test").get_text()
# # # # # # print(before_wifi_Name)
# # # # # # after_wifi_Name=""
# # # # # # if before_wifi_Name == "Test_one_2.4G":
# # # # # #     after_wifi_Name=="Test_3_2.4G"
# # # # # # else:
# # # # # #     after_wifi_Name=="Test_one_2.4G"

# # # # # # print(after_wifi_Name)
# # # # # # d(resourceId="com.lockin.loock:id/iv_arrow").click()

# # # # # # if d(text = after_wifi_Name).exists(3):
# # # # # #     d(text=after_wifi_Name).click()
# # # # # # else:
# # # # # #     for i in range(10):
# # # # # #         d.swipe(0.483, 0.67,0.706, 0.361)
# # # # # #         if d(text = after_wifi_Name).exists(3):
# # # # # #             d(text=after_wifi_Name).click()
# # # # # #             break
    
# # # # # # time.sleep(2)
# # # # # # if d(text = "下一步").exists(10):
# # # # # #     d(text="下一步").click()


# # # # # import csv


# # # # # def prmsg(self,*args):
# # # # #     # print(args)
# # # # #     # for i in args:
# # # # #     #     print(i)
# # # # #     with open("num.csv", 'a', newline='',encoding='utf-8') as f:
# # # # #         # row = 表格中数据的排序
# # # # #         # row1=["日期","测试次数","测试结果","直播总时长","进入直播的时间"]
# # # # #         row=[]
# # # # #         for i in args:
# # # # #             # row = [args[i], i+1, result, testTime]
# # # # #             row.append(i)
# # # # #         file = csv.writer(f)
        
# # # # #         file.writerow(row)

# # # # # if __name__=="__main__":
# # # # #     prmsg(1,2,3)
# # # # #     prmsg(2,3,4)
# # # # #     prmsg(2,3,4,7,4,6,4,"8sdbhcdvg","sdfgr")

# # # # # 线程
# # # # from concurrent.futures import ThreadPoolExecutor
# # # # from threading import *
# # # # import time


# # # # def f(*args):
# # # #     time.sleep(1)
# # # #     print("线程之执行")

# # # # with ThreadPoolExecutor(max_workers=6) as pool:
# # # #     print("创建线程后，活跃的线程数：",active_count())

# # # #     #通过遍历的形式，将一系列的任务提交到线程池中
# # # #     res_list=pool.map(f,range(5))
# # # #     for i in res_list:
# # # #         print(i)
# # # #     print("激活线程后，活跃的线程数：",active_count())

# # # # a=input("请输入内容：")

# # # # print(a*3)
# # # # print("线程任务完成后，活跃的线程数：",active_count())
# # # import requests


# # # host="https://test-paas-biz.lockin.com"
# # # method="POST"
# # # path="/ota/version/forceUpgrade"
# # # url=host+path
# # # uuid='d2c2d97be931181e81ded42cf0813554'

# # # print(url)
# # # data={
# # #     "uuid": 'd2c2d97be931181e81ded42cf0813554',
# # #     "version":"1.0.8"
# # #     }

# # # session=requests.session()
# # # req=session.request(method,url,json=data)
# # # print(req.json)
# # # print(req.json())


# # # # headers={"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
# # # #         "Authorization":"502faf15cec44dc8c4996ba0ec87515540f7c86f8bd90b326526dd9cf2094a96132c78ca4373d17f5629d1dc2dbdde92",
# # # #         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
# # # #         "Knfie4j-Gateway-Request":"796a39bc91f401be7f5856667b41b61d",
# # # # #         "Request-Origion":"Knife4j"}

# import logging
# from common.logformat import log_format
# from common.tool import tool
# import uiautomator2 as u2
# import os
# import time
# import re
# import serial
# import string
# import datetime
# import sys
# import serial
# import csv
# import subprocess
# import threading
# from elements.deviceSetting import deviceSetting
# import common.logformat as logformat
# # -*- coding: utf-8 -*-

# class bleSpeek:

#     def __init__(self,device_name):
#         tool.init(self,device_name)
       
#         #为每个模块创建记录器
#         self.logger=logging.getLogger(__name__)
#         # print(self.logger)
        
        
#     # def aad(self):
#     #     print("进入了aad")
#     #     self.logger.error("调试")
#     #     c=1+2
#     #     print(c)


from common.tool import tool
import time
def Online(self):
    # self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
    
    # 点击直播画面，进入直播
    self.d.click(0.489, 0.235)
    time_start = time.time()
    time.sleep(2)
    
    connect_time=0

    # 开始计时
    if self.d(textContains='KB/s').exists(10):
        self.logger.info("进入实时画面")
        time_end = time.time()
        connect_time = time_end - time_start
        print(connect_time)
        result = "直播成功"
        self.logger.info("直播成功")
        for i in range(2):
            if self.d(text = "继续观看").exists(200):
                self.d(text = "继续观看").click()
                print("就继续看看吧")
    else:
        tool.App_Screenshot(self,"无法进入直播")
        result="无法进入直播"
        self.logger.error("无法进入直播")
        return (result,0,0)

if __name__=="__main__":
    Online()