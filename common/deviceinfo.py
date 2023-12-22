import time
from common.bleSpeek import bleSpeek
from elements.deviceSetting import deviceSetting
from common.tool import tool
from elements.mainPage import mainPage
import logging
from common.tool import tool
class deviceInfo:

    def __init__(self,devicesname):
        self.devicesname=devicesname
        tool.init(self,devicesname)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)
        

    def enter_deviceinfo(self):   

        try:
            #先进入设备项目页：1.点击首页的设备--设置-设备信息
            # mainPage.click_app(self)
            mainPage.click_device(self)
            deviceSetting.setting_info(self)
            self.d(text="设备信息").click(timeout=10)

        except Exception as e:
            print(e)

        

    def clickWiFi(self):
        self.d(text="Wi-Fi").click()
        self.d(text="更换Wi-Fi").click()

    def rollup(self):
        # self.d.swipe(0.211, 0.581,0.159, 0.173)
        self.d.swipe(0.302, 0.928,0.25, 0.508)

    
    def get_OTAversion(self):
        
        device_version=self.d(textContains="固件版本号").get_text()
        OTA_version=device_version[5:]
        # ota=self.d(index=3).get_text()[5:]
        small_version=self.d(text='固件包版本').sibling(index=1).get_text()


        print("固件版本号"+OTA_version)
        # print("ota"+ota)
        print("固件包版本"+small_version)
        
        if OTA_version!=small_version:
            self.logger.error(f"版本升级失败,OTA大小版本对应不上，大版本={OTA_version}，小版本={small_version}")
            result=f"版本升级失败,OTA大小版本对应不上，大版本={OTA_version}，小版本={small_version}"
            tool.App_Screenshot(self,"OTA失败") 

              
        else:
            self.logger.info(f"OTA升级成功！OTA大版本={OTA_version}，小版本={small_version}")
            print("deviceinfo 获取大版本号")
            # print(OTA_version)
            result=OTA_version
            print(result)

        return result

        # #将结果写入excel表格记录
        # record_time=time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        # tool.write_csv(self,record_time,i+1,result)
    
    def get_modulesVersion(self):
        modulesVersion={}

        # 先获取ota大版本
        # OTAversion=deviceInfo.get_OTAversion(self)
        OTAversion=self.get_OTAversion()
        print("deviceinfo   get_modulesVersion######")
        # print(type(OTAversion))
        # print(OTAversion)
        modulesVersion['固件版本号']=OTAversion

        # 先拖动界面，展示所有的版本信息
        time.sleep(2)
        deviceInfo.rollup(self)
        time.sleep(2)
        # print("version-----------")
        
        getallRightVersion=self.d(index=5).get_text()
        print(getallRightVersion)
        T31_version=self.d(text='猫眼版本').sibling(index=1).get_text()
        wifi_version=self.d(text='Wi-Fi版本').sibling(index=1).get_text()
        # print(T31_version)
        # print(wifi_version)
        modulesVersion['猫眼版本']=T31_version
        modulesVersion['Wi-Fi版本']=wifi_version
        # print(modulesVersion)

        lock_version=self.d(text="主控固件版本").sibling(index=1).get_text()
        ble_version=self.d(text='蓝牙固件版本').sibling(index=1).get_text()
        # print(lock_version)
        # print(ble_version)
        modulesVersion['主控固件版本']=lock_version
        modulesVersion['蓝牙固件版本']=ble_version

        
        face_version=self.d(text='面容固件版本').sibling(index=1).get_text()
        finger_print_version=self.d(text='指纹固件版本').sibling(index=1).get_text()
        modulesVersion['面容固件版本']=face_version
        modulesVersion['指纹固件版本']=finger_print_version

        # print(face_version)
        # print(finger_print_version)
        print(modulesVersion)
        return modulesVersion

#从设置里面删除门锁
    def deleteDevice(self,serial_Com,i):
        # 先判断是否门锁已绑定
        bleSpeek.ble_openDoor(self,i)
        if self.d(text="已解锁").exists(15):
            self.logger.info("门锁已绑定账号")
            print("门锁已绑定账号")
            self.reset(self,serial_Com)
            print("门锁解绑完成")
        #在app上删除门锁，否则无法绑定
        deviceSetting.setting_info()
        deviceInfo.enter_deviceinfo()
        deviceInfo.rollup()
        self.d(text="删除").click()
        if self.d(text="删除").exist(3):
            self.d(text="删除").click()
            time.sleep(5)
            self.d(text="我知道了").click()


# if __name__=="__main__":
#     devicesname="V03"
#     deviceinfo=deviceInfo(devicesname)
#     deviceinfo.get_OTAversion()
#     xx=deviceinfo.get_modulesVersion()
#     print(xx)
#     # deviceinfo.enter_deviceinfo()
