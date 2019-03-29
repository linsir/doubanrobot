#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import *
from utils import xpath_get
from logger import logger
import json
import re

class People:
    def __init__(self, auth):
        self.auth = auth
    def get_contacts_list(self):
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False
        self.auth.session.headers["Referer"] = DOUBAN_HOME
        r = self.auth.session.get(DOUBAN_CONTACTS_LIST, cookies=self.auth.session.cookies.get_dict())
        xpath_exp = "//ul[@class='user-list']/li/@id"
        users = xpath_get(r.text, xpath_exp)
        contacts_list = []
        for user in users:
            if user.startswith("u"):
               contacts_list.append(user[1:])

        return contacts_list

    def edit_intro(self, content='Hello. I just edited my douban intro.'):
        '''
        edit your bio (aka intro)
        '''
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False

        post_data = {
            "ck": self.auth.ck,
            "intro": content,
        }

        self.auth.session.headers["Referer"] = DOUBAN_EDIT_INTRO
        r = self.auth.session.post(DOUBAN_EDIT_INTRO, data=post_data, cookies=self.auth.session.cookies.get_dict())
        if r.status_code == 200:
            logger.info('Okay, edited your intro successfully !')
            return True
        
    def get_contacts_rlist(self):
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False
        self.auth.session.headers["Referer"] = DOUBAN_HOME
        r = self.auth.session.get(DOUBAN_CONTACTS_RLIST, cookies=self.auth.session.cookies.get_dict())
        xpath_exp = "//ul[@class='user-list']/li/@id"
        users = xpath_get(r.text, xpath_exp)
        contacts_list = []
        for user in users:
            if user.startswith("u"):
               contacts_list.append(user[1:])

        return contacts_list

    def remove_contact(self, douban_id):
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False
        post_data = {
            "ck": self.auth.ck,
            "people": douban_id,
        }

        self.auth.session.headers["Referer"] = DOUBAN_CONTACTS_LIST
        r = self.auth.session.post(DOUBAN_REMOVE_CONTACT, data=post_data, cookies=self.auth.session.cookies.get_dict())
        data = json.loads(r.text)
        if data['result']:
            logger.info('Okay, remove_contact: "%s" successfully !' % douban_id)
            return True

    def add_contact(self, douban_id):
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False
        post_data = {
            "ck": self.auth.ck,
            "from": "rlist",
            "people": douban_id,
        }

        self.auth.session.headers["Referer"] = DOUBAN_CONTACTS_RLIST
        r = self.auth.session.post(DOUBAN_ADD_CONTACT, data=post_data, cookies=self.auth.session.cookies.get_dict())
        print(r.text)
        data = json.loads(r.text)
        if data['result'] == False:
            logger.info('add_contact: the people "%s" invalid !' % douban_id)
            return False
        else:
            logger.info('Okay, add_contact: "%s" successfully !' % douban_id)
            return True

    def get_blacklist(self):
        self.auth.session.headers["Referer"] = DOUBAN_HOME
        r = self.auth.session.get(DOUBAN_BLACKLIST, cookies=self.auth.session.cookies.get_dict())
        xpath_exp = "//dl[@class='obu']/dt/a/@href"
        urls = xpath_get(r.text, xpath_exp)
        pattern = r"https://www.douban.com/people/(\w+)/"
        blacklist = []
        for url in urls:
            id = re.findall(pattern, url)
            if id:
               blacklist.append(id[0])
        return blacklist

    def add_to_blacklist(self, douban_id):
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False
        post_data = {
            "ck": self.auth.ck,
            "people": douban_id,
        }

        self.auth.session.headers["Referer"] = DOUBAN_CONTACTS_LIST
        r = self.auth.session.post(DOUBAN_ADD_BLACKLIST, data=post_data, cookies=self.auth.session.cookies.get_dict())
        data = json.loads(r.text)
        if data['result']:
            logger.info('Okay, add_to_blacklist: "%s" successfully !' % douban_id)
            return True

    def remove_from_blacklist(self, douban_id):
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False
        url = DOUBAN_REMOVE_BLACKLIST.format(douban_id=douban_id, ck=self.auth.ck)
        self.auth.session.headers["Referer"] = DOUBAN_BLACKLIST
        r = self.auth.session.get(url, cookies=self.auth.session.cookies.get_dict())
        if r.status_code == 200:
            logger.info('Okay, add_to_blacklist: "%s" successfully !' % douban_id)
            return True
            

    def talk_status(self, content='Hello. this message from https://github.com/linsir/doubanrobot'):
        '''
        talk a status.
        '''
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False

        post_data = {
            "ck": self.auth.ck,
            "comment": content,
        }

        self.auth.session.headers["Referer"] = DOUBAN_HOME
        r = self.auth.session.post(DOUBAN_HOME, data=post_data, cookies=self.auth.session.cookies.get_dict())
        # print(r.text)
        if r.status_code == 200:
            logger.info('Okay, talk_status: "%s" post successfully !' % content)
            return True
        
        
    def send_image(self, image, content='Hello. this message from https://github.com/linsir/doubanrobot'):
        '''
        post your status with an image.
        '''
        if not self.auth.ck:
            logging.error('ck is invalid!')
            return False
        
        upload_data = {"ck": self.auth.ck}
        files = {"image":open(image, "rb")}
        self.auth.session.headers["Referer"] = DOUBAN_UPLOAD_IMAGE
        upload = self.session.post(DOUBAN_UPLOAD_IMAGE, cookies=self.session.cookies.get_dict(), data=upload_data, files=files).json()

        post_data = {
            "ck": self.auth.ck,
            "comment": content,
            "uploaded": upload["url"],
        }
        
        self.auth.session.headers["Referer"] = DOUBAN_HOME
        r = self.session.post(DOUBAN_HOME, data=post_data, cookies=self.session.cookies.get_dict())
        if r.status_code == 200:
            logging.info('Okay, send_image: "%s" post successfully !' % content)
            return True
        
        
    def send_doumail(self, id, content='Linsir, this doumail from https://github.com/linsir/doubanrobot'):
        '''
        send a doumail to other.
        '''
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False

        post_data = {
            "ck": self.auth.ck,
            "m_text": content,
            "to": id,
            "m_submit": "好了，寄出去",
        }
        self.auth.session.headers["Referer"] = DOUBAN_DOUMAIL_WRITE
        r = self.auth.session.post(DOUBAN_DOUMAIL_WRITE, data=post_data, cookies=self.auth.session.cookies.get_dict())
        if r.status_code == 200:
            logger.info('Okay, send_mail: To %s doumail "%s" successfully !' % (id, content))
            return True

    def reply_doumail(self, receive_id, content='Linsir, this doumail from https://github.com/linsir/doubanrobot'):
        '''
        send a doumail to other.
        the problem here is that the receive_id must be a number, not the custom url name.
        '''
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False

        post_data = {
            "ck": self.auth.ck,
            "m_text": content,
            "to": receive_id,
        }
        self.auth.session.headers["Referer"] = DOUBAN_DOUMAIL_CHAT.format(receive_id=receive_id)
        r = self.auth.session.post(DOUBAN_DOUMAIL_REPLY, post_data, cookies=self.auth.session.cookies.get_dict())
        if r.status_code == 200:
            logger.info('Okay, reply_doumail: To %s doumail "%s" successfully !' % (id, content))
            return True
