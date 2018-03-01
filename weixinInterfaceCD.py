# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import sae.const
import os
import urllib2, json
from lxml import etree


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "lzh"  # 这里改写你在微信公众平台里输入的token
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # sha1加密算法

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data()  # 获得post来的数据
        self.xml = etree.fromstring(str_xml)  # 进行XML解析
        mstype = self.xml.find("MsgType").text
        self.fromUser = self.xml.find("FromUserName").text
        self.toUser = self.xml.find("ToUserName").text
        self.db = web.database(dbn='mysql', port=int(sae.const.MYSQL_PORT), host=sae.const.MYSQL_HOST,
                               db=sae.const.MYSQL_DB, user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS)

        if mstype == "event":
            return self.receiveEvent()
        if mstype == 'text':
            return self.receiveText()

        if mstype == "image":
            return self.receiveImage()

        if mstype == "location":
            return self.receiveLocation();

        if mstype == "voice":
            return self.receiveVoice()

        if mstype == "video":
            return self.receiveVideo()

        if mstype == "link":
            return self.receiveLink()

    def receiveEvent(self):
        event = self.xml.find('Event').text
        if event == "subscribe":
            # content = sae.const.MYSQL_DB
            content = u"怎么现在才关注我们呢！赶紧体验我们带给您的服务吧！"
            self.db.insert('user', openid=4, number=4, password='2344')
            # self.db.query('insert into user (openid) values $id ',vars = {'id':self.fromUser})
            return self.transmitText(content)
        elif event == "unsubscribe":
            content = u"真的要这样离开吗！下一次，我们一定会做的更好！"
            return self.transmitText(content)
        elif event == "CLICK":
            return self.transmitText("我还不知道你点了什么哦,正在开发中呢！")

    def receiveText(self):
        text = self.xml.find("Content").text
        content = u'你发送的是文本，内容为：' + text
        return self.transmitText(content)

    def receiveImage(self):
        try:
            picurl = self.xml.find('PicUrl').text
            content = u"你发送的是图片，地址为：" + picurl
            return self.transmitText(content)
        except:
            content = u"图片识别失败，请尝试重发"
            return self.transmitText(content)

    def receiveVoice(self):
        voice = self.xml.find("MediaId").text
        content = u"你发送的是语音，媒体ID为：" + voice
        return self.transmitText(content)

    def receiveVideo(self):
        video = self.xml.find("MediaId").text
        content = u"你发送的是视频，媒体ID为：" + video
        return self.transmitText(content)

    def receiveLocation(self):
        x = self.xml.find("Location_X").text
        y = self.xml.find("Location_Y").text
        scale = self.xml.find("Scale").text
        label = self.xml.find("Label").text
        content = u"你发送的是位置，维度为：" + x + u"；纬度为：" + y + u"；缩放级别为：" + scale + u"；位置为：" + label
        return self.transmitText(content)

    def receiveLink(self):
        title = self.xml.find("Title").text
        description = self.xml.find("Description").text
        url = self.xml.find("Url").text
        content = u"你发送的是连接，标题为：" + title + u"；内容为：" + description + u"；连接地址为：" + url
        return self.transmitText(content)

    def transmitText(self, content):
        return self.render.reply_text(self.fromUser, self.toUser, int(time.time()), content)