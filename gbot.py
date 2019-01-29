import sys
import time
import socket 
server="irc.freenode.net" 
botnick="botname"
channel="#channel" 
queue=[]
isClass=False
admins=[':nickname']


def isAdmin(text):
    x=text.split("!")
    if x[0] in admins:
        return True
    else:
        return False


#Establish connection 
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
irc.connect((server,6667)) 
irc.setblocking(False) 
time.sleep(1) 
irc.send("USER "+botnick+" "+botnick+" "+botnick+" :Hello! I am a test bot!\r\n") 
time.sleep(1) 
irc.send("NICK "+botnick+"\n") 
time.sleep(1) 
irc.send("JOIN "+channel+"\n") 

while 1:
    time.sleep(0.1)
    try:
        text=irc.recv(2040)
        print(text)
    except Exception:
        pass
    if text.find("PING")!=-1:
        irc.send("PONG "+text.split()[1]+"\r\n")

    elif text.lower().find(":#quit "+ botnick)!=-1 and isAdmin(text):
        irc.send("PRIVMSG "+channel+" Bye!!\r\n")
        irc.send("QUIT \n")
        break

    elif text.lower().find("#endclass")!=-1 and isAdmin(text):
        isClass=False
        print(isClass)
        irc.send("PRIVMSG "+channel+" :Class is ended.\r\n")

    elif text.lower().find(":hi "+ botnick)!=-1:
        t1=text.split("!")
        irc.send("PRIVMSG "+channel+ " "+ t1[0]+", Hello!\r\n")

    elif text.lower().find("how are you "+ botnick+"?")!=-1:
        t1=text.split("!")
        irc.send("PRIVMSG "+channel+ " "+ t1[0]+", I am a happy bot! Hope you are cheerful too.\r\n")


    elif text.lower().find(":!")!=-1:
        if isClass:
            t1=text.split("!")
            if t1[0] in queue:
                irc.send("PRIVMSG "+channel+" "+t1[0]+", wait for your turn. You are already in the queue.\r\n")
            else:
                #irc.send("PRIVMSG "+channel+" "+t1[0]+", You are added to the queue.\r\n")
                queue.append(t1[0])
        else:
            irc.send("PRIVMSG "+channel+" :No class is going on. Feel free to ask your questions.\r\n")                    

    elif text.lower().find(":next")!=-1 and isAdmin(text):
        if len(queue)>1:
            n=queue.pop(0)
            irc.send("PRIVMSG "+channel+" "+n+", Ask your question. "+queue[0]+", you are next.\r\n")
        elif len(queue)==1:
            n=queue.pop(0)
            irc.send("PRIVMSG "+channel+" "+n+", Ask your question.\r\n")
        else:
            irc.send("PRIVMSG "+channel+" :Noone is in the queue.\r\n")


    elif text.lower().find(":#startclass")!=-1 and isAdmin(text):
        isClass=True
        irc.send("PRIVMSG "+channel+" :Class Started. Raise hands by typing \"!\" to ask any question.\r\n")

     #Syntax: nick #addop
    elif text.lower().find("#addop")!=-1 and isAdmin(text):
        ad=text.split(" ")
        admins.append(ad[-2])
        print(ad[-2]+ " is added as an admin")

    #Syntax: nick #removeopp
    elif text.lower().find("#removeop")!=-1 and isAdmin(text):
        ad=text.split(" ")
        admins.remove(ad[-2])
        print(ad[-2]+ " is removed from admin")


    text=""
input() 
