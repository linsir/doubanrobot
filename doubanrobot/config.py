#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
COOKIES_FILE = 'logs/cookies.txt'
LOG_FILE = 'logs/doubanrobot.log'

# endpoints
# people
DOUBAN_HOME = "https://www.douban.com/"
DOUBAN_ACCOUNT_LOGIN = "https://www.douban.com/accounts/login"
DOUBAN_MY = "https://www.douban.com/people/{accout_id}/"
DOUBAN_EDIT_INTRO = "https://www.douban.com/j/people/{accout_id}/edit_intro"
DOUBAN_DOUMAIL = "https://www.douban.com/doumail/"
DOUBAN_DOUMAIL_WRITE = "https://www.douban.com/doumail/write"
DOUBAN_DOUMAIL_REPLY = "https://www.douban.com/j/doumail/send"
DOUBAN_DOUMAIL_CHAT = "https://www.douban.com/doumail/{receive_id}"
DOUBAN_CONTACTS_LIST = "https://www.douban.com/contacts/list"
DOUBAN_CONTACTS_RLIST = "https://www.douban.com/contacts/rlist"
DOUBAN_REMOVE_CONTACT = "https://www.douban.com/j/contact/removecontact"
DOUBAN_ADD_CONTACT = "https://www.douban.com/j/contact/addcontact"
DOUBAN_BLACKLIST = "https://www.douban.com/contacts/blacklist"
DOUBAN_ADD_BLACKLIST = "https://www.douban.com/j/contact/addtoblacklist"
DOUBAN_REMOVE_BLACKLIST = "https://www.douban.com/contacts/blacklist?remove={douban_id}&ck={ck}"

# group
DOUBAN_GROUP = "https://www.douban.com/group/"
DOUBAN_GROUP_HOME = "https://www.douban.com/group/{group_id}/"
DOUBAN_GROUP_LIST_JOINED_GROUPS = 'https://www.douban.com/group/people/{accout_id}/joins'
DOUBAN_GROUP_QUIT_GROUP = "https://www.douban.com/group/{group_id}/?action=quit&ck={ck}"
DOUBAN_GROUP_MY_PUBLISH = "https://www.douban.com/group/people/{accout_id}/publish"
DOUBAN_GROUP_MY_REPLY = "https://www.douban.com/group/people/{accout_id}/reply"
DOUBAN_TOPICS = "https://www.douban.com/group/{group_id}/"
DOUBAN_NEW_TOPIC = "https://www.douban.com/group/{group_id}/new_topic"
DOUBAN_TOPIC = "https://www.douban.com/group/topic/{topic_id}/"
DOUBAN_REMOVE_TOPIC = "https://www.douban.com/group/topic/{topic_id}/remove"
DOUBAN_ADD_COMMENT = "https://www.douban.com/group/topic/{topic_id}/add_comment"
DOUBAN_REMOVE_COMMENT = "https://www.douban.com/j/group/topic/{topic_id}/remove_comment"
DOUBAN_ADMIN_REMOVE_COMMENT = "https://www.douban.com/group/topic/{topic_id}/remove_comment/?cid={cid}"
DOUBAN_REACT = "https://m.douban.com/rexxar/api/v2/group/topic/"
DOUBAN_DOULIST = "https://www.douban.com/j/doulist/"

DEBUG = True

if __name__ == '__main__':
    MY = "https://www.douban.com/people/{accout_id}"
    print(MY.format(accout_id="6333"))
