# coding: utf-8
import logging
import os
import sys
import time
from random import shuffle

from vk_target import Target

source = 'photos'  # папка с фотками
logging.basicConfig(format='%(levelname)-8s [%(asctime)s]  %(message)s',
                    filemode='at',
                    filename='dp_log.log',
                    level=logging.INFO)

if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    raise Exception('No profile name')
    # profile = input('Profile name: ')

if not profile or profile not in os.listdir('profiles'):
    raise Exception('No such profile')

with open(os.path.join('profiles', profile)) as f:
    photo_id, p_cookie, l_cookie, user_agent, *remixttpid = f.read().splitlines()
remixttpid = '' if not remixttpid else remixttpid[0]
target = Target(p_cookie, l_cookie, user_agent, remixttpid)

logging.log(logging.INFO, 'Profile loaded')


def iter_photos(src):
    photos = [os.path.join(src, x) for x in os.listdir(source)]

    while True:
        shuffle(photos)
        for photo in photos:
            yield photo


for photo in iter_photos(source):
    try:
        res = target.change_photo(photo, photo_id)
        logging.log(logging.INFO, os.path.split(photo)[-1])
        if res:
            logging.error(res[0].text.strip()[:200])
    except:
        logging.exception(photo)
    time.sleep(4350)  # не чаще 20 раз в день
