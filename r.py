import socket                   
import hashlib
import os

host = "akhilralla"
port = 60000

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
while True:
    s=socket.socket()             
    files=[]
    p=socket.socket()
    p.connect((host, port))
    p.send('getfileslist')
    while True:
        daa=p.recv(1024)
        if not daa:
            break
        files.append(daa)
    p.close()
    for i in range(0,len(files)):
        Flag=False
        aa=files[i].split()
        string="download"+" "+"TCP"+" "+aa[0]
        if os.path.exists(aa[0])==False:
            Flag=True
            r=socket.socket()
            print aa[0]+' not found updting......'
            r.connect((host, port))
            r.send(string)
        elif str(md5(aa[0]))!=aa[1]:
            Flag=True
            print aa[0]+' is changed updating......'
            r=socket.socket()
            r.connect((host,port))
            r.send(string)
        if Flag==True:
            fileread=r.recv(1024)
            fileread=fileread.split()
            with open(aa[0], 'wb') as f:
                while True:
                    data= r.recv(1024)
                    if not data:
                        break
                        # write data to a file
                    f.write(data)
            f.close()
            os.chmod(aa[0],int(fileread[8],8))
            r.close()
    s.connect((host, port))
    print "command>",
    inp=raw_input("")
    s.send(inp)
    inp=inp.split()
    if len(inp)==0:
        x=1
    elif inp[0]=='exit':
        break
    elif inp[0]=='download':
        if len(inp)!=3:
            print "INVALID COMMAND"
        elif inp[1]=='UDP':
            fileread=s.recv(1024)
            fileread=fileread.split()
            message='a'
            clientsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            clientsocket.sendto(message,(socket.gethostname(), 40000))
            with open(inp[2], 'wb') as f:
                while True:
                    data, serverAddress = clientsocket.recvfrom(1024)
                    if not data:
                        break
                    f.write(data)
            f.close()
            os.chmod(inp[2],int(fileread[8],8))
            clientsocket.close()
            s.close()
        elif inp[1]=='TCP':
            fileread=s.recv(1024)
            fileread=fileread.split()
            with open(inp[2], 'wb') as f:
                while True:
                    data= s.recv(1024)
                    if not data:
                        break
                    f.write(data)
            f.close()
            os.chmod(inp[2],int(fileread[8],8))
            s.close()
    elif inp[0]=='index':
        if len(inp)<2:
            print "INVALID COMMAND"
        while True:
            data=s.recv(1024)
            if not data or data=="INVALID COMMAND":
                break
            print data
        s.close()
    elif inp[0]=='hash':
        while True:
            data=s.recv(1024)
            if not data or data=="INVALID COMMAND":
                break
            print data
            data=data.split()
            for i in range(0,len(data),7):
                if os.path.exists(data[i])==False:
                    print data[i]+" This File Not Exists"
                elif md5(data[i])!=data[i+1]:
                    print data[i]+" This File is changed"
                else:
                    print data[i]+" This file is not changed"
        s.close()
