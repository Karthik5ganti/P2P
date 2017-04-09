import socket
import os
from datetime import datetime
import hashlib
import re
import threading
import subprocess


host = ""
port = 60004


try:
    log=open("action_log.log","a+");
except:
    print "not able to open log file";
    exit(0);

def create():
    c=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        c.connect((host, port))
    except:
        print "No available server"
        c.close()
        exit(0)

    return c


def compare(start,end,temp):
    timestamp1=temp[2]+" "+temp[3]+" "+temp[4]
    stime=datetime.strptime(start,"%b %d %H:%M")
    etime=datetime.strptime(end,"%b %d %H:%M")
    t1=datetime.strptime(timestamp1,"%b %d %H:%M")
    if stime<=t1 and t1<=etime:
        return 1
    else:
        return 0
def func(var,start="",end="",flag=1):
    var=var.split("\n")
    for i in xrange(0,len(var)-1):
        temp=var[i].split(" ")
        res=0
        if flag==0:
            res=compare(start,end,temp)
        if  res==1 or flag==1:
            if temp[0][0]=='-':
                print "type:file",
            elif temp[0][0]=='d':
                print "type:directory",
            print temp[1]+' '+temp[2]+' '+temp[3]+' '+temp[4]+' '+temp[5]



def update():
    inf=subprocess.check_output('ls -l| sed \'1 d\'| awk \'{print $1" "$5" " $6" " $7" "$8" " $9}\'',shell=True)
    inf=inf.split("\n")
    for i in range(0,len(inf)-1):
        temp=inf[i].split(" ")
        with open(temp[5],'rb') as f:
                    data=f.read()
        md5hash=hashlib.md5(data).hexdigest()
        haash[i]=md5hash

# def main():
count=0
while True:
    c=create();
    print "prompt>",
    arg = raw_input()
    count+=1
    log.write(str(count) + ". " + arg+"\n");
    c.send(arg)
    a = arg.split(' ')
    if a[0]=='index':
        if a[1]== 'longlist':
            b=c.recv(1024)
            func(b)

        if a[1]== 'shortlist':
            b=c.recv(1024)
            start = a[2]+' '+a[3]+' '+a[4]
            end = a[5]+' '+a[6]+' '+a[7]
            func(b,start,end,0)

        if a[1]=='regex':
            c.sendall('longlist')
            data=c.recv(1024)
            data=data.split("\n")
            arr=[]
            for i in range(0,len(data)-1):
                temp=data[1].split(" ")
                arr.append(temp[5])
            pattern=".*"+pattern
            arr1=[]
            for y in arr:
                m=re.matcch(pattern,y)
                if m:
                    t=m.group()
                    arr1.append(t)
            for i in range(0,len(data)-1):
                temp=data[1].split(" ")
                for j in range(0,len(arr1)):
                    if temp[5]==arr1[j]:
                        if temp[0][0]=='-':
                            print "type:file",
                        elif temp[0][0]=='d':
                            print "type:directory",
                        print temp[1]+' '+temp[2]+' '+temp[3]+' '+temp[4]+' '+temp[5]


    if a[0]=='download':
        valid=c.recv(1024)
        print valid
        if valid=='exist':
            if a[1]=='TCP':
                f=open(a[2],'wb')
                length=int(c.recv(16))
                c.send('received')
                temlen=0
                totaldata=""
                while length>temlen:
                    data=c.recv(1024)
                    if not data:
                        break
                    temlen+=len(data)
                    totaldata+=data
                f.write(totaldata)
                f.close()
                c.send('send perm')
                perm=c.recv(1024)
                print perm
                subprocess.call(['chmod', perm, a[1]])
                print('Successfully get the file')
                # else:
                    # print "No such File exists"
            if a[1]=='UDP':
                    nport = int(c.recv(1024))
                    print nport
                    ncs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    addr = (host, nport)
                    ncs.sendto("recieved", addr)
                    try:
                        f = open(a[2], "wb+")
                    except:
                        print "Insufficient Privileges or Space"
                        # return
                    while True:
                        data, addr = ncs.recvfrom(1024)
                        if data == "done":
                            break
                        f.write(data)
                        ncs.sendto("recieved", addr)
                    f.close()
                    ncs.close()
        else:
            print 'No such file exist'
    if a[0]=='exit':
        break

    if a[0]=='hash':
        if a[1]=='verify':
            d=c.recv(1024)
            if d=="error":
                print "no such file exist"
            else:
                print d
                c.send('info')
                temp=c.recv(1024)
                temp=temp.split("\n")
                for i in xrange(0,len(temp)-1):
                    var=temp[i].split(" ")
                    if var[5]==a[2]:
                        print var[2],var[3],var[4]
        if a[1]=='checkall':
            l=int(c.recv(1024))
            c.send('continue')
            for i in range(0,l-1):
                temp=c.recv(1024)
                c.send('sendhash')
                temp=temp.split(" ")
                haash=c.recv(1024)
                print haash," ",
                print temp[5],temp[2],temp[3],temp[4]
    c.close()

    dict1={}
    dict2={}
    c=create()
    c.send('hash checkall')
    l=int(c.recv(1024))
    c.send('continue')
    opp=[]
    for i in range(0,l-1):
        temp=c.recv(1024)
        c.send('sendhash')
        temp=temp.split(" ")
        haash=c.recv(1024)
        dict1[temp[5]]=haash

    c.close()

    inf=subprocess.check_output('ls -l| sed \'1 d\'| awk \'{print $1" "$5" " $6" " $7" "$8" " $9}\'',shell=True)
    inf=inf.split("\n")
    haash=[]
    for i in range(0,len(inf)-1):
        temp=inf[i].split(" ")
        with open(temp[5],'rb') as f:
                    data=f.read()
        md5hash=hashlib.md5(data).hexdigest()
        dict2[temp[5]]=md5hash

    for k in dict1.keys():
        if k in dict2.keys():
            if dict1[k]!=dict2[k]:
                print k + "is updated in the other side"
                c=create()
                c.send("download TCP "+k)
                valid=c.recv(1024)
                if valid=='exist':
                        f=open(k,'wb')
                        length=int(c.recv(16))
                        c.send('received')
                        temlen=0
                        totaldata=""
                        while length>temlen:
                            data=c.recv(1024)
                            if not data:
                                break
                            temlen+=len(data)
                            totaldata+=data
                        f.write(totaldata)
                        f.close()
                        c.send('send perm')
                        perm=c.recv(1024)
                        subprocess.call(['chmod', perm, k])
                        print('Successfully get the file')
                c.close()
        elif k!='server.py':
            print k + " is added in other side"
            c= create()
            c.send('download TCP '+k)
            valid=c.recv(1024)
            if valid=='exist':
                    f=open(k,'wb')
                    length=int(c.recv(16))
                    c.send('received')
                    temlen=0
                    totaldata=""
                    while length>temlen:
                        data=c.recv(1024)
                        if not data:
                            break
                        temlen+=len(data)
                        totaldata+=data
                    f.write(totaldata)
                    f.close()
                    c.send('send perm')
                    perm=c.recv(1024)
                    subprocess.call(['chmod', perm, k])
                    print('Successfully get the file')
            c.close()





# c.close()
