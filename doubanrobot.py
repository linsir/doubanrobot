#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-03-20 18:17:54
# @Author  : Linsir (root@linsir.org)
# @Link    : http://linsir.org
# @Version : 0.2

import requests
import requests.utils
import pickle
import json
import re
import random
import logging

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

email = 'username@email.com'
password = 'password'
cookies_file = 'cookies.txt'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='doubanrobot.log',
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-2s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class DoubanRobot:
    '''
    A simple robot for douban.com
    '''
    def __init__(self):
        self.email = email
        self.password = password
        self.ck = None
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
        if not self.load_cookies():
            if self.login():
                self.get_ck()
        else:
            self.get_ck()

    def load_cookies(self):
        '''
        load cookies from file.
        '''
        try:
            with open(cookies_file) as f:
                self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            return True
        except Exception, e:
            logging.error('faild to load cookies from file.')
            return False

    def save_cookies(self):
        '''
        save cookies to file.
        '''
        with open(cookies_file, 'w') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
        logging.info('save cookies to file.')

    def get_ck(self):
        '''
        open douban.com and then get the ck from html.
        '''
        cookies = self.session.cookies.get_dict()
        # r = self.session.get('http://httpbin.org/get',)
        r = self.session.get('https://www.douban.com',)
        if r.cookies.get_dict():
            logging.info('cookies is end of date, login again')
            self.login()
            self.get_ck()
        if cookies.has_key('ck'):
            self.ck = cookies['ck'].strip('"')
            logging.info("ck:%s" %self.ck)
        else:
            logging.error('cannot get the ck. ')

    def login(self):
        '''
        login douban.com and save the cookies to file.
        '''
        # url = 'http://httpbin.org/post'
        r = self.session.post(self.login_url, data=self.data,)
        html =  r.text
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
            logging.info('login successfully!')
        else:
            logging.error('Faild to login, check username and password and captcha code.')
            return False
        return True

    def new_topic(self, group_id, title, content='Post by python'):
        '''
        use the ck pulish a new topic on the douban group.
        '''
        if not self.ck:
            logging.error('ck is invalid!')
            return False
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
            logging.info('Okay, new_topic: %s post successfully !'%title)
            return True
        return False

    def talk_status(self, content='Hello.it\'s a test message using python.'):
        '''
        talk a status.
        '''
        if not self.ck:
            logging.error('ck is invalid!')
            return False

        post_data = {
            'ck' : self.ck,
            'comment' : content,
            }

        self.session.headers["Referer"] = "https://www.douban.com/"
        r = self.session.post("https://www.douban.com/", post_data,)
        if r.status_code == 200:
            logging.info('Okay, talk_status: %s post successfully !'%content)
            return True

    def send_mail(self, id ,content = 'Hey,Linsir !'):
        '''
        send a doumail to other.
        '''
        if not self.ck:
            logging.error('ck is invalid!')
            return False

        post_data = {
           "ck" : self.ck,
           "m_submit" : "好了，寄出去",
           "m_text" : content,
           "to" : id,
           }
        self.session.headers["Referer"] = "https://www.douban.com/doumail/write"
        r = self.session.post("https://www.douban.com/doumail/write", post_data,)
        if r.status_code == 200:
            logging.info('Okay, send_mail: To %s doumail "%s" successfully !'%(id, content))
            return True
    def sofa(self,
            group_id,
            content=['丫鬟命，公主心，怪不得人。',
                    '要交流就平等交流，弄得一副跪舔样,谁还能瞧得起你？',
                    '己所欲，勿施于人..',
                    '人在做，天在看.',]
            ):
        '''
        Randomly select a content and reply a topic.
        '''
        if not self.ck:
            logging.error('ck is invalid!')
            return False

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
                if r.status_code == 200:
                    logging.info('Okay, send_mail: To %s doumail "%s" successfully !'%(id, content))
        return True

    def get_joke(self):
        '''
        get a joke from http://www.xiaohuayoumo.com/
        '''
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
        logging.info('get a joke from http://www.xiaohuayoumo.com/')
        return title, content


def save_html(name, data):
    with open(name, 'w') as f:
        f.write(data)

if __name__ == '__main__':
    app = DoubanRobot()
    # app.login()
    titile, content = app.get_joke()
    # print content
    # if titile and content:
    #     print app.new_topic("cd", titile, content)
    app.talk_status()
    app.send_mail(63666378)
    # app.sofa("CentOS")

