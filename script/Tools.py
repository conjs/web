#coding=utf-8
import time;
import os;

class Tools:
    '''
    字符串时间转毫秒
    '''
    def strTimeToMills(self,t):
        return long(time.mktime(time.strptime(t,'%Y-%m-%d %H:%M:%S')));
    

    '''
    字符串短时间转毫秒
    '''    
    def strShortTimeToMills(self,t):
        return long(time.mktime(time.strptime(t,'%Y-%m-%d')));
    
    
    '''
    毫秒转字符串时间
    '''
    def millsToStrTime(self,t):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t));
    
    '''
    获取文件名的时间部分
    '''
    def getStrDate(self,fileName):
        end = fileName.rfind('.');
        start = end-10;
        return fileName[start:end];
    
    '''
    将某个文件移动到指定文件夹内
    src 源文件
    dist  目录
    f  目标文件
    '''
    def moveFile(self,src,dist,f):
        target = dist+f;
        if not os.path.exists(dist):
            os.mkdir(dist);
        os.rename(src, target);