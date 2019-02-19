from requests import get
from json import loads
from re import search
from zipfile import ZipFile
from os import remove
from pathlib import Path
from asyncio import get_event_loop
from threading import Thread
from tkinter import Button,Text,Tk,NORMAL,DISABLED,END

import myGlobal

ver=""
def ver2number(version):
    numberList=version.split(".")
    length=len(numberList)
    if length==1:
        return 0
    number=0
    for i in range(length):
        number+=int(numberList[-i-1])*10**i
    return number
def verCheck(version):
    response=get("https://api.github.com/repos/iawia002/annie/releases/latest")
    response_dict=loads(response.text)
    global ver
    ver=response_dict["tag_name"]
    if ver2number(ver)<=ver2number(version):
        return []
    assets=response_dict["assets"]
    retList=[]
    for Dict in assets:
        temp=[]
        temp.append(Dict["name"])
        temp.append(Dict["browser_download_url"])
        retList.append(temp)
    return retList
def getLink(retList):
    for item in retList:
        flag=search("windows_64",item[0].lower())
        if flag!=None:
            return item[1]
    return "Error"
def unzip(file_name):
    zip_file = ZipFile(file_name)
    for names in zip_file.namelist():
        zip_file.extract(names,"./annie")
    zip_file.close()
async def download(link):
    Annie="./annie/annie.exe"
    AnniePath=Path(Annie)
    if AnniePath.exists():
        remove("./annie/annie.exe")
    raw=get(link)
    temp_file="./temp.zip"
    with open(temp_file,"wb") as f:
        f.write(raw.content)
    unzip(temp_file)
    remove(temp_file)
    f=open("./ver.txt","w")
    f.write(ver)
    f.close()
async def update():
    f=open("./ver.txt","r")
    version=f.read()
    f.close()
    retList=verCheck(version)
    if len(retList)==0:
        return 0
    link=getLink(retList)
    if link=="Error":
        return 1
    await download(link)
    return 0
async def anotherFunc(argList):
    window=argList[0]
    linkButton=argList[1]
    statusShow=argList[2]
    statusShow["state"]=NORMAL
    statusShow.delete(0.0,END)
    statusShow.insert(END,"正在初始化程序")
    statusShow["state"]=DISABLED
    returnCode=await update()
    statusShow["state"]=NORMAL
    if returnCode==1:
        statusShow.delete(0.0,END)
        statusShow.insert(END,"有东西出了问题，请重试")
    else:
        linkButton["state"]=NORMAL
        statusShow.delete(0.0,END)
        statusShow.insert(END,"初始化完成")
    statusShow["state"]=DISABLED
    window.update()
def thread(async_loop,argList):
    async_loop.run_until_complete(anotherFunc(argList))
def refersh(async_loop,window,linkButton,statusShow):
    argList=[window,linkButton,statusShow]
    task=Thread(target=thread,args=(async_loop,argList))
    task.setName("Refersh")
    task.start()
'''
if __name__ == "__main__":
    async_loop=get_event_loop()
    refersh(async_loop)
'''