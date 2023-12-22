# -*- coding: utf-8 -*-
import logging
import time

from common.bleSpeek import bleSpeek
from common.onLineConnect import onLineConnect
from common.tool import tool
from elements.deviceSetting import deviceSetting


class IRcardTest:

    def __init__(self,device_name):
        tool.init(self,device_name)
        self.logger=logging.getLogger(__name__)

        
        for i in range(10000):
            red_buff=['自动切换','一直关闭','一直打开']
            try:
                for j in red_buff:
                    self.IRcard(j,i + 1)
            except Exception as e:
                print(e)

    def IRcard(self,red_buff,i):
        if bleSpeek.ble_speed(self) != 1:
            Exception("蓝牙连不上")
        #进入红外设置页面

        deviceSetting.setting_info(self)
        deviceSetting.catInfo(self)
        deviceSetting.IRcard(self)

        if self.d(text = "红外夜视").exists(10):
            time.sleep(0.5)
            self.d(text = red_buff).click()
            time.sleep(2)
            self.d(text="确定").click()
            time.sleep(2)
            tool.restart(self)
            
        time.sleep(5)
        res=self.Connect(red_buff, i)
        # print(res)
        if res[0]=="直播成功":
            result="切换成功，请在项目路径下的error文件夹里面查看截图效果是否和名称效果保持一致"      
        else:
            print("重来！！！")
            result="无法进入直播"
            
            self.logger.error("无法进入直播")
        record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        tool.write_csv(self,record_time ,i,result)

    def Connect(self,red_buff,i):
        self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
        
        time_start = time.time()
        connect_time=''

        # 开始计时
        if self.d(textContains='KB/s').exists(30):
            self.logger.info("进入实时画面")
            time_end = time.time()
            connect_time = time_end - time_start
            print(connect_time)
            tool.App_Screenshot(self,red_buff + str(i))
            result = "直播成功"          
        else:
            result = "直播失败"
            tool.App_Screenshot(self,"直播失败")
        
        return (result,connect_time)