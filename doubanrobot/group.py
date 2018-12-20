#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import random
import time
from utils import xpath_get, save_html, need_captcha, is_priavte_topic
from config import *
from logger import logger

class Group:
    def __init__(self, auth):
        self.auth = auth

    def get_joined_groups(self):
        url = DOUBAN_GROUP_LIST_JOINED_GROUPS.format(accout_id=self.auth.douban_id)
        r = self.auth.session.get(url, cookies=self.auth.session.cookies.get_dict())
        pattern = r'<a title=".+" href="' + DOUBAN_GROUP + r'(\w+)/'
        group_list = re.findall(pattern, r.text)
        return group_list


    def join_group(self, group_id, message="申请加入"):
        url = DOUBAN_GROUP_HOME.format(group_id=group_id)
        r = self.auth.session.get(url, cookies=self.auth.session.cookies.get_dict())
        xpath_exp = "//div[@class='group-misc']/a/@href"
        join_link = xpath_get(r.text, xpath_exp)
        if join_link:
            join_link = join_link[0]
            if join_link.startswith("javascript"):
                post_data = {
                    "ck": self.auth.ck,
                    "action": "request_join",
                    "message": message,
                    "send": "发送"
                }
                r = self.auth.session.post(url, data=post_data, cookies=self.auth.session.cookies.get_dict())
            else:
                r = self.auth.session.get(join_link, cookies=self.auth.session.cookies.get_dict())
        
        if r.status_code == 200:
            logger.info('Okay, join_group: "%s" successfully !' % group_id)
            return True

    def quit_group(self, group_id):
        url = DOUBAN_GROUP_QUIT_GROUP.format(group_id=group_id, ck=self.auth.ck)
        r = self.auth.session.get(url, cookies=self.auth.session.cookies.get_dict())
        if r.status_code == 200:
            logger.info('Okay, quit_group: "%s" successfully !' % group_id)
            return True

    def get_my_publish_topics(self, reply=False):
        homepage_url = DOUBAN_GROUP_MY_PUBLISH.format(accout_id=self.auth.douban_id)
        # self.auth.douban_id.join(['https://www.douban.com/group/people/', '/publish'])
        r = self.auth.session.get(homepage_url, cookies=self.auth.session.cookies.get_dict())
        if reply:
            pattern = r'<a href="' + DOUBAN_GROUP + r'topic/([0-9]+)/.*?<td nowrap="nowrap" class="td-reply">([0-9]+)'
        else:
            pattern = r'<a href="' + DOUBAN_GROUP + r'topic/([0-9]+)/'
        topics_list = re.findall(pattern, r.text, re.DOTALL)
        return topics_list

    def get_my_reply_topics(self, reply=False):
        
        homepage_url = DOUBAN_GROUP_MY_REPLY.format(accout_id=self.auth.douban_id)
        r = self.auth.session.get(homepage_url, cookies=self.auth.session.cookies.get_dict())

        if reply:
            pattern = r'<a href="' + DOUBAN_GROUP + r'topic/([0-9]+)/.*?<td nowrap="nowrap" class="td-reply">([0-9]+)'
        else:
            pattern = r'<a href="' + DOUBAN_GROUP + r'topic/([0-9]+)/'
        topics_list = re.findall(pattern, r.text, re.DOTALL)
        return topics_list

    def new_topic(self, group_id, title, content='Post by python'):
        '''
        use the ck pulish a new topic on the douban group.
        '''
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False
        group_url = DOUBAN_GROUP + group_id
        post_url = DOUBAN_NEW_TOPIC.format(group_id=group_id)
        post_data = {
            "ck": self.auth.ck,
            "rev_title": title,
            "rev_text": content,
            "rev_submit": '好了，发言',
        }
        r = self.auth.session.post(post_url, post_data, cookies=self.auth.session.cookies.get_dict())
        if r.url == group_url:
            logger.info('Okay, new_topic: "%s" post successfully !' % title)
            return True
        return False

    def topics_up(self, topics_list, content=['顶', '顶帖', '自己顶', 'waiting']):
        '''
        Randomly select a content and reply a topic.
        '''
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False

        # For example --> topics_list = ['22836371','98569169']
        for topics_id in topics_list:
            post_data = {
                "ck": self.auth.ck,
                "rv_comment": random.choice(content),
                "img": "(binary)",
                "start": "0",
                "submit_btn": "发送"
            }

            url = DOUBAN_ADD_COMMENT.format(topic_id=topics_id)
            print(need_captcha(self.auth, url+"/?start=0"))
            captcha_id, captcha_url = need_captcha(self.auth, url+"/?start=0")
            if captcha_id:
                logger.info("The captcha_image url address is %s" % captcha_url)
                vcode = raw_input('图片上的验证码是：')
                post_data["captcha-solution"] = vcode
                post_data["captcha-id"] = captcha_id

            print(post_data)
            r = self.auth.session.post(url, post_data, cookies=self.auth.session.cookies.get_dict())
            if DEBUG:
                save_html("topics_up.html", r.text)

            if r.status_code == 200:
                logger.info('Okay, already up ' + topics_id + ' topic')
            logger.info(r.status_code)
            logger.info(str(topics_list.index(topics_id) + 1).join(['Waiting for ', ' ...']))
            time.sleep(20)  # Wait a minute to up next topic, You can modify it to delay longer time
        return True

    def sofa(self, group_id, content=['沙发', '顶', '挽尊', ]):
        '''
        Randomly select a content and reply a topic.
        '''
        if not self.auth.ck:
            logger.error('ck is invalid!')
            return False

        group_url = DOUBAN_TOPICS.format(group_id=group_id)
        html = self.auth.session.get(group_url, cookies=self.auth.session.cookies.get_dict()).text
        # xpath_exp = "//tbody/tr[@class='title']/a/@href"
        topics = re.findall(r'topic/(\d+?)/.*?class="">.*?<td nowrap="nowrap" class="">(.*?)</td>', html, re.DOTALL)

        for item in topics:
            if item[1] == '':
                post_data = {
                    "ck": self.auth.ck,
                    "rv_comment": random.choice(content),
                    "img": "(binary)",
                    "start": "0",
                    "submit_btn": "发送"
                }
                url = DOUBAN_ADD_COMMENT.format(topic_id=item[0])
                r = self.auth.session.post(url, data=post_data, cookies=self.auth.session.cookies.get_dict())
                if r.status_code == 200:
                    logger.info('Okay, sofa: topic_id: %s successfully!' % (item[0]))

        return True

    def delete_other_comments(self, topic_id, comments_list):
        self.auth.session.headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.auth.session.headers["X-Requested-With"] = "XMLHttpRequest"
        # Leave last comment and delete all of the past comments
        for item in comments_list:
            payload = {
                "ck": self.auth.ck,
                "cid": item,
                "reason": "other_reason",
                "other": "",
                "submit": "确定"
            }
            remove_url = DOUBAN_ADMIN_REMOVE_COMMENT.format(topic_id=topic_id, cid=item)
            print(remove_url)
            self.auth.session.get(remove_url)
            self.auth.session.headers["Referer"] = remove_url
            r = self.auth.session.post(remove_url, data=payload, cookies=self.auth.session.cookies.get_dict())

            if r.status_code == 200:
                logger.info('Okay, already delete ' + topic_id + ' topic and cid: ' + item)
            logger.info(r.status_code)
            time.sleep(3)  # Wait ten seconds to delete next one
        return True

    def delete_reply_comments(self, topic_id, comments_list):
        for item in comments_list:
            post_data = {
                "ck": self.auth.ck,
                "cid": item
            }
            url = DOUBAN_REMOVE_COMMENT.format(topic_id=topic_id)
            r = self.auth.session.post(url, data=post_data, cookies=self.auth.session.cookies.get_dict())
            if r.status_code == 200:
                logger.info('Okay, already delete ' + topic_id + ' topic and reply cid: ' + item)
            logger.info(r.status_code)
            time.sleep(3)  # Wait ten seconds to delete next one

    def get_reply_comments_list(self, topic_id, reply_num=0):
        max_page = int(reply_num) / 100 +1
        # print(max_page)
        comments_list = []
        for page in range(max_page+1):
            # print(page)
            topic_url = DOUBAN_TOPIC.format(topic_id=topic_id) + "?start=" + str(page * 100)
            # print(topic_url)
            content = self.auth.session.get(topic_url).text
            if is_priavte_topic(content):
                break
            xpath_exp = "//li[@class='clearfix comment-item']/div/div[@id='{0}']/div[@class='operation-more']/a/@data-cid".format(self.auth.douban_id)
            comments = xpath_get(content, xpath_exp)
            if comments:
                comments_list = comments_list + comments
            time.sleep(1)

        # comments_list = re.findall(r'<li class="clearfix comment-item" id="[0-9]+" data-cid="([0-9]+)" >.+?<div class="operation_div" id="63666378">', content)
        logger.info("reply comments_list: " + str(comments_list))
        return comments_list

    def get_other_comments_list(self, topic_id, reply_num=0):
        max_page = int(reply_num) / 100 + 1
        # print(max_page)
        comments_list = []
        for page in range(max_page+1):
            topic_url = DOUBAN_TOPIC.format(topic_id=topic_id) + "?start=" + str(page * 100)
            content = self.auth.session.get(topic_url).text
            if is_priavte_topic(content):
                break
            xpath_exp = "//li[@class='clearfix comment-item']/div/div[@id!='{0}']/div[@class='operation-more']/a/@data-cid".format(self.auth.douban_id)
            # comments_list = re.findall(r'<li class="clearfix comment-item" id="[0-9]+" data-cid="([0-9]+)" >', content)
            comments = xpath_get(content, xpath_exp)
            if comments:
                comments_list = comments_list + comments
            time.sleep(1)

        logger.info("other comments_list: " + str(comments_list))
        return comments_list

    def delete_my_topic(self, topic_id, reply_num=0):
        # 先删除自己回复的评论
        comments_list = self.get_reply_comments_list(topic_id, reply_num)
        if comments_list:
            logger.info("Now, delete my reply comments of this topic. comments_list: " + str(comments_list))
            self.delete_reply_comments(topic_id, comments_list)

        # 删除其他回复的评论
        comments_list = self.get_other_comments_list(topic_id, reply_num)
        if comments_list:
            logger.info("Now, delete other comments of this topic. comments_list: " + str(comments_list))
            self.delete_other_comments(topic_id, comments_list)
        # 删除帖子
        remove_topic_url = DOUBAN_REMOVE_TOPIC.format(topic_id=topic_id)
        payload = {
            "ck": self.auth.ck
        }
        r = self.auth.session.post(remove_topic_url, data=payload, cookies=self.auth.session.cookies.get_dict())
        if r.status_code == 200:
            logger.info('Okay, already delete ' + topic_id + ' topic ')

        logger.info(r.status_code)

    def delete_reply_topic_comments(self):
        my_reply_topics = self.get_my_reply_topics(reply=True)

        for topic_id, reply_num in my_reply_topics:
            comments_list = self.get_reply_comments_list(topic_id, reply_num)
            self.delete_reply_comments(topic_id, comments_list)

    def delete_my_publish_topics(self):
        my_publish_topics = self.get_my_publish_topics(reply=True)

        for topic_id, reply_num in my_publish_topics:
            if not delete_my_topic(topic_id, reply_num):
                logger.error('Can not delete ' + topic_id + ' topic ')

