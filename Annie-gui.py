from tkinter import Tk,Label,Entry,Text,Button,messagebox,NORMAL,DISABLED,END,W,E,N,S
from subprocess import PIPE,Popen,CREATE_NO_WINDOW
from asyncio import get_event_loop
from re import search
from signal import SIGTERM
import os

import update
import myGlobal


def main(async_loop):
    whereIsAnnie="./annie/annie"

    def refresh(async_loop):
        update.refersh(async_loop,window,linkBotton,statusShow)
    def changeFlag():
        downButton["state"]=NORMAL
    def linkJudge():
        statusShow["state"]=NORMAL
        link=linkEntry.get()
        if len(link)==0:
            statusShow.delete(0.0,END)
            statusShow.insert(END,"请输入链接后确认")
        else:
            statusShow.delete(0.0,END)
            myGlobal.child=Popen([whereIsAnnie,"-i",link],stdout=PIPE,encoding="utf-8",creationflags=CREATE_NO_WINDOW)
            returnCode=myGlobal.child.poll()
            while returnCode is None:
                line=myGlobal.child.stdout.readline().strip()
                statusShow.insert(END,line+"\n")
                if myGlobal.b_flag==0 and search("Site:",line):
                    myGlobal.b_flag=1
                    changeFlag()
                    myGlobal.link=link
                returnCode=myGlobal.child.poll()
        statusShow["state"]=DISABLED
    def download():
        downloadPath="./download/"
        statusShow["state"]=NORMAL
        version=verEntry.get()
        if len(version)>0:
            arg=[whereIsAnnie,"-o",downloadPath,"-f",version,myGlobal.link]
        else:
            arg=[whereIsAnnie,"-o",downloadPath,myGlobal.link]
        statusShow.delete(0.0,END)
        myGlobal.child=Popen(arg,stdout=PIPE,universal_newlines=True,encoding="utf-8",creationflags=CREATE_NO_WINDOW)
        returnCode=myGlobal.child.poll()
        flag=False
        while returnCode is None:
            line=myGlobal.child.stdout.readline().strip()
            judgeList=line.split()
            if len(judgeList)>0 and not flag:
                judgeFlag=judgeList[0]
                if judgeFlag=='0':
                    flag=True
            if flag:
                statusShow.delete(END+"- 2 lines",END)
                statusShow.insert(END,"\n"+line+"\n")
            else:
                statusShow.insert(END,line+"\n")
            window.update()
            returnCode=myGlobal.child.poll()
        statusShow["state"]=DISABLED
    def on_closing():
        if messagebox.askokcancel("确认", "真的要走吗"):
            if myGlobal.child:
                myGlobal.child.terminate()
            window.destroy()
    '''整个窗口设定
    '''
    window=Tk()
    window.title("Annie")
    window.iconbitmap("zhangyu.ico")
    '''菜单的设定
    menubar为主菜单
    menubar=Menu(window)
    settingmenu=Menu(menubar,tearoff=0)
    '''
    '''Label
    总标题
    '''
    mainLabel=Label(window,
        text="A simple GUI for Annie",
        font=("Arial",20)
        )
    mainLabel.grid(row=0,column=1,columnspan=3)
    '''Link有关
    linkLabel为标签
    linkEntry为链接入口
    linkButton为确认链接
    '''
    linkLabel=Label(window,
        text="输入链接",
        )
    linkLabel.grid(row=1,column=0,columnspan=1)
    linkEntry=Entry(window
        )
    linkEntry.grid(row=1,column=1,columnspan=3)
    linkBotton=Button(window,
        state=DISABLED,
        text="这就是链接",
        command=linkJudge
        )
    linkBotton.grid(row=1,column=4,columnspan=1)
    '''内容输出
    '''
    statusShow=Text(window,
        font=("l",10),
        state=DISABLED,
        width=50
        )
    statusShow.grid(row=2,rowspan=10,column=0,columnspan=5,sticky=W+E+N+S,)
    refreshButton=Button(window,
        text="初始化",
        font=("",10),
        command=lambda:refresh(async_loop)
        )
    refreshButton.grid(row=12,column=0,columnspan=1)
    '''版本选择
    '''
    verLabel=Label(window,
        text="输入所需版本对应代码",
        )
    verLabel.grid(row=12,column=2,columnspan=1,sticky=W)
    verEntry=Entry(window,
        )
    verEntry.grid(row=12,column=3,columnspan=1,sticky=W)
    '''开始下载
    '''
    downButton=Button(window,
        text="下载！",
        font=("",10),
        state=DISABLED,
        command=download,
        )
    downButton.grid(row=12,column=4,columnspan=1,sticky=W)
    window.protocol("WM_DELETE_WINDOW",on_closing)
    if myGlobal.a_flag==1:
        statusShow["state"]=NORMAL
        statusShow.insert(END,"程序需要初始化")
        statusShow["state"]=DISABLED
        myGlobal.a_flag==0
    window.mainloop()
if __name__ == "__main__":
    async_loop=get_event_loop()
    main(async_loop)