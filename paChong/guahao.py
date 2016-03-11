#https://gist.github.com/CraxGrix/5bb33e116934f1ebf259
#http://www.v2ex.com/t/257070#reply2
#这个软件的原理是先获得图片验证码，然后构造post包，需要人手工填上验证码
#http://www.zoulei.net/
# http://onlinemd5.com/
import requests 

def login(): 
    s = requests.session() #这个估计是为了获得验证码还有post
    s.get('http://www.guahao.com/user/login') #这样下面就会发送session
    captcha_content = s.get('http://www.guahao.com/validcode/genimage/1').content 
    with open('dic.jpeg', 'wb') as fp: 
        fp.write(captcha_content) 
    data = { 
    "method": "dologin", 
    "target": "/", 
    "loginId": "13136180314", 
    "password": "e10adc3949ba59abbe56e057f20f883e", #'md5加密后的密码', 123456 
    "validCode": input('CODE: ') 
    } 
    r = s.post('http://www.guahao.com/user/login', data=data, allow_redirects=False) 
    print(r.status_code) 


if __name__ == '__main__': 
    login()