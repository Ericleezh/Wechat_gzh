#!/usr/bin/python
# -*- coding: utf-8 -*-
import bs4
import LoginMyscse
from LoginMyscse import Login
from LoginMyscse import headers
from LoginMyscse import s



#爬取学生个人信息 绩点
class StuInfo:
    #soup = parsePage(0)
    def __init__(self):
        self.getInfo()
        self.toStrPersonInfo()
        self.toStrCourseInfo()
    #提取关键信息
    def getInfo(self):
        try:
            cookies = LoginMyscse.Login().getcookie()
            url = Login().getHtml(cookies)[0]  # 具体要爬取个人信息网址
            response = s.get(url, headers=headers, cookies=cookies)
            self.soup = bs4.BeautifulSoup(response.text, 'lxml')
            self.divElem =self.soup.select('div[align="left"]')
            self.adminElem = self.soup.select('td[class="td_left"]')
            self.admin = self.adminElem[8].text.strip()
            self.admin = ''.join(self.admin.split())
            for i in range(len(self.divElem)):
                self.divElem[i] = self.divElem[i].text.strip()
        except:
            return '信息获取失败'
    #个人信息
    def toStrPersonInfo(self):
        str = ""
        str += u'学号:' + self.divElem[2] + '\n'
        str += u'姓名:' + self.divElem[3] + '\n'
        str += u'年级:' + self.divElem[4] + '\n'
        str += u'专业:' + self.divElem[5] + '\n'
        str += u'身份证:' + self.divElem[6] + '\n'
        str += u'邮箱:' + self.divElem[7] + '\n'
        str += u'行政班:' + self.admin + '\n'
        str += u'班主任:' + self.divElem[8] + '\n'
        str += u'辅导员:' + self.divElem[9] + '\n'
        return str

    #获取课程名称 成绩 学分
    def toStrCourseInfo(self):
        cookies = LoginMyscse.Login().getcookie()
        url = Login().getHtml(cookies)[0]  # 具体要爬取个人信息网址
        response = s.get(url, headers=headers, cookies=cookies)
        res = response.text.replace('even', 'odd') #统一所有的tr元素
        soup = bs4.BeautifulSoup(res, 'lxml')
        trElem = soup.select('tr[class="odd"]')

        self.allcourselist = [] #所有课程信息的列表
        self.allcompulsorylist = [] #所有必修课程信息的列表
        self.allelectivelist = []   #所有选修课程信息的列表
        temp = ''
        for i in range(len(trElem)):
            td = trElem[i].select('td')
            for j in range(len(td)):
                td[j] = td[j].text
            self.allcourselist.append(td)
            if len(td) == 10:
                if td[0] != '': #开课学期不为空则拿出来
                    temp = td[0]
                else:
                    td[0] = temp #将开课学期补充
                self.allcompulsorylist.append(td)
            elif len(td) == 9:
                self.allelectivelist.append(td)

        self.str = '必修\n'
        self.str += '课程名称' + '    ' + '成绩' + '    ' + '已得学分\n'
        for i in self.allcompulsorylist:
            if '2017年第一学期' == i[7].encode('utf-8'):
                self.str += i[2].encode('utf-8') + '(' + i[1].encode('utf-8') + ')    ' + i[-2].encode(
                    'utf-8') + '    ' + i[-1].encode('utf-8') + '\n'

        self.str += '\n选修\n'
        self.str += '课程名称' + '    ' + '成绩' + '    ' + '已得学分\n'
        for i in self.allelectivelist:
            if '2017年第一学期' == i[6].encode('utf-8'):
                self.str += i[1].encode('utf-8') + '(' + i[0].encode('utf-8') + ')    ' + i[-2].encode(
                    'utf-8') + '    ' + i[-1].encode('utf-8') + '\n'


        soup = bs4.BeautifulSoup(response.text, 'lxml')
        # 获取当前绩点
        nowGAPElem = self.soup.select('font[color="#FF0000"]')
        nowGAP = nowGAPElem[-1].text
        # 获取学分和成绩
        self.listg = []
        for i in self.allcompulsorylist + self.allelectivelist:
            if i[-1].strip():
                self.listg.append([i[-1].encode("utf-8"), i[-2].encode("utf-8")])
        # 计算绩点
        credit = 0
        score = 0
        for i in self.listg:
            credit += float(i[0])
            tmpStr = i[1].replace("(补)", "")
            if tmpStr == "优":
                score += 95 * float(i[0])
            elif tmpStr == "良":
                score += 85 * float(i[0])
            elif tmpStr == "中":
                score += 75 * float(i[0])
            elif tmpStr == "及格" or tmpStr == "合格":
                score += 65 * float(i[0])
            elif tmpStr == "不及格":
                score += 0 * float(i[0])
            else:
                score += int(tmpStr) * float(i[0])
        calGPA = (score / credit) / 10 - 5

        GAP0 = str(round(calGPA, 1))
        GAP1 = str(round(calGPA, 4))
        GAP = u'当前绩点：' + nowGAP + u'\n预计绩点:' + GAP0 + u'(' + GAP1 + u')\n仅供参考,实际绩点以系统更新为准'

        return self.str+GAP.encode("utf8")

#爬取课程表
class Timetable:
    schedule = []
    complexcourse = []
    course = []
    realcorse = []
    def __init__(self):
        cookies = LoginMyscse.Login().getcookie()
        url = Login().getHtml(cookies)[1]  # 具体要爬取课程表网址
        response = s.get(url, headers=headers, cookies=cookies)
        self.soup = bs4.BeautifulSoup(response.text, 'lxml')
    #提取课程表网页关键信息
    def getSchedule(self):
        try:
            timeElem = self.soup.select('tr[bgcolor="#FFFFFF"] td[align="center"]')
            courseElem = self.soup.select('tr[bgcolor="#FFFFFF"] td[align="left"]')
            rows = len(courseElem) / 7
            for i in range(rows):
                j = i * 7
                time = timeElem[i].text.replace('<br>', '').replace('&nbsp;', '').replace(' ', '')
                mon = courseElem[j].text.replace('&nbsp;', ' ')
                tue = courseElem[j + 1].text.replace('&nbsp;', ' ')
                wed = courseElem[j + 2].text.replace('&nbsp;', ' ')
                thu = courseElem[j + 3].text.replace('&nbsp;', ' ')
                fri = courseElem[j + 4].text.replace('&nbsp;', ' ')
                sat = courseElem[j + 5].text.replace('&nbsp;', ' ')
                sun = courseElem[j + 6].text.replace('&nbsp;', ' ')
                self.schedule.append([time, mon, tue, wed, thu, fri, sat, sun])
            return self.schedule
        except:
            return '信息获取失败'

    def toStrSchedule(self,n):
        lit = self.getSchedule()
        for i in range(len(lit)):
            temp = []
            for j in range(7):
                if lit[i][j + 1].strip() != '':
                    timecourse = lit[i][j + 1] + ' ' + lit[i][0]
                    temp.append(timecourse)
                else:
                    temp.append('')
            self.complexcourse.append(temp)
    #将行列元素转换
        for i in range(7):
            self.course.append([row[i] for row in self.complexcourse])
        for i in range(7):
            temp = []
            for j in range(8):
                if self.course[i][j] != '':
                    temp.append(self.course[i][j])
            self.realcorse.append(temp)
        today = ''
        tomorrow = ''
        for i in self.realcorse[n]:
            today+=i+'\n'
        for i in self.realcorse[n+1]:
            tomorrow+=i+'\n'
        str = ''
        str +=u'今天课程:\n'+today+'--------------\n'+u'明天课表:\n'+tomorrow
        return str

 #爬取考试时间表
class ExamTest:

    def __init__(self):
        cookies = LoginMyscse.Login().getcookie()
        url = Login().getHtml(cookies)[2]  # 具体要爬取考试时间表的网址
        response = s.get(url, headers=headers, cookies=cookies)
        self.res = response.text.replace('even', 'odd')
        self.soup = bs4.BeautifulSoup(self.res, 'lxml')
        self.getExamtable()
        self.toStrExam()
    #获取数据放在二维列表中
    def getExamtable(self):
        try:
            self.examinfo = []
            trElem = self.soup.select('tr[class="odd"]')
            for i in range(len(trElem)):
                tdlist = []
                for j in range(8):
                    tdlist.append(trElem[i].select('td')[j].text)
                self.examinfo.append(tdlist)
        except:
            return '信息获取失败'
    #将拿到的数据转换成字符串
    def toStrExam(self):
        str = ''
        for i in range(len(self.examinfo)):
            str += u'课程名称:' + self.examinfo[i][1] + '(' + self.examinfo[i][0] + ')\n'
            str += u'考试时间:' + self.examinfo[i][2] + '  ' + self.examinfo[i][3] + '\n'
            str += u'    考场:' + self.examinfo[i][4] + '\n'
            str += u'  座位号:' + self.examinfo[i][6] + '\n'
            str += u'    状态:' + self.examinfo[i][7] + '\n\n'
        return  str

 #爬取考勤信息
class Attendance:
     checkinfo = []
     def __init__(self):
         cookies = LoginMyscse.Login().getcookie()
         url = Login().getHtml(cookies)[3]  # 具体要爬取的网址
         response = s.get(url, headers=headers, cookies=cookies)
         self.res = response.text.replace('even', 'odd')
         self.getTest()
         self.toStrAttendance()
     # 获取数据放在二维列表中
     def getTest(self):
         try:
             soup = bs4.BeautifulSoup(self.res, 'lxml')
             trElem = soup.select('tr[class="odd"]')
             for i in range(len(trElem)):
                 tdlist = []
                 for j in range(3):
                     tdlist.append(trElem[i].select('td')[j].text)
                 self.checkinfo.append(tdlist)
             return self.checkinfo
         except:
             return '信息获取失败'

     # 将拿到的数据转换成字符串
     def toStrAttendance(self):
         self.str = u'课程名称:\n'
         for i in range(len(self.checkinfo)):
             if self.checkinfo[i][2] == '':
                 self.checkinfo[i][2] == u'暂无'
             self.str += self.checkinfo[i][1] + u'：' + self.checkinfo[i][2] + '\n'
         return self.str
#爬取学生奖惩情况

#爬取晚归、违规记录
# class Violation:
#     def __init__(self):
#         self.parsePage()
#         self.toStrVio()
#     def parsePage(self):
#         url = getHtml()[-2]  # 具体要爬取的网址
#         response = s.get(url, headers=headers)
#         res = response.text.replace('even', 'odd')
#         soup = bs4.BeautifulSoup(res,'lxml')
#         self.table = soup.find_all("table", attrs={"width": "95%", "class": "table", "align": "center"})
#         self.tr = self.table[0].find_all("tr", attrs={"class": "odd"})
#         self.lit = []
#         n = 0
#         for i in range(int(len(td) / 8)):
#             temp = []
#             for j in range(8):
#                 temp.append(td[n].get_text())
#                 n = n + 1
#             self.lit.append(temp)
#
#     def toStrVio(self):
#         str = ''
#         for i in range(len(self.lit)):
#             for j in range(len(self.lit[i])):
#                 str += self.lit[i][j] + " "
#             str += "\n"
#         return str
