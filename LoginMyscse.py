#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys
import requests
#设置编码
#初始化要用到的信息，这里先手动输入学号和密码，后期从微信端获取


url = 'http://class.sise.com.cn:7001/sise/'
postUrl = 'http://class.sise.com.cn:7001/sise/login_check_login.jsp'
mainUrl = 'http://class.sise.com.cn:7001/sise/module/student_states/student_select_class/main.jsp'
s = requests.session()
cookies = {}
#获取各个页面链接

class Login:
    # def __init__(self):
    #     global cookies
    #def __init__(self):
    response = s.get(url)
    def getcookie(self):
        cookies['JSESSIONID'] = self.response.cookies.get('JSESSIONID')
        return cookies
    def loginmyscse(self,number,password):
        # 下载页面，并解析 使用requests模块自动管理cookie
        soup = BeautifulSoup(self.response.text, 'lxml')
        hidElemAttr = soup.select('input')[0].attrs.values()
        randomElemAttr = soup.select('#random')[0].attrs.values()
        # 拿到表单中隐藏的数据
        hidElemName = hidElemAttr[1]
        hidElemValue = hidElemAttr[2]
        randomElemName = randomElemAttr[3]
        randomElemValue = randomElemAttr[2]
        # 封装POST数据
        data = {
            'username': number,
            'password': password,
            hidElemName: hidElemValue,
            randomElemName: randomElemValue,
        }
        # 提交表头，参数是各个浏览器的信息。模拟成浏览器访问网页
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3218.0 Safari/537.36',
        }
        # 模拟登录系统
        res = s.post(postUrl, data=data, headers=header)
        return res.text

    def getHtml(self,cookies):
        response = s.get(mainUrl, headers=headers, cookies=cookies)
        soup = BeautifulSoup(response.text, 'lxml')
        clickElem = soup.select('td[onclick]')
        clickHtml = []
        for i in range(len(clickElem)):
            halfUrl = clickElem[i].attrs.values()[3].split("'")[1]
            if halfUrl[0] == '/':
                clickHtml.append('http://class.sise.com.cn:7001' + halfUrl)
            else:
                clickHtml.append('http://class.sise.com.cn:7001' + halfUrl[14:])
        print cookies
        return clickHtml


#获取学生信息表头。模拟成浏览器访问，Referer代表从哪个页面链接过来的。
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3218.0 Safari/537.36',
    'Referer':'http://class.sise.com.cn:7001/sise/module/student_states/student_select_class/main.jsp',
}







