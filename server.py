import socket
import os
import subprocess
import hashlib

port = 60004
host = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
print 'Server is Listening to',host,":",port;



while True:
    conn, addr = s.accept()
    data =conn.recv(1024)
    a = data.split(' ')
    print a
    if a[0]=='index':
        if a[1] == 'longlist':
            longlist=subprocess.check_output('ls -l| sed \'1 d\'| awk \'{print $1" "$5" " $6" " $7" "$8" " $9}\'',shell=True)
            conn.send(longlist)
    if a[0]=='download':
        downfile=a[2]
        if os.path.isfile(downfile):
            print "ll"
            conn.send('exist')
            if a[1]=='TCP':
                with open(a[2],'rb') as f:
                        data=f.read()
                l=len(data)
                print l
                conn.sendall('%16d' % l)
                if conn.recv(1024)=='received':
                    conn.sendall(data)
                f.close()
                if(conn.recv(1024)=='send perm'):
                    x=oct(os.stat(a[2]).st_mode & 0777)
                    conn.send(str(x))
                # conn.recv(1024)
            if a[1]=='UDP':
                ncs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                nport = 12345
                ncs.bind((host,nport))
                conn.send(str(nport))
                data, addr = ncs.recvfrom(1024)
                print data
                if data == "recieved":
                    try:
                        f = open(a[2], "rb")
                        byte = f.read(1024)
                        while byte:
                            ncs.sendto(byte, addr)
                            data, addr = ncs.recvfrom(1024)
                            if data != "recieved":
                                break
                            byte = f.read(1024)
                        ncs.sendto("done", addr)
                    except:
                        print "Bad Connection Error"
        else:
            c.send('no')
    if a[0]=='hash':
        if a[1]=='verify':
            try:
                print "here"
                with open(a[2],'rb') as f:
                    data=f.read()
                md5hash=hashlib.md5(data).hexdigest()
                conn.send(md5hash)
                if conn.recv(1024)=='info':
                    inf=subprocess.check_output('ls -l| sed \'1 d\'| awk \'{print $1" "$5" " $6" " $7" "$8" " $9}\'',shell=True)
                    conn.send(inf)
            except:
                 conn.send('error')
        if a[1]=='checkall':
            print 'here'
            inf=subprocess.check_output('ls -l| sed \'1 d\'| awk \'{print $1" "$5" " $6" " $7" "$8" " $9}\'',shell=True)
            inf=inf.split("\n")
            conn.send(str(len(inf)))
            if conn.recv(1024)=='continue':
                for i in range(0,len(inf)-1):
                    temp=inf[i].split(" ")
                    conn.send(inf[i])
                    if conn.recv(1024)=='sendhash':
                        with open(temp[5],'rb') as f:
                            data=f.read()
                        md5hash=hashlib.md5(data).hexdigest()
                        conn.send(md5hash)
conn.close()
s.close()
