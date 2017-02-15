# coding:utf-8
import re
import urllib
import urllib2
import cookielib
class CookieBrowser(object):
    # 构造方法，用来传递初值
    def __init__(self):
        self.cookie=cookielib.MozillaCookieJar()
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
    def saveCookie(self,filename):
        self.cookie.save(filename,ignore_expires=True,ignore_discard=True)
    def loadCookie(self,filename):
        self.cookie.load(filename,ignore_expires=True,ignore_discard=True)
    def getCookies(self):
        return self.cookie
    def setCookies(self,cookie):
        self.cookie=cookie
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
    def resetCookies(self):
        self.cookie=cookielib.CookieJar()
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
    def open(self,addr,param):
        return self.opener.open(addr,param)
    def read(self,addr):
        return self.opener.open(addr).read()
    def post(self,url,**param):
        postdata=urllib.urlencode(param)
        return self.opener.open(url,postdata)
    def rawpost(self,url,param):
        return self.opener.open(url,param)
    def hasStr(self,url,parrent):
        return re.findall(parrent,self.read(url))