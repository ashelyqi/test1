# -*- coding: utf-8 -*-

import os
import sys
import datetime
import inspect
import ctypes
import win32api
import win32con
import serial,re,time
import unittest
import threading
from random import randint

#当前时间戳
time_now = str(round(time.time(),3))


today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
time_future = today + datetime.timedelta(days=30)
#当前天23:59:59的时间戳
today_endtime = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
#当前天的30天后23:59:59的时间戳
future_endtime=int(time.mktime(time.strptime(str(time_future), '%Y-%m-%d'))) - 1

#201401010001年时间戳  1388505660

# 时间戳--->日期格式
# now_time = int(time.time())
# now_data_time = time.strftime("%Y%m%d%H%M%S",time.localtime(now_time))
# print(now_data_time)

# 日期格式--->时间戳
# now_time = "20190813000000"
# now_time_stamp = int(time.mktime(time.strptime(now_time,"%Y%m%d%H%M%S")))
# print(now_time)

class Serial_Log:
    def __init__(self, serial_log):
        self.ser = serial.Serial()
        self.ser.port = serial_log
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.parity = "N"
        self.ser.stopbits = 1
        self.ser.timeout = 100
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False

    def start(self):
        while 1:
            try:
                if self.ser.isOpen():
                    pass
                else:
                    self.ser.open()
                    # print " 是否成功打开串口，True or False "
                    # print ser.isOpen();
                return 1
            except:
                print(" serial is already opened by others.  please ensure serial is closed!!! ")
                time.sleep(1)




def init_folder(log_folder):
    pathname = os.getcwd()
#    fname = '%s%s'%(pathname,log_folder)
    if os.path.exists(log_folder):
        print ("---文件已存在--")
        #os._exit(0)
    else:
        os.makedirs(log_folder)
        print ("当前目录下创建LOG文件夹成功")

#os.path.exists('d:/assist')

def init_com(serial_log):
    global ser
    ser = serial.Serial()
    ser.port = serial_log
    ser.baudrate = 115200
    ser.bytesize = 8
    ser.parity = "N"
    ser.stopbits = 1
    ser.timeout = 100
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False



def serial_open():
    while 1:
        try:
            if ser.isOpen():
                pass
            else:
                ser.open()
                #print " 是否成功打开串口，True or False "
                #print ser.isOpen();
            return 1
        except:
            print (" serial is already opened by others.  please ensure serial is closed!!! ")
            time.sleep(1)

#

def get_time_tag():
    localtime = time.strftime('%Y-%m-%d_%H-%M-%S')
    return "[" + localtime + "]:"



# 抓log
def catch_log(log_path, log="", show=1, tag=1):
    # 判断是否显示log
    if show:
        print (log)
    f = open(log_path, "a")
    try:
        # 判断是否加时间标志
        if tag:
            f.write(get_time_tag())
        f.write(log)
    except:
        print ("write log failed !")
    f.close()


def find_word(filename, word, Run_times, log_path_count):
    i = 0
    flag = 1
    while flag:
        f = open(filename, 'r').read();
        if f.find(word) != -1:
            time.sleep(1);
            catch_log(log_path_count, log="pass, " + str(i) + " times test, found target .\n", show=1,tag=1)
            return 1
        else:
            print("try again to find the word")
            time.sleep(10)
            if i < 6:  # 修改检查次数，达到延时多次检查的目的
                i = i + 1
                flag = 1;
            else:
                catch_log(log_path_count, log="fail!!!! " + str(Run_times + 0) + " times test, please check!!!!!.\n",show=1, tag=1)
                return 1




def tag_print(log_path_count,symbol="*",num=110):
    for i in range(1,num):
        catch_log(log_path_count, log=str(symbol),show=0, tag=0)
    catch_log(log_path_count, log="\n", show=0, tag=0)



#串口log
def read_serial_log():
    while(1):
        time.sleep(1)
        buffer = "" + ser.read(ser.inWaiting()).decode(encoding="utf-8").replace("\r", "")#.replace("\n", "")
        #写串口log
        if buffer == "":
            pass
        else:
            catch_log(log_path, log=buffer,show=0, tag=1)


# 下面两函数的目的是杀死线程
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    # else:
    #     catch_log(log_path,log="fail,未知错误")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

# 清空文件操作
def vEmptyFile(strFileName="log.txt"):
    with open(str(strFileName), 'w+') as fl:
        strInfo = fl.read()
        if strInfo != '':
            fl.write('')
    return

#获取当前时间  时间数组
def strGetNowTime():
    now = datetime.datetime.now()
    strTime = now.strftime("%Y-%m-%d %H:%M:%S")
    return strTime


#提示窗口
def vShowForm(strDetails="OK",strTitle="Result"):
    win32api.MessageBox(0,
                        str(strDetails),
                        str(strTitle)+" "+strGetNowTime(),
                        win32con.MB_ICONINFORMATION)



#写文件并选择方式和是否打印写入信息
def bWritePrint(strWriteInfo="",strFileName="log.txt",strWriteWay='a',bIsPrint=True):
    try:
        with open(strFileName,strWriteWay) as fl:
            fl.write(strWriteInfo.replace("\r",""))
        if bIsPrint:
            print (strWriteInfo.strip())
        return True
    except:
        return False



#向固定端口发送指令 返回值为指令反馈数组
def strSendPort(strCmd,serial_Com,fTime=0.5):
    try:
        ser = serial.Serial(serial_Com,9600,timeout=float(fTime))
        if strCmd != "":
            #ser.write(strCmd)
            ser.write(strCmd.encode("utf-8"))
            #print strCmd
        strInfo = ser.readlines()
        #print strInfo
        ser.close()
        return strInfo
    except:
        raise AssertionError(serial_Com+" open error!")


#控制继电器  常断接法的话，  0 表示连接，1表示断开
def ControlRelay(intInput,relay_Com):
    if intInput == "All_right_con":#1111  All_right_con
        strSendPort("O",relay_Com)
        #vShowForm("All On")
    elif intInput == "All_left_con":#0000  All_left_con
        strSendPort("P",relay_Com)
        #vShowForm("All Off")
    elif intInput == "relay1_left_con":#0111
        strSendPort("W",relay_Com)
        #vShowForm("All On")
    elif intInput == "relay2_left_con":#1011
        strSendPort("K",relay_Com)
    elif intInput == "relay3_left_con":  # 1101
        strSendPort("M", relay_Com)
    elif intInput == "relay4_left_con":  # 1110
        strSendPort("N", relay_Com)
    else:
        vShowForm("Input fail,pleas check input!")
        return False
    return True

if __name__ == "__main__":
    serial_Com = "com15"
    log_path ="E:\poweroff-on.log"
    # for i in range(1, 10000):
        # s = randint(3, 120)  # 断电时间随机
        # catch_log(log_path, log="第 "+str(i)+"轮测试，上电---等待 "+str(s)+"s ---断电---等待5s---再上电，循环测试\n")
    print("111111111111")
    ControlRelay("relay2_left_con", serial_Com)
    time.sleep(5)
    ControlRelay("All_right_con", serial_Com)

    time.sleep(8)



