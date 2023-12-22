# -*- coding: utf-8 -*-
import logging
import time

from common.bleSpeek import bleSpeek
from common.tool import tool


class onlineTime:

    def __init__(self,device_name):
        tool.init(self,device_name)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)
        tool.write_csv(self,"时间","测试次数","测试结果","直播加载时长","直播保持时长")
        for i in range(10000):
            try:
                tool.restart(self)
               
                result=self.Online()
                # print(type(result))
                recordtime=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                tool.write_csv(self,recordtime,i,result[0],result[1],result[2])
                
            except Exception as e:
                print(e)

    def Online(self):
        time.sleep(10)
        # 点击直播画面，进入直播
        self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
        # self.d.click(0.489, 0.235)
        time_start = time.time()
        connect_time=0

        # 开始计时
        if self.d(textContains='KB/s').exists(30):
            self.logger.info("进入实时画面")
            time_end = time.time()
            connect_time = time_end - time_start

            # # 新增打开对讲功能
            # self.logger.info("进入对讲")
            # self.d.click(0.381, 0.913)
            if self.d(text = "连接失败,请点击重试").exists(100):
                time_speak=time.time()-time_end
                tool.App_Screenshot(self,"直播断开")
                result="直播断开"
                return (result,connect_time,time_speak)

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
            
        if self.d(text="连接失败,请点击重试").exists(600):
            time_end2 = time.time()
            time_result = time_end2 - time_end
            print(time_result)
            if time_result < 480:
                print("直播时长过短")
                tool.App_Screenshot(self,f"直播时长过短,{time_result}")
                result = "直播失败"
                self.logger.error("直播失败")
            else:
                result = "直播成功"
                self.logger.info("直播成功")  
        else:
            result="11分钟还没结束"
            tool.App_Screenshot(self,"直播11分钟了")
            self.logger.error("11分钟还没结束")

        return (result,connect_time,time_result)


