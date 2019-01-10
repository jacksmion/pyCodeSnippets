#coding:utf-8
import os
import time
from cStringIO import StringIO
from collections import deque

def BFS_Dir(path):  
    queue = deque() 
    out_buffer = StringIO()
    queue.append(path)
    dir_num = 0
    file_num = 0
    try:
        while True:  
            obj = queue.popleft()  
            if (os.path.isdir(obj)):  
                dir_num += 1
                out_buffer.write(obj + '\n')
                try:
                    for item in os.listdir(obj): 
                        queue.append(os.path.join(obj, item))
                except:
                    pass 
            elif(os.path.isfile(obj)):  
                file_num += 1
                out_buffer.write(obj + '\n') 
    except IndexError:
        pass
    print out_buffer.getvalue()
    out_buffer.close()
    print u"目录数:%s, 文件数:%s" % (dir_num, file_num)
   

start_time = time.time()
b = BFS_Dir(r'F:\jacksmion')  
print u"一共花费了%s" % (time.time() - start_time)