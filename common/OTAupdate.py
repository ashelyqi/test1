import json
from common.deviceinfo import deviceInfo 
import requests
import logging
from common.tool import tool
import time
class OTAupdate:

    def __init__(self,devicename,OTAversion,downOTAVersion,uuid,test_Env):

        self.host="https://paas-biz.lockin.com"
        # self.session=requests.session()
        tool.init(self,devicename)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)
        
       
        # 实例化deviceinfo类
        self.verInfo=deviceInfo(devicename)
        # tool.write_csv(self,"时间","测试次数","测试结果","实际版本或问题")

        for i in range(10000):
            try:
                # 每次都重新启动app
                tool.restart(self)
                result=self.OTAloop(OTAversion,downOTAVersion,uuid,i,test_Env)
                record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                tool.write_csv(self,record_time,i+1,result[0],result[1])
               
            except Exception as e:
                print(e)

    #检查OTA版本是否完全升级成功
    def check_version(self,OTAversion):

        # OTAversion={'固件版本号': '1.0.6', '猫眼版本': '1.0.6', 'Wi-Fi版本': '1.0.6', '主控固件版本': '12.0.2.1', '蓝牙固件版本': '1.0.2.1', '面容固件版本': '16.3.7.1', '指纹固件版本': '31.1.9.1'}
        # modulesVersion={'固件版本号': '1.0.6', '猫眼版本': '1.0.6', 'Wi-Fi版本': '1.0.6', '主控固件版本': '1.0.2.1', '蓝牙固件版本': '1.0.2.1', '面容固件版本': '16.3.7.1', '指纹固件版本': '31.1.9.1'}

        modulesVersion=self.verInfo.get_modulesVersion()
        # print(modulesVersion)

        for k in modulesVersion:
            # print(k)
            #如果当前版本存在跟预期版本不符，则跳出循环
            if OTAversion[k]!=modulesVersion[k]:
                self.logger.error("OTA失败，{k}模块版本号不对应。预期版本:{OTAversion[k]}，实际版本:{modulesVersion[k]}")
                tool.App_Screenshot(self,'OTA失败')
                
                result=f"OTA失败，{k}模块版本号不对应。预期版本:{OTAversion[k]}，实际版本:{modulesVersion[k]}"
                return ("OTA升级失败",result)
        
        result=f"实际版本:{modulesVersion['固件版本号']}"
        return ("OTA升级成功",result)         


    def OTAloop(self,OTAversion,downOTAVersion,uuid,i,test_Env):
        #进入设备信息页面
        deviceInfo.enter_deviceinfo(self)
        time.sleep(2)
        ota_ver_before=downOTAVersion

        if  self.d(text="有新版本").exists(5):
            # 获取大版本用于降级
            ota_ver_before=self.verInfo.get_OTAversion()
            self.logger.info(f'存在新版本，准备升级')

            # 1.点击更新版本
            # 2.若检测到“当前已是最新版本”字样，先检测大版本，若大版本是更新的版本，再检测小版本号。若都更新成功，则打印日志。
            # 3.操作降级，每60s检测一下大版本号和小版本号
            self.d(text="有新版本").click()
            
            if self.d(text="立即更新").exists(5):
                self.d(text="立即更新").click()
            else:
                self.logger.error("没有找到立即更新的按钮")
            self.logger.info("开始升级版本....")
            #检查当前升级状态
            if self.d(textContains="正在升级").exists(10):
                self.logger.info('正在升级，请稍后...')
                if self.d(textContains="升级失败").exists(20):
                    tool.App_Screenshot(self,"升级失败")
                    record_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                    tool.write_csv(self,record_time,i+1,"升级失败,点击重试")
                    self.d(text="重试").click()

                if self.d(textContains="正在安装升级包").exists(60):
                    self.logger.info('正在安装升级包...')
            else:
                if self.d(text="升级失败").exists(5*60):
                    tool.App_Screenshot(self,"升级失败")
                    
                    self.logger.error("升级失败...")
                    tool.restart(self)
                    return ("升级失败","升级过程中出问题了")

            # # 兼容插件bug，为了暂时运行脚本
            # time.sleep(5*60)
            

            if self.d(textContains="最新版本").exists(5*60):
                UpdateVer=self.d(textContains="当前版本").get_text()
                 #点击左上角返回键
                self.d(description="Back").click()
                
                self.logger.info(f'更新后的版本：{UpdateVer}')
                time.sleep(3)
            time.sleep(2)
            #判断升级完后的版本是否符合预期
            result=self.check_version(OTAversion)
            print(result)
            self.logger.info(result)
            
            return result
                
        else:
   
            print(ota_ver_before)
            self.logger.info(f'当前已是最新版本，先降级版本至原来的版本{ota_ver_before}')
            #先将版本强制降级至原来的版本
            self.updownOTA(downOTAVersion,uuid,test_Env)

            time.sleep(6*60)
            self.logger.info(f'降级完成，开始检查版本号...')
            # 降级完成，重新获取当前版本号
            
            #重启app,进入设备信息页面
            tool.restart(self)
            deviceInfo.enter_deviceinfo(self)
            time.sleep(2)
            
            bigVersion=self.verInfo.get_OTAversion()
            if bigVersion==ota_ver_before:
                self.logger.info(f'降级成功，当前版本{bigVersion}')
                result=("降级成功",f"当前版本{bigVersion}")
            else:
                self.logger.error("降级失败...")
                result=("降级失败",f"当前版本{bigVersion}")

            return result

    def updownOTA(self,downOTAVersion,uuid,test_Env):
        if test_Env==1:
            host="https://test-paas-biz.lockin.com"
        else:
            host="https://paas-biz.lockin.com"
        method="POST"
        path="/ota/version/forceUpgrade"
        url=host+path
        print(url)
        data={
            "uuid": uuid,
            "version":downOTAVersion
            }
        print(data)
        session=requests.session()
        req=session.request(method,url,json=data)
        # print(req.json)
        print(req.json())
        



# if __name__=="__main__":
#     OTA=OTAupdate()
#     x=OTA.check_version()
#     print(x)
            
