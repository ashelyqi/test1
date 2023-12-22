
import time


class deviceSetting:
    
    #进入设备主页
    def lukezhineng(self):
        self.d(text="鹿客智能").click()
    #进入设备设置主页
    def setting_info(self):
        self.d(text='设置').click()

    #进入猫眼配置页面
    def catInfo(self):
        self.d(text="智能猫眼").click()

    #进入猫眼工作模式
    def catWork(self):
        time.sleep(2)
        self.d(textContains="猫眼工作模式").click()
        self.d(text="自定义模式").click(timeout=3)
        self.d(text="设置").click(timeout=3)

    def IRcard(self):
        self.d(text="红外夜视").click()
        time.sleep(3)
        # self.d(text="红外夜视").click()
        self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.View[1]').click()


        

