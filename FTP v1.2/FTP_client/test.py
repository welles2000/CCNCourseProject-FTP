import socket
import optparse
import configparser  #做记录用的模块，用来做文件处理
import json
import zipfile
import os,sys

# 压缩解压
# startdir = '1'  #要压缩的文件夹路径
# file_news = startdir +'.zip' # 压缩后文件夹的名字
# z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
# for dirpath, dirnames, filenames in os.walk(startdir):
#     fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
#     fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
#     for filename in filenames:
#         z.write(os.path.join(dirpath, filename),fpath+filename)
# print ('压缩成功')
# z.close()

# zipDir = '1.zip'
# path = os.path.dirname(os.path.abspath(zipDir))
# file_name = zipDir.split('.')[0]
# print(path)
# print(file_name)
# if os.path.exists(os.path.join(path, file_name)):
#     pass
# else:
#     os.makedirs(os.path.join(path, file_name))
# zip_file = zipfile.ZipFile(zipDir)
# for names in zip_file.namelist():
#     zip_file.extract(names, os.path.join(path, file_name))
# zip_file.close()

# src_target = '1.zip'
# cmd_list = ['mkdir',src_target]
# print(cmd_list[1])


# def lsall(path):
#     nl =[]
#     nll = []
#     file_list = os.listdir(path)
#     for file in file_list:
#         nl.append(os.path.join(path, file))
#     for file in nl:
#         nll.append(file)
#         if os.path.isdir(file):
#             for f in os.listdir(file):
#                 nl.append(os.path.join(file, f))
#     return nll
#
#
# path = '.'
# dic = {}
# str = lsall(path)
# dic['index']=str
# dicJson = json.dumps(dic).encode('utf-8')
# de = json.loads(dicJson.decode('utf-8'))
# n = de.get('index')
# print(type(n))

# filepath1 = "data/outputs/河北省.dddd"
# a = os.path.basename(filepath1)
# b = os.path.dirname(filepath1)
# e = '.'
# print(a)
# print(b)
# if '.' in a:
#     print('isfile')
# else:
#     print('isdir')

# path = '1\\1'
# if not os.path.exists(path):
#     os.makedirs(path)
#     print('create')
# else:
#     print("---  There is a folder!  ---")

# str = 'E:\\university\\computer communication network\\Project\\FTP\\FTP_server\\home\\view\\images\\1'
# print(str)
# print(str.replace('\\',' '))



################# getDir images .


