# -*- coding: utf-8 -*-

import requests


def login():
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Content-Length':'102',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host': 'www.guahao.com',
        'Pragma':'no-cache',
        'Referer': 'http://www.guahao.com/user/login?target=%2F',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
    }
    s = requests.session()
    s.get('http://www.guahao.com/user/login')
    captcha_content = s.get('http://www.guahao.com/validcode/genimage/1').content
    with open('dic.jpeg','wb',) as fp:
        fp.write(captcha_content)
    data = {
        'method': 'dologin',
        'target': '/',
        'loginid': '帐号',
        'password': 'md5加密后的密码',
        'vaildCode': raw_input()
    }
    r = s.post('http://www.guahao.com/user/login',data=data,headers=headers)
    print r.text



if __name__ == '__main__':
    login()
