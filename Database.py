# # -*- coding: utf-8 -*-
# import pymysql
# #数据库类
# class Database(object):
#     #初始化数据库信息
#     def __init__(self):
#         self.host = 'localhost'
#         self.port = 3306
#         self.user = 'root'
#         self.password = 'root'
#         self.db = 'myscse'
#     #数据库连接
#     def getConn(self):
#         try:
#             self.conn = pymysql.connect(host=self.host,port=self.port,user=self.user,passwd=self.password,db=self.db,charset='uft8')
#             self.cursor = self.conn.cursor()
#         except:
#             print 'connect database error!'
#     #插入数据(table为要插入的表，my_dict是从教务系统爬取的数据组成的字典)
#     def insertData(self,table,my_dict):
#         try:



