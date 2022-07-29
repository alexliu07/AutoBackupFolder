import sys,os,time,datetime
import tkinter as tk
from tkinter import filedialog,ttk,messagebox
targetFolder = ''
saveFolder = ''
duration = 0
maxSave = 0
compression = False
firstCopy = False
#错误处理
def error(text):
    messagebox.showwarning(text,text)
#选择要备份文件夹
def selectTargetFolder():
    global foldersel,targetFolder
    targetFolder = filedialog.askdirectory()
    foldersel['state'] = 'normal'
    foldersel.delete(0,'end')
    foldersel.insert(0,targetFolder)
    foldersel['state'] = 'readonly'
#选择要保存文件夹
def selectSaveFolder():
    global sfoldersel,saveFolder
    saveFolder = filedialog.askdirectory()
    sfoldersel['state'] = 'normal'
    sfoldersel.delete(0,'end')
    sfoldersel.insert(0,saveFolder)
    sfoldersel['state'] = 'readonly'
#设置保存
def saveSetting():
    global durationText,duration,iscompress,compression,isfirstcopy,firstCopy,maxSave,maxsaveText
    try:
        duration = int(durationText.get())
        maxSave = int(maxsaveText.get())
        #检测文件夹是否设置
        if targetFolder == '' or saveFolder == '':
            raise IndexError
        if iscompress.get():
            compression = True
        else:
            compression = False
        if isfirstcopy.get():
            firstCopy = True
        else:
            firstCopy = False
        #保存到文件
        file = open('settings.ini','w+',encoding='utf-8')
        file.write(str([targetFolder,saveFolder,duration,maxSave,compression,firstCopy]))
        file.close()
        sys.exit()
    except ValueError:
        error('数字项目未设置或设置值不标准')
    except IndexError:
        error('目标文件夹未设置')
#读取设置
if os.path.exists('settings.ini'):
    file = open('settings.ini','r',encoding='utf-8')
    content = eval(file.read())
    targetFolder = content[0]
    saveFolder = content[1]
    duration = content[2]
    maxSave = content[3]
    compression = content[4]
    firstCopy = content[5]
if sys.argv[1] == 'set':
    #设置模式
    win = tk.Tk()
    win.title('自动备份文件夹 设置模式')
    #备份文件夹选择
    folderseltip = tk.Label(win,text="要备份的文件夹：")
    folderseltip.pack()
    foldersel = tk.Entry(win)
    #载入
    foldersel.delete(0,'end')
    foldersel.insert(0,targetFolder)
    foldersel['state'] = 'readonly'
    foldersel.pack()
    folderselbtn = tk.Button(win,text="浏览",command=selectTargetFolder)
    folderselbtn.pack()
    line1 = ttk.Separator(win,orient=tk.HORIZONTAL)
    line1.pack(padx=10,pady=10,fill=tk.X)
    #保存文件夹选择
    sfolderseltip = tk.Label(win,text="要保存到的文件夹：")
    sfolderseltip.pack()
    sfoldersel = tk.Entry(win)
    #载入
    sfoldersel.delete(0,'end')
    sfoldersel.insert(0,saveFolder)
    sfoldersel['state'] = 'readonly'
    sfoldersel.pack()
    sfolderselbtn = tk.Button(win,text="浏览",command=selectSaveFolder)
    sfolderselbtn.pack()
    line2 = ttk.Separator(win,orient=tk.HORIZONTAL)
    line2.pack(padx=10,pady=10,fill=tk.X)
    #间隔时间设置
    durationtip = tk.Label(win,text="间隔时间(秒)")
    durationtip.pack()
    durationText = tk.Entry(win)
    durationText.delete(0,'end')
    durationText.insert(0,str(duration))
    durationText.pack()
    line3 = ttk.Separator(win,orient=tk.HORIZONTAL)
    line3.pack(padx=10,pady=10,fill=tk.X)
    #压缩确认
    compressiontip = tk.Label(win,text="是否启用压缩")
    compressiontip.pack()
    iscompress = tk.IntVar()
    compressioncheck = tk.Checkbutton(win,variable=iscompress)
    if compression:
        compressioncheck.select()
    compressioncheck.pack()
    line4 = ttk.Separator(win,orient=tk.HORIZONTAL)
    line4.pack(padx=10,pady=10,fill=tk.X)
    #最大保存数量
    maxsavetip = tk.Label(win,text="最大保存数量")
    maxsavetip.pack()
    maxsaveText = tk.Entry(win)
    maxsaveText.delete(0,'end')
    maxsaveText.insert(0,str(maxSave))
    maxsaveText.pack()
    line5 = ttk.Separator(win,orient=tk.HORIZONTAL)
    line5.pack(padx=10,pady=10,fill=tk.X)
    #先复制再压缩
    firstcopytip = tk.Label(win,text="先复制再压缩(对于被其他进程占用的文件有一定作用)")
    firstcopytip.pack()
    isfirstcopy = tk.IntVar()
    firstcopycheck = tk.Checkbutton(win,variable=isfirstcopy)
    if firstCopy:
        firstcopycheck.select()
    firstcopycheck.pack()
    line6 = ttk.Separator(win,orient=tk.HORIZONTAL)
    line6.pack(padx=10,pady=10,fill=tk.X)
    #确认
    submit = tk.Button(win,text="确定",command=saveSetting)
    submit.pack()
    win.mainloop()
elif sys.argv[1] == 'run':
    #检测文件
    if not os.path.exists('settings.ini'):
        print('程序未配置！请使用main.py set以进行配置')
        sys.exit()
    count = 0
    #运行模式
    os.system('echo 自动备份文件夹 运行模式 服务启动！请勿关闭此窗口')
    while True:
        count += 1
        print('正在进行第',count,'次备份')
        #读取文件列表
        if not os.path.exists('files.list'):
            file = open('files.list','w+',encoding='utf-8')
            file.write('[]')
            file.close()
        file = open('files.list','r',encoding='utf-8')
        filelist = eval(file.read())
        file.close()
        if len(filelist) == maxSave:
            if compression:
                os.remove(saveFolder+'/'+filelist[0])
            else:
                os.system('rmdir /S /Q "'+saveFolder+'/'+filelist[0]+'"')
            del filelist[0]
        #读取文件名
        filen = os.path.splitext(os.path.split(targetFolder)[1])[0]
        newfilen = filen+'-'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        #检测是否需要压缩
        if compression:
            #是否先复制
            if firstCopy:
                if not os.path.exists('tmp'):
                    os.mkdir('tmp')
                #复制目标文件夹
                os.system('xcopy /Y /E /I /C "'+targetFolder+'" tmp')
                #压缩
                os.system('7zip\\7za.exe a "'+newfilen+'.zip" tmp/.')
                #复制到目标位置
                os.system('copy "'+newfilen+'.zip" "'+saveFolder+'"')
                #删除源目录
                os.system('rmdir tmp /S /Q')
                os.system('del "'+newfilen+'.zip"')
            else:
                #压缩目标文件夹
                os.system('7zip\\7za.exe a "'+newfilen+'.zip" "'+targetFolder+'/."')
                #复制到目标位置
                os.system('copy "'+newfilen+'.zip" "'+saveFolder+'"')
                #删除源文件
                os.system('del "'+newfilen+'.zip"')
            #添加文件到列表
            filelist.append(newfilen+'.zip')
        else:
            #复制到目标位置
            os.system('xcopy /Y /E /I /C "'+targetFolder+'" "'+saveFolder.replace('/','\\')+'\\'+newfilen+'"')
            filelist.append(newfilen)
        #将列表写入文件
        file = open('files.list','w+',encoding='utf-8')
        file.write(str(filelist))
        file.close()
        time.sleep(duration)