#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-03-20 18:17:54
# @Author  : Linsir (root@linsir.org)
# @Link    : http://linsir.org
# @Version : 0.1

import requests
import requests.utils
import pickle
import json
import re
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

email = 'xxx@email.com'
password = 'your_passwd'
cookies_file = 'cookies.txt'
 
class douban_robot:

    def __init__(self):
        self.email = email
        self.password = password
        self.data = {
                "form_email": email,
                "form_password": password,
                "source": "index_nav",
                "remember": "on"
        }  
        self.session = requests.Session()
        self.login_url = 'https://www.douban.com/accounts/login'
        self.session.headers = {
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
            "Origin": "https://www.douban.com",
        }
        # self.session.headers = self.headers
        self.load_cookies()
        self.get_ck()

    def load_cookies(self):
        with open(cookies_file) as f:
            self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))

    def save_cookies(self):
        with open(cookies_file, 'w') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

    def get_ck(self):

        cookies = self.session.cookies.get_dict()
        # r = self.session.get('http://httpbin.org/get',)
        r = self.session.get('https://www.douban.com',)
        if r.cookies.get_dict():
            print 'cookies is end of date, login agin'
            self.login()
            self.get_ck()
        if cookies.has_key('ck'):
            self.ck = cookies['ck'].strip('"')
            print "ck:%s" %self.ck
        else:
            print 'cookies is end of date.'

    def login(self):
        url = 'http://httpbin.org/post'
        r = self.session.post(self.login_url, data=self.data,)
        html =  r.text
        # print html
        # save_html('1.html', html)
        # 验证码
        regex = r'<img id="captcha_image" src="(.+?)" alt="captcha"'
        imgurl = re.compile(regex).findall(html)
        if imgurl:
            print "The captcha_image url address is %s" %imgurl[0]
             
            captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
            if captcha:
                vcode=raw_input('图片上的验证码是：')
                self.data["captcha-solution"] = vcode
                self.data["captcha-id"] = captcha.group(1)
                self.data["user_login"] = "登录"

                r = self.session.post(self.login_url, data=self.data)

            # save_html('2.html',r.text)
        if r.url == 'https://www.douban.com/':
            self.save_cookies()
            print 'login successfully!'
        else:
            return False
        return True

    def new_topic(self, group_id, title, content='Post by python'):

        group_url = "https://www.douban.com/group/" + group_id
        post_url = group_url + "/new_topic"
        post_data = {
            'ck':self.ck,
            'rev_title': title ,
            'rev_text': content,
            'rev_submit':'好了，发言',
            }
        r = self.session.post(group_url, post_data)
        if r.url == group_url:
            print 'Okay, new_topic: %s post successfully !'%title
            return True
        return False

    def talk_statuses(self, content='Hello.it\'s a test message using python.'):
        post_data = {
            'ck' : self.ck,
            'comment' : content,
            }

        self.session.headers["Referer"] = "https://www.douban.com/"
        r = self.session.post("https://www.douban.com/", post_data,)

    def send_mail(self, id ,content = 'Hey,Linsir !'):

        post_data = {
           "ck" : self.ck,
           "m_submit" : "好了，寄出去",
           "m_text" : content,
           "to" : id,
           }
        self.session.headers["Referer"] = "https://www.douban.com/doumail/write"
        r = self.session.post("https://www.douban.com/doumail/write", post_data,)

    def sofa(self,
            group_id,
            content=['丫鬟命，公主心，怪不得人。', 
                    '要交流就平等交流，弄得一副跪舔样,谁还能瞧得起你？',
                    '己所欲，勿施于人..',
                    '人在做，天在看.',]
            ):

        group_url = "https://www.douban.com/group/" + group_id +"/#topics"
        html = self.opener.open(group_url).read() 
        topics = re.findall(r'topic/(\d+?)/.*?class="">.*?<td nowrap="nowrap" class="">(.*?)</td>',
                    html, re.DOTALL)

        for item in topics:
            if item[1] == '':
                post_data = {
                        "ck" : self.ck,
                        "rv_comment" : random.choice(content),
                        "start" : "0",
                        "submit_btn" : "加上去"
                }
                self.session.post("https://www.douban.com/group/topic/" + item[0] + "/add_comment#last?", post_data)

    def get_joke(self):
        html = self.session.get('http://www.xiaohuayoumo.com/').text
        result = re.compile(r']<a href="(.+?)">(.+?)</a></div>.+?', re.DOTALL).findall(html)
        for x in result[:1]:
            title = x[1]
            joke_url = 'http://www.xiaohuayoumo.com' + x[0]
            page = self.session.get(joke_url).text
            result = re.compile(r'content:encoded">(.+?)<p.+?</p>(.+?)</div></div></div></div>',
                        re.DOTALL).findall(page)
            for x in result[:1]:
                content = x[0] + x[1]
                content = re.sub(r'</?\w+[^>]*>',' ',content)

        return title, content


def save_html(name, data):
    with open(name, 'w') as f:
        f.write(data)

if __name__ == '__main__':
    app = douban_robot()
    titile, content = app.get_joke()
    # print content
    # if titile and content:
    #     print app.new_topic("cd", titile, content)
    # app.talk_statuses()
    app.send_mail(63666378)
    # app.sofa("CentOS")

