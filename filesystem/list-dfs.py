#coding:utf-8
import os 
import time 
def DFS_Dir(path, dirCallback = None, fileCallback = None):  
    stack = []  
    ret = []  
    stack.append(path)
    dir_num = 0
    file_num = 0 
    while len(stack) > 0:  
        tmp = stack.pop(len(stack) - 1)  
        if(os.path.isdir(tmp)):
            dir_num += 1  
            ret.append(tmp)
            try:  
                for item in os.listdir(tmp):  
                    stack.append(os.path.join(tmp, item))
            except:
                pass
            if dirCallback:  
                dirCallback(tmp)  
        elif(os.path.isfile(tmp)): 
            file_num += 1
            ret.append(tmp)  
            if fileCallback:  
                fileCallback(tmp) 
    print u"目录数:%s, 文件数:%s" % (dir_num, file_num) 
    return ret  
  
def printDir(path):  
    print "dir: " + path  
  
def printFile(path):  
    print "file: " + path  

start_time = time.time()
d = DFS_Dir(r'F:\jacksmion', printDir, printFile)
print u"一共花费了%s" % (time.time() - start_time)