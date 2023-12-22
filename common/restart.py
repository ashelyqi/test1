# -*- coding: utf-8 -*-
 
import random
import time

from common.tool import tool, cin_passwd


class restart:

    def __init__(self, device_name,strPort):
        # tool.init(self, device_name)
        for i in range(10000):
            try:
                self.upAndDown(i + 1,strPort)
            except Exception as e:
                print(e)

    def upAndDown(self,i,strPort):
        cin_passwd(79,strPort)
        print("开始上电...")
        x = random.randrange(5, 15)
        time.sleep(x)
        print("上电等待" + str(x) + "秒...")
        cin_passwd(80,strPort)
        print("下电...等待5s")
        time.sleep(5)
        print("第" + str(i) + "次上下电结束-----")
        return x