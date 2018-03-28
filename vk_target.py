# coding: utf-8
import json
import time
import logging
import requests as req


class Target:
    def __init__(self, p_cookie, l_cookie, ua, remixttpid=''):
        self.p_cookie = p_cookie
        self.l_cookie = l_cookie

        # region LOGIN
        s = req.Session()
        s.headers['user-agent'] = ua
        s.headers['content-type'] = 'application/x-www-form-urlencoded'
        s.headers['x-requested-with'] = 'XMLHttpRequest'
        s.cookies.set('h', '1', domain='.login.vk.com', path='/')
        s.cookies.set('p', p_cookie, domain='.login.vk.com', path='/')
        s.cookies.set('l', l_cookie, domain='.login.vk.com', path='/')
        r = s.post('https://login.vk.com/', 'role=al_frame')
        logging.debug('authorizing: %s' % r.url)
        if 'hash' in r.url:  # если 2fa включено
            if not remixttpid: raise Exception('No remixttpid')
            s.cookies.set('remixttpid', remixttpid, domain='.vk.com', path='/')
            r = s.post('https://login.vk.com/', 'role=al_frame')
            logging.debug('authorizing(2fa): %s' % r.url)

            if 'hash' in r.url:
                raise Exception('Login failed')
        r = s.get('https://vk.com/edit')
        assert 'login' not in r.url
        logging.debug('auth check: %s' % r.url)
        # endregion

        self.id = l_cookie
        self.s = s

    def get_hash(self, pid):
        photo_id = '%s_%s' % (self.id, pid)
        data = {
            'act': 'show',
            'photo': photo_id,
            'al': 1,
            'al_ad': 0,
            'list': 'album%s_0 / rev' % self.id,
            'module': 'profile'
        }
        logging.debug('get_hash data: %s' % data)
        r = self.s.post('https://vk.com/al_photos.php', data)
        logging.debug('get_hash post:\n\turl: %s\n\trequest headers: %s\n\trequest body: %s\n\tresponse headers: %s' %
                      (r.url, {k:v for k,v in r.request.headers.items() if k != 'Cookie'}, r.request.body, r.headers))
        j = get_json(r.text)
        hs = [x['pe_hash'] for x in j if x['id'] == photo_id][0]
        return hs

    def change_photo(self, path, pid):
        data = {'act': 'get_editor', 'al': 1,
                'photo_id': '%s_%s' % (self.id, pid),
                'hash': self.get_hash(pid)}
        res = self.s.post('https://vk.com/al_photos.php', data)
        j = get_json(res.text)
        url = j['upload']['url']

        photo = upload_photo(path, url)

        data = {
            'act': 'pe_save',
            'al': 1,
            '_query': photo,
            'hash': data['hash'],
            'photo': data['photo_id'],
            'texts': ''
        }
        res = self.s.post('https://vk.com/al_photos.php', data)
        if 'ошибка' in res.text.lower():
            print(res.text, photo, sep='\n\n', end='\n\n---\n\n')
            return res, photo


def get_json(response):
    try:
        return json.loads(response.split('<!json>')[1].split('<!>')[0])
    except IndexError:
        fname = '%s.dump' % int(time.time())
        with open(fname, 'wt') as f:
            f.write(response)
        raise Exception('Dump file: %s' % fname)


def upload_photo(path, server):
    if type(path) == str:
        with open(path, 'rb') as f:
            r = req.post(server, files={'file0': ('edited_NaN.jpg', f)}).text
    else:
        r = req.post(server, files={'file0': ('edited_NaN.jpg', path)}).text
    return r
