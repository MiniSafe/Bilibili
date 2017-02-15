# coding:utf-8
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import time
import re
import rsa
import json
import urllib
import binascii
import random
from CookieBrowser import CookieBrowser


class Bilibili():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.brow     = CookieBrowser()
        try:
            self.brow.loadCookie(self.username)
        except:
            pass
        self.key      = self.getkey()
    # 获取验证码
    def getVcode(self,filename='vcode.jpg'):
        f=open(filename,'wb')
        f.write(self.brow.read('https://passport.bilibili.com/captcha'))
        f.close()
    # 测试是否登录
    def testLogin(self):
        try:
            return '的个人空间' in re.findall('<title>[\w\W]*?</title>',self.brow.read('http://space.bilibili.com'))[0][7:-8]
        except :
            return False
    # 获取登录需要的一些信息
    def getLoginInfo(self):
        return json.loads(self.brow.read('https://passport.bilibili.com/login?act=getkey'))
    # 加密密码
    def encryptpwd(self,passwd, hash):
        password = hash['hash'] + passwd
        pub_key = hash['key']
        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
        message = rsa.encrypt(str(password), pub_key)
        message = binascii.b2a_base64(message)
        return message
    # 获取某没卵用判断是否登录的key
    def getkey(self):
        return json.loads(self.brow.read('https://passport.bilibili.com/qrcode/getLoginUrl'))['data']['oauthKey']
    # 登录
    def login(self,vcode):
        password=self.encryptpwd(self.password,self.getLoginInfo())
        print password
        postdata=urllib.urlencode({
            'act':'login',
            'gourl':'https://passport.bilibili.com/login',
            'keeptime':'2592000',
            'pwd':password,
            'userid':self.username,
            'vdcode':vcode.upper()
        })
        print postdata
        try:
            self.brow.rawpost('https://passport.bilibili.com/login/dologin',postdata)
            return self.testLogin()
        except:
            return self.testLogin()
        finally:
            self.brow.saveCookie(self.username)
    # 随机数
    def random(self,num=16):
        return ''.join([str(random.randint(0,9)) for x in xrange(num)])
    # 获取你关注的更新
    def getFollow(self,pageLength=10,pageNumber=1):
        reptime=str(time.time()).replace('.','')
        addr='http://api.bilibili.com/x/feed/pull?callback=jQuery1720'+self.random(16)+'_'+reptime+'0&jsonp=jsonp&ps='+str(pageLength)+'&pn='+str(pageNumber)+'&type=0&_='+reptime+'9'
        ret=self.brow.read(addr)
        ret=ret[ret.index('(')+1:-1]
        return json.loads(ret)
    # 回复某帖子
    def reply(self,aid,message):
        postdata=urllib.urlencode({
            'oid'    :aid,
            'type'   :'1',
            'message':message,
            'plat'   :'1',
            'jsonp'  :'jsonp'
        })
        try:
            string=json.loads(self.brow.open('http://api.bilibili.com/x/v2/reply/add',postdata).read())['message']
            if string == "":
                return True
            return string
        except:
            return False
    # 回复帖子里的回复
    def replyReply(self, aid, rid_f, rid_s, message):
        postdata=urllib.urlencode({
            'oid'    :aid,
            'type'   :'1',
            'root':rid_f,
            'parent':rid_s,
            'message':message,
            'plat'   :'1',
            'jsonp'  :'jsonp'
        })
        try:
            if json.loads(self.brow.open('http://api.bilibili.com/x/v2/reply/add',postdata).read())['message'] == "":
                return True
        except:
            return False
    # 点赞
    def fabulous(self, aid, rid):
        postdata = urllib.urlencode({
            'oid': aid,
            'type': '1',
            'rpid':rid,
            'action': '1',
            'jsonp': 'jsonp'
        })
        try:
            if json.loads(self.brow.open('http://api.bilibili.com/x/v2/reply/add',postdata).read())['message'] == "":
                return True
        except:
            return False
    # 投币
    def coin(self,aid,num=1):
        postdata=urllib.urlencode({
            'aid':aid,
            'rating':'100',
            'player':'1',
            'multiply':num
        })
        return self.brow.open('http://www.bilibili.com/plus/comment.php',postdata).read()=='OK'
    # 获取回复
    def getReply(self,aid,pagenum=1):
        reptime = str(time.time()).replace('.', '')
        url='http://api.bilibili.com/x/v2/reply?callback=jQuery1720'+self.random(16)+'_'+reptime+'0&jsonp=jsonp&pn='+str(pagenum)+'&type=1&oid='+str(aid)+'&sort=0&_='+reptime+'9'
        data=self.brow.read(url)
        data=data[data.index('(')+1:-1]
        return json.loads(data)
    # 获取回复数
    def getReplyNum(self,aid):
        return self.getReply(aid)['data']['page']['acount']
    # 获取评论列表
    def getList(self,pageNumber=1):
        reptime = str(time.time()).replace('.', '')+'0'
        return json.loads(self.brow.read('http://space.bilibili.com/ajax/Bangumi/getList?mid=13071886&page='+str(pageNumber)+'&_='+reptime))['data']
    # 获取评论数量
    def getListCount(self):
        return self.getList()['count']
    # 握草，后面三个函数忘了干嘛的了。。。不要相信标注
    def getListContent(self,pageNumber=1):
        return self.getList(pageNumber)['result']
user=Bilibili('username','password')
print user.testLogin()
if not user.testLogin():
    user.getVcode()
    vcode = raw_input('vcode:')
    print user.login(vcode)
aidlist=[]
count=0
while True:
    print count
    count+=1
    for x in xrange(10):
        for dic in user.getFollow(pageNumber=x)['data']['feeds']:
            dic=dic['addition']
            if not dic['aid'] in aidlist:
                print dic['aid'],dic['title'],dic['author'],dic['create']#,user.reply(dic['aid'],'水个帖子,没什么礼物，我就祝大家鸡年大吉吧')
                time.sleep(1)
                aidlist.append(dic['aid'])
        time.sleep(5)
user.getReplyNum('8114028')
