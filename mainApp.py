# -*- coding: utf-8 -*-
from common.IRcardTest import IRcardTest
from common.SwitchWifi import SwitchWifi
from common.onLineConnect import onLineConnect
from common.onlineTime import onlineTime
from common.bleSpeek import bleSpeek
from common.addDeletePwd import addDeletePwd
from common.boding import boding
from common.restart import restart
from common.OTAupdate import OTAupdate
from common.BLEKeepTime import BLEKeepTime
from common.New_bleSpeek import New_bleSpeek
# 1.蓝牙连接速率及开锁时间（bleSpeek）      
# 2.添加-删除密码（addDeletePwd）
# 3.门锁断电测试 (restart)
# 3.摄像头上下电测试 (restart)·
# 5.直播连接时长+保持时长+连接成功率测试  (onlineTime)
# 6.直播连接成功率测试 (onLineConnect)
# 7.wifi切换测试 (SwitchWifi)-----需要先连接过2个wifi，请在对应的函数下修改wifi1，wifi2的名称
# 8.红外切换测试 (IRcardTest)
# 9.绑定解绑测试 ---------  需要焊线比较麻烦，这个pengqi专门做压测
# 10.OTA挂机测试 ------- 需要门锁大版本是最新版本
# 11.蓝牙长连接保持时长


# ********************************
# 注意：所有脚本都需要门锁是已上锁状态
# 挂机数据在common/Logdir文件夹下
# ********************************
devicename = "peng"
comName = "com17"
a = 5



#挂绑定解绑才需要的，这个变量值是接继电器的串口
serial_Com="com15"

#挂ota才需要修改的配置
if a==10:
    # 测试环境1；正式环境0
    test_Env=1
    #OTA降级版本
    downOTAVersion="1.1.1"
    #测试ota请先设置好最新的OTA版本信息
    OTAversion={}
    OTAversion['固件版本号']='1.1.2'
    OTAversion['猫眼版本']='1.1.2'
    OTAversion['Wi-Fi版本']='1.1.2'
    OTAversion['主控固件版本']='1.0.6.1'
    OTAversion['蓝牙固件版本']='1.0.6.1'
    OTAversion['面容固件版本']='16.4.11.0'
    OTAversion['指纹固件版本']='31.1.9.0'

    # mac：95：48
    uuid="24e1132c7e358ce7f00d1c562256d2f0"

    # 线上锁
    # uuid="755b4343f0eeea8d05db684b67d1d347"

#实现函数
if __name__ == '__main__':
    if a == 1:
        # bleSpeek(devicename)
        New_bleSpeek(devicename)
    elif a == 2:
        # 1 为添加密码，其余int为删除
        testtimes=1000
        addDeletePwd(devicename,testtimes)
    elif a == 3:
        # 3.门锁断电测试 (restart)
        comName="com19"
        testtimes=10000
        restart(comName,testtimes)
    elif a==4:
    # 4.摄像头上下电测试 (restart)
        restart(comName)
    elif a == 5:
        onlineTime(devicename)
    elif a == 6:
        onLineConnect(devicename)
    elif a == 7:
        # 切换的2个wifi，请先让门锁能够成功连上2个wifi
        wifi1="Test_one_2.4G"
        wifi2="软测二组_TPlink_2.4G"
        SwitchWifi(devicename,wifi1,wifi2)
    elif a == 8:
        IRcardTest(devicename)
    elif a == 9:
        boding(devicename,serial_Com)    
    elif a==10:
        OTAupdate(devicename,OTAversion,downOTAVersion,uuid,test_Env)
    elif a==11:
        BLEKeepTime(devicename)
        

