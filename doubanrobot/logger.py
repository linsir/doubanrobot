#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from config import LOG_FILE, DEBUG


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-3s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename=LOG_FILE,
                    filemode='a')

console = logging.StreamHandler()
if DEBUG:
    console.setLevel(logging.INFO)
else:
    console.setLevel(logging.ERROR)
    
formatter = logging.Formatter('%(asctime)s %(levelname)-s %(message)s', datefmt='%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)


