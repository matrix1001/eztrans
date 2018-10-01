import json, requests
import ctypes

from msgserver.msgserver import MsgServer

def translator(content, src='auto', dst='zh', **kwargs):
    GOOGLE_API="http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl={src}&tl={dst}&q={content}"
    try:    
        url = GOOGLE_API.format(content=content, src=src, dst=dst)
        decoder = json.JSONDecoder()
        html = requests.get(url, timeout=3).text
        result_dict = decoder.decode(html)
        trans = result_dict['sentences'][0]['trans']
        user = ctypes.CDLL('user32.dll')
        title = 'translator: %s' % result_dict['src']
        msg =  '%s -> %s' % (content, trans)
        user.MessageBoxW(None, msg, title, 0)
        return trans
    except Exception as e:
        print(e, str(e))
        return None

if __name__ == '__main__':
    address = ('localhost', 8088)
    server = MsgServer(address)
    server.commands['translator'] = {
        'func':translator,
        'required':{
            'content':str, 
                },
        'optional':{
            'src':str, 
            'dst':str,
            'encoding':str,
                },
        'description':'my translator',
    }
    server.start()
    input()
    server.stop()