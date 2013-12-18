#coding=utf-8
import ConfigParser
import os
import pymongo
import Tools

class LogProcess:
    tools = Tools.Tools();
    bakDir = "bak/"
        
    def __init__(self):
        config = ConfigParser.ConfigParser();
        f = open("config.ini","r");
        config.readfp(f)
        f.close();
        self.logroot = config.get("LOG","LOGROOT")
        self.host = config.get("COMMON","DBHOST")
        self.port = int(config.get("COMMON","DBPORT"))
 
    

    def processResource(self,subPath,baseFile,className):
        fullPath = self.logroot+subPath;
        l = os.listdir(fullPath);
        for item in l:
            if(item.__len__() <= baseFile.__len__()):
                continue;
            itemFile =  open(self.logroot+subPath+item);
            lines = itemFile.readlines();
            itemFile.close();
            posts = []
            for line in lines:
                if not line.strip():
                    continue;
                post = self.__getResourceArray(line,className);
                posts.append(post);
            if posts.__len__()>0:
                con = pymongo.Connection(self.host,self.port);
                db = con.mining;
                if(subPath.startswith("spar")):
                    db.log_spar.insert(posts);
                elif(subPath.startswith("bindspar")):
                    db.log_bindspar.insert(posts);
                elif(subPath.startswith("gold")):
                    db.log_gold.insert(posts);
                elif(subPath.startswith("honor")):
                    db.log_honor.insert(posts);
                elif(subPath.startswith("sparother")):
                    db.log_sparother.insert(posts);
                elif(subPath.startswith("resource")):
                    db.log_resource.insert(posts);
            src = fullPath+item
            dst = fullPath+self.bakDir 
            self.tools.moveFile(src, dst,item);
            print "processResource";

    def __getResourceArray(self,line,className):
        post = {}
        post["_class"] = className
        arr = line.split('#')
        arrLen = len(arr);
        allServer = arr[1].split('_');
        post["version"] = arr[0]
        post["yx"] = allServer[0]
        post["serverFlag"] = allServer[1]
        post["playerId"] = arr[3]
        post["playerName"]=arr[4]
        post["userId"] = arr[5]
        post["lv"] = arr[6]
        post["addType"] = arr[7]
        post["resourceType"] = arr[8]
        post["amount"] = arr[9]
        post["cause"] = arr[10]
        post["component"] = arr[11]
        post["time"] = self.tools.strTimeToMills(arr[2])
        post["other"] = "";
        if(arrLen>=13):
            post["other"] = arr[12];
        return post;


    def processLoginSpan(self):
        subPath = "loginspan/"
        baseFile = "loginspan.log"
        className = "cn.conjs.game.web.persistence.domain.LogLoginSpan"
        tools = Tools.Tools();
        fullPath = self.logroot+subPath;
        l = os.listdir(fullPath)
        for item in l:
            if(item.__len__() <= baseFile.__len__()):
                continue;
            itemFile =  open(self.logroot+subPath+item);
            lines = itemFile.readlines();
            itemFile.close()
            posts = []
            for line in lines:
                if not line.strip():
                    continue;
                post = {}
                arr = line.split('#')
                allServer = arr[1].split('_');
                post["_class"] = className
                post["version"] = arr[0]
                post["yx"] = allServer[0]
                post["serverFlag"] = allServer[1]
                post["playerId"] = arr[3]
                post["playerName"]=arr[4]
                post["openId"] = arr[5]
                post["minute"] = arr[6]
                post["ip"] = arr[7]
                post["time"] = tools.strTimeToMills(arr[2])
                posts.append(post)
            if posts.__len__() >0 :
                con = pymongo.Connection(self.host,self.port);
                db = con.mining
                db.log_loginspan.insert(posts)
            self.tools.moveFile(fullPath+item, fullPath+self.bakDir,item);

    def processBindSpar(self):
        subPath = "bindspar/"
        baseFile = "bindspar.log"
        className = "cn.conjs.game.web.persistence.domain.LogResource"
        self.processResource(subPath,baseFile,className);
        print "processBindSpar";
        
    def processSpar(self):
        subPath = "spar/"
        baseFile = "spar.log"
        className = "cn.conjs.game.web.persistence.domain.LogResource"
        self.processResource(subPath,baseFile,className);
        print "processSpar";
    def processGold(self):
        subPath = "gold/"
        baseFile = "gold.log"
        className = "cn.conjs.game.web.persistence.domain.LogResource"
        self.processResource(subPath,baseFile,className);
        print "processGold";
    def processHonor(self):
        subPath = "honor/"
        baseFile = "honor.log"
        className = "cn.conjs.game.web.persistence.domain.LogResource"
        self.processResource(subPath,baseFile,className);
        print "processHonor";
    def processSparOther(self):
        subPath = "sparother/"
        baseFile = "sparother.log"
        className = "cn.conjs.game.web.persistence.domain.LogResource"
        self.processResource(subPath,baseFile,className);
        print "processSparOther";
    def processItem(self):
        subPath = "resource/"
        baseFile = "resource.log"
        className = "cn.conjs.game.web.persistence.domain.LogResource"
        self.processResource(subPath,baseFile,className);
        print "processItem";
    def processOnline(self):
        subPath = "online/"
        baseFile = "online.log"
        cname = "cn.conjs.game.web.persistence.domain.LogOnline"
        fullPath = self.logroot+subPath;
        l = os.listdir(fullPath)
        for item in l:
            if(item.__len__() <= baseFile.__len__()):
                continue;
            itemFile =  open(self.logroot+subPath+item);
            lines = itemFile.readlines();
            itemFile.close()
            content = ""
            for line in lines:
                if not line.strip():
                    continue;
                arr = line.split('#')
                arrLen = len(arr);
                if(arrLen<2):
                    continue;
                c = int(arr[1]);
                if c <=0:
                    continue;
                content += line;
                content += ";"
                
            if content.strip():
                data = {}
                strTime = self.tools.getStrDate(item);
                data["time"] = self.tools.strShortTimeToMills(strTime);
                data["content"] = content;
                data["_class"] = cname
                con = pymongo.Connection(self.host,self.port);
                db = con.mining;
                db.log_online.insert(data);
            self.tools.moveFile(fullPath+item, fullPath+self.bakDir,item);

    def processPay(self):
        return;
        
        


