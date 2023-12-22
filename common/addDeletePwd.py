# -*- coding: utf-8 -*-
import logging
import random
import time
import common.tool as tool
from common.bleSpeek import bleSpeek
from common.locationKey import locationKey
import csv

# class Switch:
    # # 控制连接手机
    # def __init__(self):
    #     self.file = "E:\\lock\\log\\" + time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())) + '自动化数据.csv'
    #     # self.file = log_folder+ time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '自动化数据.csv'

    # # 主要功能：保存到本地csv文件
    # def write_csv(self, res1='', res2='', res3='', res4='', res5='', res6='', res7='', res8='', res9='',res10='',res11=''):
    #     with open(self.file, 'a', newline='') as f:
    #         #  表格存储，每次测试的时候，可以选择自己需要存储的数据和排序位置 ！！！！！！--------------------------------------------
    #         print("写数据")
    #         row = [res1, res2, res3, res4, res5, res6, res7, res8, res9,res10,res11]
    #         file = csv.writer(f)
    #         file.writerow(row)

class addDeletePwd:

    def __init__(self,device_name,testtimes):
        tool.init(self,device_name)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)
        self.main(testtimes)

    #从用户详情开始，添加密码
    def addPwd(self):
        if self.d(text = "蓝牙钥匙").exists(5):
            self.d(text="密码").click()
            time.sleep(0.5)
            self.d.click(0.797, 0.876)
            if self.d(textContains="该成员的密码数量满啦").exists(5):
                print("该成员的密码数量满啦")
                return "该成员的密码数量满啦"
                #此处需要处理密码满的状态
            else:
                len = random.randint(6, 11) #密码长度随机
                password=""
                for s in range(len):
                    a = random.randint(0,9) #密码值随机
                    password=str(password)+str(a)
                print("密码 = " + password)
                self.d.xpath('//android.widget.EditText').set_text(password)
                self.d(text="下一步").click()
                time.sleep(0.5)
                self.d.xpath('//android.widget.EditText').set_text(password)
                self.d(text = "下一步").click()
                time.sleep(0.5)
                if self.d(text="密码添加成功").exists(60):
                    print("密码添加成功")
                    self.d(text="完成").click()
                    time.sleep(5)
                    return "密码添加成功"
                else:
                    print("不知道为什么失败，先截图")
                    tool.tool.App_Screenshot(self, "密码添加失败")
                    return "密码添加失败,截图"

    #完整操作添加密码
    def addPwd_1(self,w):
        try:
            if bleSpeek.ble_speed(self) != 1:
                Exception("蓝牙连不上")
                self.d(text="钥匙管理").click()
                time.sleep(0.5)
                # self.d(description="Add").click()
                # self.d(text="普通成员").click()
                if self.d(text="赵钱孙"+str(w)).exists():
                    self.d(text="赵钱孙"+str(w)).click()
                    a=self.addPwd()
                    return a
                else:
                    print("未进入钥匙管理界面")
                    return "未进入钥匙管理界面"
        except Exception as e:
            print(e)
            return str(e)

    #删除所有用户
    def deletePwd(self):
        try:
            if bleSpeek.ble_speed(self) != 1:
                Exception("蓝牙连不上")
            self.d(text="钥匙管理").click()
            time.sleep(0.5)
            for j in range(1,10):
                # if self.d(text="赵钱孙").exists(5):
                if self.d(text="赵钱孙"+str(j)).exists(5):
                    self.d(text="赵钱孙"+str(j)).click()
                    time.sleep(2)
                    if self.d(text="删除").exists(5):
                        time.sleep(2)
                        self.d(text="删除").click()
                        print("点击删除")
                        time.sleep(0.5)
                        if self.d(text="取消").exists(3):#用户下无授权
                            # self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.Button[1]').click()
                            # self.d(textContains="取消").sibling(text="删除").click()
                            self.d.click(0.595, 0.857)
                            time.sleep(8)
                        else:
                            print("赵钱孙" + str(j)+"下无授权")
                        if self.d(text="赵钱孙" + str(j)).exists(5):
                            print("删除失败,截图")
                            tool.tool.App_Screenshot(self, "删除密码失败")
                        elif self.d(text="请打开手机蓝牙并靠近门锁操作").exists(1):
                            print("超时未删除成功,截图")
                            tool.tool.App_Screenshot(self, "删除密码失败")
                        else:
                            print("删除成功：赵钱孙" + str(j))
                        time.sleep(1)
                    else:
                        print("未成功进入赵钱孙" + str(j)+"的详情界面，截图")
                        tool.tool.App_Screenshot(self, "未成功进入赵钱孙" + str(j)+"的详情界面")
                else:
                    print("赵钱孙" + str(j)+" 不存在，不需要删除")
            if self.d(text="赵钱孙").exists(5):
                print("批量删除操作有失败历史，截图")
                tool.tool.App_Screenshot(self, "批量删除操作有失败历史")
                return "批量删除操作有失败历史，截图"
            else:
                print("批量删除操作全部成功")
                return "批量删除操作全部成功"

        except Exception as e:
            print(e)
            return str(e)




    def Create_user(self,w):#Create a user
        try:
            if bleSpeek.ble_speed(self) != 1:
                Exception("蓝牙连不上")
                self.d(text="钥匙管理").click()
                time.sleep(0.5)
                # self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]')
                # self.d.click(0.797, 0.88)
                self.d(description="Add").click()
                if self.d(text="用户已满").exists(5): #这里缺少密码已满的判断
                    self.deletePwd()
                else:
                    if self.d(text="选择要添加的成员类型").exists(5):
                        self.d(text="普通成员").click()
                        time.sleep(0.5)
                        self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').set_text("赵钱孙"+str(w))
                        self.d(text="确定").click()  #这里缺少命名冲突的判断，但是不影响运行
                        time.sleep(0.5)
                        self.d.xpath('//*[@content-desc="Back"]').click()
                        self.d(description="Back").click()
                        if self.d(text="赵钱孙"+str(w)).exists(5):
                            print("创建用户成功：赵钱孙"+str(w))
                            return "创建用户成功：赵钱孙"+str(w)
                        else:
                            print("创建用户失败：赵钱孙" + str(w))
                            return "创建用户失败：赵钱孙" + str(w)
        except Exception as e:
            print(e)
            return str(e)

    def main(self,testtimes):
        x=1
        run = Switch()
        run.write_csv(res1="测试轮数", res2="删除所有密码", res3="创建用户",res4="添加密码", res5="测试时间")
        q=testtimes//30+1
        print(q)
        for i in range(0,q): #
            print("开始删除所有用户密码")
            c = self.deletePwd()
            run.write_csv(res1=str(x), res2=str(c), res3="",res4="",res5=str(str(time.strftime('%Y-%m-%d_%H-%M-%S'))))
            for w in range(1,6):
                print("开始创建用户" + str(w))
                a=self.Create_user(w)
                run.write_csv(res1=str(x), res2="", res3=str(a),res4="",res5=str(str(time.strftime('%Y-%m-%d_%H-%M-%S'))))
                for k in range(0,5):
                    print(str(x) + "轮测试，添加密码的成员" + str(w))
                    b = self.addPwd_1(w)
                    x=x+1
                    run.write_csv(res1=str(x), res2="", res3="", res4=str(b),res5=str(str(time.strftime('%Y-%m-%d_%H-%M-%S'))))



