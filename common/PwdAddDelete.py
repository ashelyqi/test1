# -*- coding: utf-8 -*-
import logging
import time
import common.tool as tool
from common.bleSpeek import bleSpeek
from locationKey import locationKey

class addDeletePwd:

    def __init__(self,device_name,a):
        tool.tool.init(self,device_name)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)
        if a == 1:
            for i in range(10000):
                try:
                    self.addPwd(i)
                except Exception as e:
                    print(e)
                    tool.tool.App_Screenshot(self,"密码添加失败")
                    self.logger.error("密码添加失败")
        else:
            self.deletePwd()

    def addPwd(self,i):
        if bleSpeek.ble_speed(self) != 1:
            Exception("蓝牙连不上")
        time.sleep(2)
        self.d(text = "钥匙管理").click()
        time.sleep(0.5)
        #添加管理员密码
        for i in range(10):
            
            locationKey.adminKeyAdd(self)
        addBtn=self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]')
        addBtn.click()
        if self.d(text = "普通成员").exists(5):
            print("选择成员类型中")
            self.d(text = "普通成员").click()
            print("我点了你呢")
        else:
            Exception("未进入成员类型界面")
        time.sleep(0.5)
        self.d(text="确定").click()
        time.sleep(1)
        self.d(text="密码").click()
        time.sleep(0.5)
        self.d.click(0.846, 0.913)
        if i >= 10:
            password = "0" + str(i) + "0" + str(i)
            print("密码 = " + password)
        else:
            password = "00" + str(i) + "00" + str(i)
            print("密码 = " + password)
        self.d.xpath('//android.widget.EditText').set_text(password)
        self.d(text="下一步").click()
        self.d.xpath('//android.widget.EditText').set_text(password)
        self.d(text = "下一步").click()
        if self.d(text="密码添加成功").exists(60):
            print("密码添加成功")
        else:
            print("不知道为什么失败，先截图")

    def deletePwd(self):
        if bleSpeek.ble_speed(self) != 1:
            Exception("蓝牙连不上")
        self.d(text = "成员管理").click()
        time.sleep(0.5)
        for i in range(50):
            user = "普通成员" + str(i + 1)
            try:
                self.d(text=user).click()
                if self.d(text="删除").exists(5):
                    print("删除1")
                    time.sleep(0.5)
                    self.d(text="删除").click()
                if self.d(text="取消").exists(5):
                    print("删除2")
                    time.sleep(0.5)
                    self.d(text="删除").click()
                if self.d(text="成员管理").exists(60):
                    print("删除成功 = " + user)
            except Exception as e:
                print(e)




