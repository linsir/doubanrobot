#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-04 22:17:10
# @Author  : Linsir (root@linsir.org) | Jimmy66 (root@jimmy66.com)
# @Link    : http://linsir.org | http://jimmy66.com
# @Version : 0.4
import requests
import pickle
import re
from config import *
from utils import xpath_get
from logger import logger

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Auth:
    '''
    A simple robot for douban.com
    '''
    def __init__(self, mail, password):
        self.ck = None
        self.douban_id = None
        self.mail = mail
        self.password = password
        self.session = requests.Session()
        self.login_url = DOUBAN_ACCOUNT_LOGIN
        self.session.headers = {
            "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.3",

            "Origin": DOUBAN_HOME,
        }
        # self.session.headers = self.headers
        if self.load_cookies():
            self.get_ck()
        else:
            self.get_new_cookies()

        if self.check_cookies():
            self.get_ck()
        else:
            self.get_new_cookies()

    def check_cookies(self):
        # r = self.session.get('http://httpbin.org/get',)
        r = self.session.get(DOUBAN_HOME, cookies=self.session.cookies.get_dict())
        # regex = '<input type="hidden" name="ck" value="(.+?)"/>'
        # ck = re.search(regex, r.text)
        xpath_exp = "//form[@name='mbform']/div/input[@name='ck']/@value"
        ck = xpath_get(r.text, xpath_exp)
        headers = dict(r.headers)
        if 'Set-Cookie' in headers:
            self.save_cookies(r.cookies)
        if ck:
            self.ck = ck[0]
            return True
        else:
            self.session.cookies.clear()
            logger.info('Cookies is end of date, login again')
            return False

    def load_cookies(self):
        '''
        load cookies from file.
        '''
        try:
            with open(COOKIES_FILE) as f:
                self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            return True
        except Exception, e:
            logger.error('Faild to load cookies from file. : %s' % e)
            return False

    def get_new_cookies(self):
        if self.login():
            self.get_ck()

    def save_cookies(self, cookies):
        '''
        save cookies to file.
        '''
        if cookies:
            self.session.cookies.update(cookies)
        with open(COOKIES_FILE, 'w') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
        logger.info('Save cookies to file.')

    def get_ck(self):
        '''
        open douban.com and then get the ck from html.
        '''
        cookies = self.session.cookies.get_dict()
        # print(cookies)
        if 'ck' in cookies:
            self.ck = cookies['ck'].strip('"')
            logger.info("ck: %s" % self.ck)
            if 'dbcl2' in cookies:
               self.douban_id = cookies['dbcl2'].strip('"').split(':')[0]
               logger.info("douban_id: %s" % self.douban_id)
        else:
            logger.info('Cookies is end of date, login again')
            self.ck = None
            logger.error('Cannot get the ck. ')

    def login(self):
        '''
        Login douban.com and save the cookies to file.
        '''
        payload = {
            "form_email": self.mail,
            "form_password": self.password,
            "source": "index_nav",
            "remember": "on"
        }
        self.session.cookies.clear()
        # url = 'http://httpbin.org/post'
        r = self.session.post(self.login_url, data=payload, cookies=self.session.cookies.get_dict())
        html = r.text
        if DEBUG:
            save_html("login.html", r.text)
        # 验证码
        # regex = r'<img id="captcha_image" src="(.+?)" alt="captcha"'
        # imgurl = re.compile(regex).findall(html)
        xpath_exp = "//img[@id='captcha_image']/@src"
        imgurl = xpath_get(html, xpath_exp)
        if imgurl:
            logger.info("The captcha_image url address is %s" % imgurl[0])

            # captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
            xpath_exp = "//input[@name='captcha-id']/@value"
            captcha_id = xpath_get(html, xpath_exp)
            if captcha_id:
                vcode = input('图片上的验证码是：')
                payload["captcha-solution"] = vcode
                payload["captcha-id"] = captcha_id[0]
                payload["user_login"] = "登录"

            r = self.session.post(self.login_url, data=payload, cookies=self.session.cookies.get_dict())
            # save_html('2.html',r.text)
        if r.url == DOUBAN_HOME:
            self.save_cookies(r.cookies)
            logger.info('login successfully!')
        else:
            logger.error('Faild to login, check username and password and captcha code.')
            return False
        return True
