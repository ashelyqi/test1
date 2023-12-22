# -*- coding: utf-8 -*-
import logging
from common.tool import tool
import time
from common import *
from common.bleSpeek import bleSpeek
from elements.deviceSetting import deviceSetting
from common.deviceinfo import deviceInfo
from common.common import ControlRelay

class boding:
    def __init__(self,devicename,serial_Com):
        tool.init(self,devicename)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)
        # 重置门锁
        self.reset(serial_Com)
        time.sleep(25)
                
        for i in range(10000):
            #执行绑定操作
            result=self.run(i,serial_Com)

            if result=="门锁绑定成功":
                record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                tool.write_csv(self,record_time,i,result)
                
            else:
                record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                tool.write_csv(self,record_time,i,result)
                # continue

            self.logger.info("门锁已绑定账号")
            time.sleep(1)
            self.reset(serial_Com)
            time.sleep(25)
            print("门锁解绑完成")

            # tool.restart(self)
            # time.sleep(2)
            # if self.d(text="删除设备").exists(15):
            #     self.d(text="删除设备").click()
            #     time.sleep(2)
            #     self.d(index=4).click()
            #     time.sleep(2)
            #     self.d(text="我知道了").click()
            #     self.logger.info("门锁解绑并在app上删除完成")
            
            


    def run(self,i,serial_Com):
        # 进入门锁主页
        tool.restart(self)
        if self.d(textContains="声明与条款").exists(5):
            self.d(resourceId="com.lockin.loock:id/checkbox").click()
            self.d(text="同意并继续").click()

        if self.d(text="删除设备").exists(5):
                self.d(text="删除设备").click()
                time.sleep(2)
                self.d(index=4).click()
                time.sleep(2)
                self.d(text="我知道了").click()
                tool.restart(self)
                self.logger.info("门锁解绑并在app上删除完成")

        if self.d(text = "添加设备").exists(10):
            self.d(text = "添加设备").click()
            for i in range(3):
                if self.d(text = "添加设备").exists(5):
                    self.d(text = "添加设备").click()
                else:
                    break
        # else:
        #     addBtn=self.d.xpath('//*[@resource-id="com.lockin.loock:id/fl_container"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.ImageView[1]')
        #     addBtn.click()
        #     time.sleep(1)
        #     self.d(text = "添加设备").click()
        
        time.sleep(3)
        if self.d(textContains="鹿客智能锁 V5 Air").exists(30):
            self.d(textContains="鹿客智能锁 V5 Air").click()
            self.logger.info("点击了鹿客智能锁 V5 Air")
            print("点击了鹿客智能锁 V5 Air门锁")
        else:
            print("未检测到附近处于配对中的设备...")
            tool.App_Screenshot(self,"未检测到附近处于配对中的设备...")
            return "未检测到附近处于配对中的设备..."

        time.sleep(2)
        try:
            for i in range(10):
                if not self.d(text="确认").exists(3):
                    
                    self.d(textContains="鹿客智能锁 V5 Air").click()
                    print(f"我已经第{i}次点鹿客智能锁 V5 Air了")
                    self.logger.error(f"我已经第{i}次点鹿客智能锁 V5 Air了")
                    self.logger.info("出现了首页看到门锁，但是点不动v03门锁")
                else:
                    break
            time.sleep(2)        
            self.d(text="确认").click()
        except Exception as e:
            print(e)

        time.sleep(2)
        
        if self.d(text="同意并继续").exists(5):
            for i in range(5):
                self.d(resourceId="com.lockin.loock:id/checkbox").click()
                self.d(text="同意并继续").click()
                if self.d(text="下一步").exists(3):
                    break
        time.sleep(1)
        self.d(text="下一步").click()
        if self.d(textContains="没有设置密码").exists(10):
            self.d(text="确定").click()

        #让设备进入配对模式
        self.reparing(serial_Com)

        if self.d(textContains="同步数据成功").exists(15):
            print("设备正在绑定中")
            self.logger.info("设备正在绑定中")
            
            if self.d(textContains="绑定失败").exists(20):
                
                self.logger.error("出现了绑定过程中失败问题")
                tool.App_Screenshot(self,"出现了绑定过程中失败问题")
                result='出现了绑定过程中失败问题'
                record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                tool.write_csv(self,record_time,i,result)

                self.d(text="确定").click()
                
        else:
            print("设备绑定失败")
            print("未进入设备吗？？")
            result="设备绑定失败"
            tool.App_Screenshot(self,result)
            
            self.logger.info("设备绑定失败")  
            return result
        
        if self.d(textContains="配置网络").exists(30):
            print("正在网络配置")
            
        time.sleep(3)
        # app bug先调试解决
        tool.restart(self)
        if self.d(textContains="声明与条款").exists(5):
            self.d(resourceId="com.lockin.loock:id/checkbox").click()
            self.d(text="同意并继续").click()


        time.sleep(1)
        if self.d(textContains="点击继续设置").exists(30):
            print("门锁绑定成功")
            result="门锁绑定成功"
        else:
            print("门锁绑定失败")
            tool.App_Screenshot(self,"门锁绑定失败")
            time.sleep(30)
            result="门锁绑定失败"

        return result

    # 绑定成功后删除
    def DeviceManageDelete(self,i):
        # # 先判断是否门锁已绑定
        # bleSpeek.ble_openDoor(self,i)
        # if self.d(text="已解锁").exists(15):
        #     self.logger.info("门锁已成功绑定账号")
        #     print("门锁已绑定账号")
        #     self.reset(self,serial_Com)
        #     print("门锁解绑完成")

        self.d(text="我的").click()
        self.d(text="设备管理").click()
        self.d(text="管理").click()
        self.d(text="删除设备").click()
        if self.d(text="V03").exists(3):
            self.d(text="V03").click()
            self.d(text="删除").click()
            self.d(text="确认").click()
            time.sleep(1)
            self.d(text="我知道了").click()
        else:
            print("没有V03设备")

        
        #恢复出厂
    def reset(self,serial_Com):
        print("按压恢复出厂按键5s")
        ControlRelay("relay2_left_con", serial_Com)
        time.sleep(5)
        ControlRelay("All_right_con", serial_Com)
        time.sleep(10)

        # public.touch_input.touch_press_key(touch_input_port,adminPWD , light_screen=False)  # 按键验证管理员密码
        # time.sleep(2)

    #进入配对模式
    def reparing(self,serial_Com):
        print("按压功能键5s，进入配对模式")
        ControlRelay("relay3_left_con", serial_Com)
        time.sleep(5)
        ControlRelay("All_right_con", serial_Com)
        time.sleep(2)
       




