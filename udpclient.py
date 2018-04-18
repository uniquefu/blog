#Author:Jeff Lee

import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = ('168.0.20.33', 10021)  # 服务器端地址

#增加链路
msgid =1 #/*消息ID*/
sid=2	#/*会话ID*/
len=3	#/*消息长度*/
uid=4	#/*用户标示*/
token=5	#/*token值*/
netid=6	#/*添加的IP地址和网络类型*/
band=7	#/*增加链路最大打开要求*/

format1 = 'iiiiiBi'
data= 'msgid,sid,len,uid,token,path,band'

while True:
    data = input('请输入要处理的数据:')  # 获得数据
    if not data or data == 'quit':
        break
    data =struct.pack(format1,msgid,sid,len,uid,token,netid,band)
    s.sendto(data, addr)  # 发送到服务端
    recvdata, addr = s.recvfrom(1024)  # 接收服务器端发来的数据
    print(recvdata.decode('utf-8'))  # 解码打印

s.close()  # 关闭socket