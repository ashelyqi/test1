# -*- coding: utf-8 -*-


import logging
from common.tool import tool
from common.bleSpeek import bleSpeek
import time

class onLineConnect:

    def __init__(self,device_name):
        tool.init(self,device_name)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)
        tool.write_csv(self, "时间","测试次数","测试结果","直播加载时长")
        for i in range(10000):
            try:
                tool.restart(self)
                
                res=self.Connect()
                record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))   
                tool.write_csv(self, record_time,i+1,res[0],res[1])

            except Exception as e:
                print(e)

    def Connect(self):
        time.sleep(10)
        self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
        self.logger.info("点击进入直播")
        time_start = time.time()
        connect_time=''

        # 开始计时
        if self.d(textContains='KB/s').exists(30):
            self.logger.info("进入实时画面")
            time_end = time.time()
            connect_time = time_end - time_start
            print(connect_time)
            result = "直播成功"          
        else:
            result = "直播失败"
            tool.App_Screenshot(self,"直播失败")
        
        return (result,connect_time)
        
        


   

