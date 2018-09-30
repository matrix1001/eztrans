import requests
import json
import argparse
from lxml import html


GOOGLE_API="http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl={src}&tl={dst}&q={content}"
BINGS_API="http://api.microsofttranslator.com/v2/Http.svc/Translate?appId=AFC76A66CF4F434ED080D245C30CF1E71C22959C&from={src}&to={dst}&text={content}"
BAIDU_API="http://fanyi.baidu.com/transapi?from={src}&to={dst}&query={content}"
YOUDAO_API="http://fanyi.youdao.com/translate?&doctype=json&type={type}&i={content}"
YOUDAO_TYPE=['ZH_CN2EN',
             'ZH_CN2JA',
             'ZH_CN2KR',
             'ZH_CN2FR',
             'ZH_CN2RU',
             'ZH_CN2SP',
             'EN2ZH_CN',
             'JA2ZH_CN',
             'KR2ZH_CN',
             'FR2ZH_CN',
             'RU2ZH_CN',
             'SP2ZH_CN',]
TIMEOUT = 2
def html_get(url):
    return requests.get(url, timeout=TIMEOUT).text

def bings(content, src='auto', dst='zh'):
    try:
        url = BINGS_API.format(content=content, src=src, dst=dst)
        h = html.fromstring(html_get(url))
        result = h.text
        return result
    except:
        return None

def google(content, src='auto', dst='zh'):
    try:
        url = GOOGLE_API.format(content=content, src=src, dst=dst)
        decoder = json.JSONDecoder()
        result = decoder.decode(html_get(url))
        return result['sentences'][0]['trans']
    except:
        return None

def baidu(content, src='auto', dst='zh'):
    try:
        url = BAIDU_API.format(content=content, src=src, dst=dst)
        decoder = json.JSONDecoder()
        result = decoder.decode(html_get(url))
        return result['data'][0]['dst']
    except:
        return None
def youdao(content, src='auto', dst='zh'):
    try:
        if src=='auto':
            typ = 'AUTO'
        else:
            src = src.upper()
            dst = dst.upper()
            if src=='ZH': src='ZH_CN'
            if dst=='ZH': dst='ZH_CN'
            
            typ = '{src}2{dst}'.format(src=src,dst=dst)
            if typ not in YOUDAO_TYPE:
                return None
        url = YOUDAO_API.format(type=typ, content=content)
        decoder = json.JSONDecoder()
        result = decoder.decode(html_get(url))
        return result['translateResult'][0][0]['tgt']
    except:
        return None

def testall(content, src='auto', dst='zh'):
    print('------translating %s from %s to %s------' % (content, src, dst))
    print('bings:', bings(content, src, dst))
    print('google:', google(content, src, dst))
    print('baidu:', baidu(content, src, dst))
    print('youdao:', youdao(content, src, dst))

def test():
    testall('hola')
    testall('hola', src='es', dst='zh')
    testall('ハロー')
    testall('привет', dst='en')
    testall('Bonjour', dst='es')
    testall('良い')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple commandline translator by https://github.com/matrix1001.')
    parser.add_argument('-s', nargs='?', default='auto', help='language shortcut. like zh, en, ja......')
    parser.add_argument('-d', nargs='?', default='zh', help='language shortcut. like zh, en, ja......')
    parser.add_argument('content', type=str)
    args = parser.parse_args()
    print(google(args.content, args.s, args.d))