#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-04 22:17:10
# @Author  : Linsir (root@linsir.org) | Jimmy66 (root@jimmy66.com)
# @Link    : http://linsir.org | http://jimmy66.com
# @Version : 0.4

import requests
import requests.utils
import pickle
import json
import re
import random
import logging
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

COOKIES_FILE = 'cookies.txt'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-3s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename='doubanrobot.log',
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)-s %(message)s', datefmt='%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class DoubanRobot:
    '''
    A simple robot for douban.com
    '''
    def __init__(self, account_id, password, douban_id):
        self.ck = None
        self.douban_id = douban_id
        self.data = {
                "form_email": account_id,
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
        if self.load_cookies():
            self.get_ck()
        else:
            self.get_new_cookies()

    def load_cookies(self):
        '''
        load cookies from file.
        '''
        try:
            with open(COOKIES_FILE) as f:
                self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            return True
        except Exception, e:
            logging.error('faild to load cookies from file.')
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
        logging.info('save cookies to file.')

    def get_ck(self):
        '''
        open douban.com and then get the ck from html.
        '''
        # r = self.session.get('http://httpbin.org/get',)
        r = self.session.get('https://www.douban.com/accounts/',cookies=self.session.cookies.get_dict())
        # save_html('1.html', r.text)
        cookies = self.session.cookies.get_dict()
        headers = dict(r.headers)
        if headers.has_key('Set-Cookie'):
            logging.info('cookies is end of date, login again')
            self.ck = None
            self.get_new_cookies()
        elif cookies.has_key('ck'):
            self.ck = cookies['ck'].strip('"')
            logging.info("ck:%s" %self.ck)
        else:
            logging.error('cannot get the ck. ')

    def login(self):
        '''
        login douban.com and save the cookies to file.
        '''
        self.session.cookies.clear()
        # url = 'http://httpbin.org/post'
        r = self.session.post(self.login_url, data=self.data, cookies=self.session.cookies.get_dict())  #核心语句数据从其中传入
        html =  r.text
        # save_html('1.html', html)
        # 验证码
        regex = r'<img id="captcha_image" src="(.+?)" alt="captcha"'
        imgurl = re.compile(regex).findall(html)
        if imgurl:
            logging.info("The captcha_image url address is %s" %imgurl[0])

            captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
            if captcha:
                vcode=raw_input('图片上的验证码是：')
                self.data["captcha-solution"] = vcode
                self.data["captcha-id"] = captcha.group(1)
                self.data["user_login"] = "登录"
                # print 'yes'


            r = self.session.post(self.login_url, data=self.data, cookies=self.session.cookies.get_dict())
            # save_html('2.html',r.text)
        if r.url == 'https://www.douban.com/':
            self.save_cookies(r.cookies)
            logging.info('login successfully!')
        else:
            logging.error('Faild to login, check username and password and captcha code.')
            return False
        return True

    def get_my_topics(self):
        homepage_url = self.douban_id.join(['https://www.douban.com/group/people/','/publish'])
        r = self.session.get(homepage_url).text
        topics_list = re.findall(r'<a href="https://www.douban.com/group/topic/([0-9]+)/', r)
        return topics_list

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
        r = self.session.post(group_url, post_data, cookies=self.session.cookies.get_dict())
        if r.url == group_url:
            logging.info('Okay, new_topic: "%s" post successfully !'%title)
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
        r = self.session.post("https://www.douban.com/", post_data, cookies=self.session.cookies.get_dict())
        # save_html('3.html',r.text)
        if r.status_code == 200:
            logging.info('Okay, talk_status: "%s" post successfully !'%content)
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
        r = self.session.post("https://www.douban.com/doumail/write", post_data, cookies=self.session.cookies.get_dict())
        if r.status_code == 200:
            logging.info('Okay, send_mail: To %s doumail "%s" successfully !'%(id, content))
            return True

    def topics_up(self,
            topics_list,
            content=['顶',
                    '顶帖',
                    '自己顶',
                    'waiting',]
            ):
        '''
        Randomly select a content and reply a topic.
        '''
        if not self.ck:
            logging.error('ck is invalid!')
            return False


        # For example --> topics_list = ['22836371','98569169']
        #topics_list = ['22836371','98569169']
        for item in topics_list:
            post_data = {
                    "ck" : self.ck,
                    "rv_comment" : random.choice(content),
                    "start" : "0",
                    "submit_btn" : "加上去"
            }

            r = self.session.post("https://www.douban.com/group/topic/" + item + "/add_comment#last?", post_data, cookies=self.session.cookies.get_dict())
            if r.status_code == 200:
                logging.info('Okay, already up ' + item + ' topic' )
            print r.status_code
            print str( topics_list.index(item) + 1 ).join(['Waiting for ',' ...'])
            time.sleep(60)  # Wait a minute to up next topic, You can modify it to delay longer time
        return True

   def sofa(self,
            group_id,
            content=['沙发',
                    '顶',
                    '挽尊',]
            ):
        '''
        Randomly select a content and reply a topic.
        '''
        if not self.ck:
            logging.error('ck is invalid!')
            return False

        group_url = "https://www.douban.com/group/" + group_id +"/#topics"
        html = self.session.get(group_url, cookies=self.session.cookies.get_dict()).text
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
                r = self.session.post("https://www.douban.com/group/topic/" + item[0] + "/add_comment#last?", post_data, cookies=self.session.cookies.get_dict())
                if r.status_code == 200:
                    logging.info('Okay, send_mail: To %s doumail "%s" successfully!'%(id, content))
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
    account_id =  ''    # your account no (E-mail or phone number)
    password   =  ''    # your account password
    douban_id  =  ''    # your id number
    app = DoubanRobot(account_id, password,douban_id)
    # app.login()
    # titile, content = app.get_joke()
    # print titile, content
    # if titile and content:
    #     print app.new_topic("cd", titile, content)
    app.talk_status('hahahah, just for a test')
    app.send_mail(159831817, 'Hallo, linsir.')
    app.sofa("CentOS")
    topics_list = app.get_my_topics()
    app.topics_up(topics_list)
