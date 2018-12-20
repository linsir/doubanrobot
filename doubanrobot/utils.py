#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from lxml import etree
from logger import logger


def save_html(name, data):
    filename = "logs/" + name 
    with open(filename, 'w') as f:
        f.write(data)

def xpath_get(content, xpath_exp):
    try:
        html = etree.HTML(content)
        value = html.xpath(xpath_exp)
        if len(value):
            return value
        else:
            logger.warning("xpath_get: [" + xpath_exp + "] no result: ")
            return ""
    except Exception as e:
        logger.error("xpath_get(): " + str(e.message))

def need_captcha(auth, url):
    r = auth.session.get(url, cookies=auth.session.cookies.get_dict())
    html = r.text
    xpath_exp = "//img[@id='captcha_image']/@src"
    imgurl = xpath_get(html, xpath_exp)
    if imgurl:
        logger.info("The captcha_image url address is %s" % imgurl[0])
        xpath_exp = "//input[@name='captcha-id']/@value"
        captcha_id = xpath_get(html, xpath_exp)
        if captcha_id:
            return captcha_id[0], imgurl[0]
        
    else:
        return False, False

def is_priavte_topic(html):
    xpath_exp = "//img[@style='float:left;']/@src"
    imgurl = xpath_get(html, xpath_exp)
    if imgurl:
        logger.warning("The topic can not read")
        return True
    else:
        return False
