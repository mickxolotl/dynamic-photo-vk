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

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s [%(asctime)s]  %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    raise Exception('No profile name')
    # profile = input('Profile name: ')

if not profile or profile not in os.listdir('profiles'):
    raise Exception('No such profile')

with open(os.path.join('profiles', profile)) as f:
    text = f.read()
    if text.startswith('\ufeff'):
        text = text[1:]
    photo_id, p_cookie, l_cookie, user_agent, *remixttpid = text.splitlines()
remixttpid = '' if not remixttpid else remixttpid[0]
photo_id = photo_id if '_' not in photo_id else photo_id.split('_')[-1]

target = Target(p_cookie, l_cookie, user_agent, remixttpid)

logging.log(logging.INFO, 'Profile loaded')

if profile in os.listdir(source) and os.path.isdir(os.path.join(source, profile)):
    source = os.path.join(source, profile)
logging.info('Looking for photos in %s' % source)


def iter_photos(src):
    photos = [os.path.join(src, x) for x in os.listdir(src)
              if x != '.gitkeep' and not os.path.isdir(os.path.join(src, x))]
    if not photos:
        logging.error('No photos in %s' % src)
        sys.exit(1)

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
    except KeyboardInterrupt:
        logging.info('Exit')
        sys.exit(0)
    except Exception:
        logging.exception(photo)
    try:
        time.sleep(4350)  # не чаще 20 раз в день
    except KeyboardInterrupt:
        logging.info('Exit')
        sys.exit(0)
