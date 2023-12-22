class mainPage:
    
    #进入app
    def click_app(self):
        self.d(resourceId="com.miui.home:id/icon_icon", description="鹿客管家").click()

    #进入设备详情页
    def click_device(self):
        self.d(text='鹿客智能').click()
    
    #进入我的主页
    def click_myPage(self):
        self.d(text='我的').click()
        