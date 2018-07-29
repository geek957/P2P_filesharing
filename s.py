import hashlib
import socket
import os
import re
import time
import stat
port = 60000
host = "akhilralla"
exit=False


class Server:
    def __init__(self):
        self.s=socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
    def md5(self,fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    def runall(self):
        print "server listening..."
        self.s.listen(5)
        self.conn, self.addr = self.s.accept()
        self.data = self.conn.recv(1024)
        self.data=self.data.split()
#print len(self.data)
        if len(self.data)==0:
            return
        elif self.data[0]=='download':
            if len(self.data)!=3:
                print "INVALID COMMAND"
            elif self.data[1]=='UDP':
                if os.path.exists(self.data[2])==False:
                    print "File not exists"
                    return
                self.conn.send(str(self.data[2])+' '+str(os.stat(self.data[2]).st_size)+' '+str(time.ctime(os.stat(self.data[2]).st_mtime))+' '+str(self.md5(self.data[2]))+' '+str(oct(stat.S_IMODE(os.lstat(self.data[2]).st_mode)))+' ')
                serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                serverSocket.bind((socket.gethostname(),40000))
                message, clientAddress = serverSocket.recvfrom(1024)
                modifiedMessage = message.upper()
                self.filename=self.data[2]
    	        f = open(self.filename,'rb')
   	        l = f.read(1024)
    	        while (l):
                    serverSocket.sendto(l,clientAddress)
       	            l = f.read(1024)
                serverSocket.sendto(l,clientAddress)
    	        f.close()
                serverSocket.close()
    	        self.conn.close()
            elif self.data[1]=='TCP':
                if os.path.exists(self.data[2])==False:
                    print "File not exists"
                    return
                self.filename=self.data[2]
                self.conn.send(str(self.data[2])+' '+str(os.stat(self.data[2]).st_size)+' '+str(time.ctime(os.stat(self.data[2]).st_mtime))+' '+str(self.md5(self.data[2]))+' '+str(oct(stat.S_IMODE(os.lstat(self.data[2]).st_mode)))+' ')
                f=open(self.filename,'rb')
   	        l = f.read(1024)
    	        while (l):
                    self.conn.send(l)
       	            l = f.read(1024)
    	        f.close()
    	        self.conn.close()
        elif self.data[0]=='index':
            if len(self.data)<2:
                print "INVALID COMMAND"
                self.conn.send("INVALID COMMAND")
            elif  self.data[1]=='longlist':
                for file in os.listdir(os.getcwd()):
                    a=os.stat(file)
                    '''self.conn.send(file)
                    self.conn.send("\t")
                    self.conn.send(str(a.st_size))
                    self.conn.send("\t")
                    if os.path.isfile(file):
                        self.conn.send("file")
                    else:
                        self.conn.send("Directory")
                    self.conn.send("\t")
                    self.conn.send(str(time.ctime(a.st_mtime)))
                    self.conn.send("\n")'''
                    filename=str(file)
                    size=str(a.st_size)
                    if os.path.isfile(file):
                        type="file"
                    else:
                        type="Directory"
                    mtime=str(time.ctime(a.st_mtime))
                    self.conn.send(filename+" "+size+" "+type+" "+mtime+"\n")
                self.conn.close()
            elif self.data[1]=='shortlist' and len(self.data)==4:
                for file in os.listdir(os.getcwd()):
                    a=os.stat(file)
                    mint=time.mktime(time.strptime(' '.join(self.data[2:6]), '%d %m %Y %H:%M:%S'))
                    maxt=time.mktime(time.strptime(' '.join(self.data[6:10]), '%d %m %Y %H:%M:%S'))
                    if mint<os.path.getmtime(file)<maxt:
                        '''self.conn.send(file)
                        self.conn.send("\t")
                        self.conn.send(str(a.st_size))
                        self.conn.send("\t")    
                        if os.path.isfile(file):
                            self.conn.send("file")
                        else:
                            self.conn.send("Directory")
                        self.conn.send("\t")
                        self.conn.send(str(time.ctime(a.st_mtime)))
                        self.conn.send("\n")'''
                        filename=str(file)
                        size=str(a.st_size)
                        if os.path.isfile(file):
                            type="file"
                        else:
                            type="Directory"
                        mtime=str(time.ctime(a.st_mtime))
                        self.conn.send(filename+" "+size+" "+type+" "+mtime+"\n")
                    self.conn.close()
            elif self.data[1]=='regex' and len(self.data)==3:
                reprog=re.compile(' '.join(self.data[2:]).strip())
                for file in os.listdir(os.getcwd()):
                    if reprog.match(file):
                        a=os.stat(file)
                        '''self.conn.send(file)
                        self.conn.send("\t")
                        self.conn.send(str(a.st_size))
                        self.conn.send("\t")
                        if os.path.isfile(file):
                            self.conn.send("file")
                        else:
                            self.conn.send("Directory")
                        self.conn.send("\t")
                        self.conn.send(str(time.ctime(a.st_mtime)))
                        self.conn.send("\n")'''
                        filename=str(file)
                        size=str(a.st_size)
                        if os.path.isfile(file):
                            type="file"
                        else:
                            type="Directory"
                        mtime=str(time.ctime(a.st_mtime))
                        self.conn.send(filename+" "+size+" "+type+" "+mtime+"\n")
                    self.conn.close()
            else:
                print "INVALID COMMAND"
                self.conn.send("INVALID COMMAND")
        elif self.data[0]=='hash':
            if len(self.data)<2:
                print "INVALID COMMAND"
                self.conn.send("INVALID COMMAND")
            elif self.data[1]=='checkall':
                for file in os.listdir(os.getcwd()):
                    '''self.conn.send(file)
                    self.conn.send("\t")
                    self.conn.send(self.md5(file))
                    self.conn.send("\t")
                    self.conn.send(str(time.ctime(os.stat(file).st_mtime)))
                    self.conn.send("\n")'''
                    self.conn.send(str(file)+' '+str(self.md5(file))+' '+str(time.ctime(os.stat(file).st_mtime))+' ')
                self.conn.close()
            elif self.data[1]=='verify' and len(self.data)==3:
                '''self.conn.send(self.data[2])
                self.conn.send("\t")
                self.conn.send(self.md5(self.data[2]))
                self.conn.send("\t")
                self.conn.send(str(time.ctime(os.stat(self.data[2]).st_mtime)))
                self.conn.send("\n")'''
                self.conn.send(str(self.data[2])+' '+str(self.md5(self.data[2]))+' '+str(time.ctime(os.stat(self.data[2]).st_mtime))+' ')
                self.conn.close()
            else:
                print "INVALID COMMAND"
                self.conn.send("INVALID COMMAND")
        elif self.data[0]=='getfileslist':
            ata=''
            for file in os.listdir(os.getcwd()):
                '''self.conn.send(str(file))
                self.conn.send("\t")
                self.conn.send(str(self.md5(file)))'''
                self.conn.send(str(file)+' '+str(self.md5(file))+' ')
            self.conn.send(ata)
            self.conn.close()
        elif self.data[0]=='exit':
            global exit
            exit=True
        else:
             print "command not found"
obj=Server()
while exit==False:
    obj.runall()
