#!/usr/bin/env python
#coding:utf-8
import web
import os
import time
import datetime
import config
from urllib import quote

web.config.debug = True

# load config file
root = config.root
bin_path = config.bin_path

types = [
    ".h",".cpp",".cxx",".cc",".c",".cs",".html",".js",
    ".php",".java",".py",".rb",".as",".jpeg",".jpg",".png",
    ".gif",".ai",".psd",".mp3",".avi",".rmvb",".mp4",".wmv",
    ".mkv",".doc",".docx",".ppt",".pptx",".xls",".xlsx",
    ".zip",".tar",".gz",".7z",".rar",".pdf",".txt",".exe",
    ".apk"
]

render = web.template.render('template/')

urls = (
    '/favicon.ico',"Ico",
    '/list_(.*)', "Script",
    '/bin_upload(.*)', "Upload",
    '/changetime(.*)', "ChangeTime",
    '/(.*)','Index',
)

class Ico:
    def GET(self):
        return open("static/img/favicon.ico").read()

'''
@purpose: bin文件的上传和删除
@author : damon
'''
class Upload:
    def POST(self, *args, **kw):
        # save a file to disk
        x = web.input(file={})
        #print "bintag, filename:", x.bintag, x.file.filename
        if x.bintag == "" or x.file.filename == "":
            return "<script type=\"text/javascript\">alert(\"参数输入不正确，请检查参数!\"); parent.location.reload();</script>"

        if 'file' in x:
            filepath= x.file.filename.replace('\\','/')     # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]              # splits the and chooses the last part (the filename with extension)
            filename = unicode(filename, "utf8")
            fout = open(os.path.join(bin_path, filename),'wb')    # creates the file where the uploaded file should be stored
            fout.write(x.file.file.read())                  # writes the uploaded file to the newly created file.
            fout.close()                                    # closes the file, upload complete.
        return "<script>parent.location.reload()</script>"

    def DELETE(self, filename):
        try:
            filename = filename.encode('utf-8') 
            #print "Upload filename:", filename
            os.remove(os.path.join(bin_path,filename))
        except:
            return "success" 

'''
@purpose: 改时间脚本的执行
@author : damon
'''
class ChangeTime:
    def POST(self, *args, **kw):
        changetime = web.input()
        return "<script>parent.location.reload()</script>"


class Script:
    def GET(self, filename):
        #script 1: 修改服务器时间
        if filename == "alice.py":
            dt = datetime.datetime.now()
            nowtime = dt.strftime('%Y-%m-%d %H:%M:%S')
            return render.list_time(nowtime)

        #script2:  bin上传修改 
        elif filename == "layout.html":
            listbin = []
            item = os.listdir(bin_path)
            item = sorted(item, key = str.lower)
            for i in item:
                if i[0] == '.' or os.path.isdir(bin_path + i):
                    continue
                temp = {}
                temp['name'] = i 
                temp['type'] = '.' + i.split('.')[-1]
                
                try:
                    types.index(temp['type'])
                except:
                    temp['type'] = "general"


                temp["time"] = time.strftime("%H:%M:%S %Y-%m-%d",
                        time.localtime(os.path.getmtime(bin_path + i))) 
                
                size = os.path.getsize(os.path.join(bin_path ,i))
                if size < 1024:
                    size = str(size) + ".0 B"
                elif size < 1024 * 1024:
                    size = "%0.1f KB" % (size/1024.0)
                elif size < 1024 * 1024 * 1024:
                    size = "%0.1f MB" % (size/1024.0/1024.0)
                else :
                    size = "%0.1f GB" % (size/1024.0/1024.0/1024.0)
                
                temp["size"] = size
                temp["encode"] = quote(i)

                listbin.append(temp)

            return render.list_resconv(listbin)

        else:
            return "hello word"
    '''
    def POST(self, filename):
        changetime = web.input()
        #excute change time script here:

        
        return "<script>parent.location.reload()</script>"  #fresh page eg: F5
    '''



class Index:
    def GET(self,path):
        # list all the files
        if path == '':
            list = []
            item = os.listdir(root)
            item = sorted(item, key = str.lower)
            
            for i in item:
                if i[0] == '.' or os.path.isdir(root + i):
                    continue
                temp = {}
                temp['name'] = i 
                temp['type'] = '.' + i.split('.')[-1]
                
                try:
                    types.index(temp['type'])
                except:
                    temp['type'] = "general"


                temp["time"] = time.strftime("%H:%M:%S %Y-%m-%d",
                        time.localtime(os.path.getmtime(root + i))) 
                
                size = os.path.getsize(os.path.join(root,i))
                if size < 1024:
                    size = str(size) + ".0 B"
                elif size < 1024 * 1024:
                    size = "%0.1f KB" % (size/1024.0)
                elif size < 1024 * 1024 * 1024:
                    size = "%0.1f MB" % (size/1024.0/1024.0)
                else :
                    size = "%0.1f GB" % (size/1024.0/1024.0/1024.0)
                
                temp["size"] = size
                temp["encode"] = quote(i)

                list.append(temp)
            
            return render.layout(list) 
        
        # return a file
        else:
            web.header('Content-Type','application/octet-stream')
            web.header('Content-disposition', 'attachment; filename=%s' % path)
            file = open(os.path.join(root,path))
            size = os.path.getsize(os.path.join(root,path))
            web.header('Content-Length','%s' % size)
            return file.read()
    '''     
    def DELETE(self,filename):
        try:
            filename = filename.encode('utf-8') 
            os.remove(os.path.join(root,filename))
        except:
            return "success" 
    '''

    def POST(self,filename):

        # save a file to disk
        x = web.input(file={})
        
        if 'file' in x:
            filepath= x.file.filename.replace('\\','/')     # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]              # splits the and chooses the last part (the filename with extension)
            filename = unicode(filename, "utf8")
            fout = open(os.path.join(root,filename),'wb')    # creates the file where the uploaded file should be stored
            fout.write(x.file.file.read())                  # writes the uploaded file to the newly created file.
            fout.close()                                    # closes the file, upload complete.
            
        return "<script>parent.location.reload()</script>" 

# start the application
# it's adaptable to both uwsgi start & python start
app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
    
