# -*- coding: utf-8 -*-

import logging
import time

from common.bleSpeek import bleSpeek
from common.deviceinfo import deviceInfo
from common.onLineConnect import onLineConnect
from common.tool import tool
from elements import deviceSetting

class SwitchWifi:

    def __init__(self,device_name,wifi1,wifi2):
        tool.init(self,device_name)
        self.logger=logging.getLogger(__name__)
        
        for i in range(10000):
            try:
                self.switch(i + 1,wifi1,wifi2)
            except Exception as e:
                print(e)

    def switch(self,i,wifi1,wifi2):
        if bleSpeek.ble_speed(self) != 1:
            # self.logger.error("蓝牙连不上")
            Exception("蓝牙连不上")

        time.sleep(1)
        #进入设置
        deviceInfo.enter_deviceinfo(self)
        time.sleep(0.5)
        before_wifi_Name=self.d(text="Wi-Fi").sibling(index=2).get_text()
        time.sleep(0.5)
        #点击更换wifi
        deviceInfo.clickWiFi(self)
        time.sleep(2)

        after_wifi_Name=""
        print(before_wifi_Name)
        if before_wifi_Name == wifi1:
            after_wifi_Name=wifi2
        else:
            after_wifi_Name=wifi1
        print("wifi名称呢？？"+after_wifi_Name)
        self.logger.info(f"更新后的wifi名称:{after_wifi_Name}")
        #点击选择wifi
        self.d(resourceId="com.lockin.loock:id/iv_arrow").click()
       
        if self.d(text = after_wifi_Name).exists(3):
            self.d(text=after_wifi_Name).click()
        else:
            for i in range(10):
                self.d.swipe(0.394, 0.952,0.508, 0.631,0.5)
                time.sleep(1)
                
                if self.d(text = after_wifi_Name).exists(5):
                    self.d(text=after_wifi_Name).click()
                    result="success"
                    break
                else:
                    tool.App_Screenshot(self,f"列表找不到{after_wifi_Name}")
                    result=f"列表找不到{after_wifi_Name}"
            if result!="success":
                record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                tool.write_csv(self,record_time,i,result)
                return result
          
        time.sleep(2)
        if self.d(text = "下一步").exists(10):
            self.d(text="下一步").click()

        if self.d(text="100%").exists(60):
            time.sleep(1)
        # 重启app，判断首页的wifi是否有切换成功
            tool.restartApp(self)
            time.sleep(2)
            self.d(text="鹿客智能").click()
            self.d(index=3).click()
            time.sleep(1)
            wifitext=self.d(textContains="已连接").get_text() 
            if wifitext.index(after_wifi_Name):
                result = "wifi更换成功"+wifitext
            else:
                result = "wifi更换失败，实际的wifi:"+wifitext+",切换的wifi:"+after_wifi_Name
            self.logger.info(result)                
        else:
            result = "wifi更换失败"
            self.logger.error("wifi更换失败")
            tool.App_Screenshot(self,result)

        record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        tool.write_csv(self,record_time,i,result)
        



