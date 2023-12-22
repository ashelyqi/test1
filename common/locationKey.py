
import logging
from common.tool import tool
import random

class locationKey:
    def __init__(self,device_name) -> None:
        tool.init(self,device_name)
        #为每个模块创建记录器
        self.logger=logging.getLogger(__name__)

    #进入管理员密码列表
    def adminKey(self):
        if self.d(text="我").exists(15):
            # 给管理员添加密码
            self.d(text="我").click()
            self.d(text="密码").click()
        else:
            result="出现大问题啦啦啦，没有管理员“我”的账号"
            self.logger.error("出现大问题啦啦啦，没有管理员“我”的账号")
            return "出现大问题啦啦啦，没有管理员“我”的账号"

    #管理员钥匙添加
    def adminKeyAdd(self):
                  
        keyAddBtn=self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
        keyAddBtn.click()
        if self.d(textContains="该成员的密码数量满啦").exists(5):
            
            return
        
        numstr=''
        for i in range(6):
            x=random.randint(0,9)
            print(x)
            numstr+=str(x)
        print(numstr)
        self.d(textContains="请输入6~10位开锁密码").sibling(index=1).child(index=0).send_keys(numstr)
        # self.d.xpath('//android.widget.EditText').sendkeys(numstr)
        self.d(text="下一步").click()
        self.d(textContains="请重复输入6~10位开锁密码").sibling(index=1).child(index=0).send_keys(numstr)
        self.d(text="下一步").click()
        if self.d(text="密码添加成功").exists(10):
            print("密码添加成功")
            self.logger.info("密码添加成功")
            self.d(text="完成").click()  
    