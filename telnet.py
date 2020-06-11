##!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telnetlib
import time


#连接到telnet服务器，执行命令 返回一个telnet对象
def conn(host,username,password,port=23,timeout=10):
    username = username.encode('utf-8')
    password = password.encode('utf-8')
    try:
        tn = telnetlib.Telnet(host,port,timeout)
        tn.set_debuglevel(5)
        tn.read_until(b"Username:", timeout=2)
        tn.write(username + b"\n")
        tn.read_until(b"Password:", timeout=2)
        tn.write(password + b"\n")
        tn.write(b"\n")
        time.sleep(1)
        return tn
    except Exception as e:
        print(e)

#拿到tn句柄 执行cmd teturn 命令执行的结果
def exec(tn,cmd):
    cmd = cmd.encode('utf-8')
    if b"dis" not in cmd:
        raise Exception("Disallowed cmd")

    i = True
    output = b""
    tn.write(cmd + b'\n')
    time.sleep(1)
    output += b"\r\n"
    # 输出全部的dis cu内容
    while i:
        # 如果输出是以'---- More ----'结尾，则输入空格换屏
        ret = tn.read_until(b'---- More ----',timeout=5)
        if ret.endswith(b'---- More ----'):
            # 将本次的输出结果去'---- More ----'读入到output中
            output  +=  ret
            #output += swrest.strip(b'\x1b[16D                \x1b[16D')
            tn.write(b' ')
            time.sleep(1)
        else:
            # 不是以'---- More ----'结尾，保存本次输出到output中并结束while循环
            output += ret
            time.sleep(1)
            tn.write(b"\n")
            pass
            i = False
    time.sleep(1)
    output += tn.read_very_eager()
    # 输将结果出
    tn.close()
    return output.decode('utf-8')


def Output(filename,msg):
    with open(filename,"w") as f:
        f.write(msg)

def fmt(res):
    if b'  ---- More ----\x1b[16D                \x1b[16D' in res:
        res = res.replace(b'  ---- More ----\x1b[16D                \x1b[16D',b'')
    elif b'---- More ----\r\x00\r\x00               \r\x00' in res:
        res = res.replace(b'---- More ----\r\x00\r\x00               \r\x00',b'') 
    return res
    '---- More ----\r\r               \r'


def main():
    host = "192.168.254.10"
    username = 'admin'
    password = 'admin123'
    cmd = 'dis cu'
    fname  = r"s5720.cfg"

    tn = conn(host,username,password)
    mild_res = exec(tn,cmd)
    res = fmt(mild_res)

    Output(fname,res)


main()
