import logging
import time
from common.tool import tool


class BLEKeepTime:
    def __init__(self,device_name):
        tool.init(self,device_name)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)

        tool.write_csv(self,"时间","蓝牙连接保持情况","蓝牙连接时长","蓝牙连接保持时长")
        for i in range(10000):
            try:
                connectTime,keepTime=self.ble_speed()
                if keepTime==-1:
                    result="未进入门锁主页"
                elif keepTime==0:
                    result="蓝牙连接失败"
                else:
                    if keepTime>=15*60:
                        result="蓝牙连接保持时长达标>15min"
                    else:   
                        result="蓝牙连接保持时长不达标"
                        tool.App_Screenshot(self,"蓝牙保持时长不达标，此时门锁主页状态")
                record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                #record_time事件发生时间
                #result蓝牙连接状态
                #蓝牙连接保持时长
                tool.write_csv(self,record_time,result,connectTime,keepTime)
            except Exception as e:
                print(e)

     # 蓝牙长连接
    def ble_speed(self):
        # 进入插件首页
        tool.restart(self)
        
        
        if self.d(text="首页").exists(5):
            # 计时开始
            timestart=time.time()
            self.d(text='鹿客智能').click()

            # #为了兼容APP加载慢，导致置灰点击之后无响应问题
            for i in range(5):
                if self.d(text="相册").exists(1):
                    break
                else:
                    self.d(text='鹿客智能').click()
                    self.logger.info(f"出现了点击鹿客智能，没有进入设备功能页面，第{i+1}次点击")

        
        if self.d(text="安全守护中").exists(60):
            time1 = time.time()
            connectTime=time1-timestart
            self.logger.info("蓝牙已连接")

            for i in  range(16):
                if self.d(textContains="更新于").exists(60):
                    break
                else:
                    keephowtime=i+1
                    self.logger.info(f"蓝牙已连接超过{keephowtime}min了")
                    #等5min点击一下屏幕，防止手机息屏
                    self.d.click(0.746, 0.214)
                    self.logger.info(f"每1min点击一下屏幕，防止手机息屏")

            time2 = time.time()
            time3 = time2 - time1

            self.logger.info(f"蓝牙已断开,蓝牙连接时长{connectTime}，蓝牙保持时长{time3}")
            print("蓝牙断开")
            return (connectTime,time3)


        elif self.d(text = "相册").exists(5):
            tool.App_Screenshot(self,"蓝牙连接失败")
            self.logger.error("蓝牙连接失败")
            # print("蓝牙连接失败")
            return 0,0
        else:

            self.logger.error("未进入门锁主页")
            tool.App_Screenshot(self,"未进入门锁主页")
            return -1,-1