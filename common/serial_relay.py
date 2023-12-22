# coding:utf-8
import serial,re
from public.file_operations import FileOperations

# 串口发送HEX数据
class RelaySendPort:
    def strSendPort(self,strCmd, strport="Com4", fTime=0.5):
        try:
            ser = serial.Serial(strport, 9600, timeout=float(fTime))
            if strCmd != "":
                ser.write(strCmd.encode("utf-8"))
            strInfo = ser.readlines()
            ser.close()
            return strInfo
        except:
            raise AssertionError(strport + " open error!")

# 控制继电器发送的数据
class RelayControl(RelaySendPort):
    def __init__(self):
        self.bwriteprint=FileOperations()
    def ControlRelay_Press(self,input,strport,logname=""):
        if str(input) == "79":
            RelaySendPort.strSendPort(self, "O", strport)
            if logname != "":
                self.bwriteprint.bWritePrint(input, logname)
        elif str(input) in ["1", "2", "3"]:
            RelaySendPort.strSendPort(self, "N", strport)
            if logname != "":
                self.bwriteprint.bWritePrint(input, logname)
        elif str(input) in ["4", "5", "6"]:
            RelaySendPort.strSendPort(self, "M", strport)
            if logname != "":
                self.bwriteprint.bWritePrint(input, logname)
        elif str(input) in ["7", "8", "9"]:
            RelaySendPort.strSendPort(self, "K", strport)
            if logname != "":
                self.bwriteprint.bWritePrint(input, logname)
        elif str(input) in [r"*", "0", r"#"]:
            RelaySendPort.strSendPort(self, "G", strport)
            if logname != "":
                self.bwriteprint.bWritePrint(input, logname)
        elif str(input) == "80":
            RelaySendPort.strSendPort(self, "P", strport)
            if logname != "":
                self.bwriteprint.bWritePrint(input, logname)
        else:
            print("Input fail,pleas input 0到9的数或*或#")
            return False
        return True

#继电器输入
class Lock_Press(RelayControl):
    # 初始化继电器,并点亮屏幕
    def Device_init(self,strport):
        RelayControl.ControlRelay_Press(self, "80", strport) #80开,79关
        RelayControl.ControlRelay_Press(self, "79", strport)

    def Press(self,input,strport,logname):
        RelayControl.ControlRelay_Press(self, input, strport, logname)
        RelayControl.ControlRelay_Press(self, "79", strport)


# 输入密码
class InputPassword(Lock_Press):
    def Input_Password(self, password, strport_1="0", strport_2="0", strport_3="0",logname=""):
        bwriteprint = FileOperations()
        if str(password) == "":
            if logname != "":
                self.bwriteprint.bWritePrint("待输入的数据为空", logname)
        else:
            # if strport_1 !="0":
            #     Lock_Press.Device_init(self, strport_1)  # 初始化继电器
            # if strport_2 != "0":
            #     Lock_Press.Device_init(self, strport_2)  # 初始化继电器
            # if strport_3 != "0":
            #     Lock_Press.Device_init(self, strport_3)  # 初始化继电器
            Lock_Press.Press(self, 1, strport_1, logname)
            for i in str(password):
                if i in ["1", "4", "7", r"*"]:
                    Lock_Press.Press(self, i, strport_1, logname)
                elif i in ["2", "5", "8", "0"]:
                    Lock_Press.Press(self, i, strport_2, logname)
                elif i in ["3", "6", "9", r"#"]:
                    Lock_Press.Press(self, i, strport_3, logname)
                else:
                    bwriteprint.bWritePrint("密码输入失败，找不到输入数字!", logname)

class GetLockLog:
    # 串口抓取数据
    def Get_Lock_Log(self, read, check_flag="actuallyaddpassowrd(\d+)", logname=""):
        bwriteprint = FileOperations()
        #rsp = '\n'.join([item.decode(encoding="utf-8").replace("\r", "").replace("\n", "") for item in read]).replace(' ', '')
        rsp = '\n'.join([str(item).replace(r"\r", "").replace(r"\n'","").replace(r"b'","").replace(r"\x1b","").replace("[0m","").replace("[33m","") for item in read]).replace(" ", "")
        if logname:
            bwriteprint.bWritePrint(rsp, logname)
        seek_result = re.findall(check_flag, rsp)
        if seek_result:
            return True, seek_result[0]
        else:
            return False, []


# if __name__ == "__main__":
for i in range(1,10000):
    import time
    press = RelayControl()
    press.ControlRelay_Press(80,"COM18")
    print("80")
    time.sleep(3)
    press.ControlRelay_Press(79, "COM18")
    print("79")
    time.sleep(3)