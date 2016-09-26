'''
pattern: ws(分词)，pos(词性标注)，ner(命名实体识别)，dp(依存句法分析)，sdp(语义依存分析)，srl(语义角色标注),all(全部任务)
fromat: xml(XML格式)，json(JSON格式)，conll(CONLL格式)，plain(简洁文本格式)
'''
import requests


class LTP:
    def __init__(self):
        self.url_get_base = "http://api.ltp-cloud.com/analysis/?"
        self.api_key = 'd8a0h8h0hWjctLeUkTgyDGexbMSd2ODUTN1OfuMX'
        self.format = 'json'

    def get(self, text, pattern):
        url = "%sapi_key=%s&text=%s&format=%s&pattern=%s" % (self.url_get_base, self.api_key, text, self.format, pattern)
        r = requests.get(url)
        print(r.status_code)
        return r.text


if __name__ == '__main__':
    file_path = 'C:/Users/51694/Desktop/学习/语料/Abstract-1.txt'
    with open(file_path, encoding='utf-8') as f:
        for text in f.readlines()[:50]:
            pattern = 'sdp'
            L = LTP()
            print(L.get(text, pattern))

