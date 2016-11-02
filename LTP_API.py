'''
pattern: ws(分词)，pos(词性标注)，ner(命名实体识别)，dp(依存句法分析)，sdp(语义依存分析)，srl(语义角色标注),all(全部任务)
fromat: xml(XML格式)，json(JSON格式)，conll(CONLL格式)，plain(简洁文本格式)
api_key : z8o079p31CVWTcjD2s2hBgjTxhWPOBzNcpYWMi2q
'''

import json
import collections
import requests
import sys
import os

file_path = 'testfile'
DIV = '--------------------------------------------------------------------------------'


class TextAnalysisByLTP:

    def __init__(self, path):
        self.__url_get_base = "http://api.ltp-cloud.com/analysis/?"
        self.__api_key = 'z8o079p31CVWTcjD2s2hBgjTxhWPOBzNcpYWMi2q'
        self.__format = 'json'
        self.__path = path
        self.__file = self.readfile()
        self.__output = 'output'
        self.__output_num = 1
        self.ner = []
        self.punctuation = ',.，。：、'

    def readfile(self):
        with open(self.__path, 'r', encoding='utf-8') as f:
            file = f.readlines()
        return file

    def get(self, text, pattern):
        url = "%sapi_key=%s&text=%s&format=%s&pattern=%s" % (self.__url_get_base, self.__api_key, text, self.__format, pattern)
        r = requests.get(url)
        return r.text, r.status_code

    @staticmethod
    def __del_semicolon(sentence):
        for i in ';；':
            sentence = sentence.replace(i, ' ')
        return sentence

    def __del_punc(self, sentence):
        for i in self.punctuation:
            sentence = sentence.replace(i, ' ')
        return sentence

    @staticmethod
    def __ws(line_json):
        sentence_token = []
        for word in line_json:
            ws_str = word['cont']
            sentence_token.append(ws_str)
        return sentence_token

    @staticmethod
    def __pos(line_json):
        sentence_token = []
        for word in line_json:
            cont = word['cont']
            pos = word['pos']
            pos_str = cont + '|' + pos
            sentence_token.append(pos_str)
        return sentence_token

    def __ner(self, line_json):
        name_entity = []
        sentence_token = []
        for word in line_json:
            cont = word['cont']
            pos = word['pos']
            ner = word['ne']
            ner_str = cont + '|' + pos + '|' + ner
            sentence_token.append(ner_str)
            if ner != 'O':
                name_entity.append(cont + '|' + ner)
        self.ner += name_entity
        return sentence_token

    # def __dp(self, line_json):
    #     sentence_token = []
    #     for word in line_json:
    #         cont = word['cont']
    #         sentence_token.append(cont)
    #     return sentence_token
    #
    # def __sdp(self, line_json):
    #     sentence_token = []
    #     for word in line_json:
    #         cont = word['cont']
    #         sentence_token.append(cont)
    #     return sentence_token
    #
    # def __srl(self, line_json):
    #     sentence_token = []
    #     for word in line_json:
    #         print(word)
    #         cont = word['cont']
    #         sentence_token.append(cont)
    #     return sentence_token

    def __writefile(self, processed_txt, file_name, pattern):
        output_file = ''
        for i in range(1, 10000):
            output_file = pattern + '_' + file_name + str(i) + '.txt'
            if output_file in os.listdir(os.getcwd()):
                continue
            else:
                break
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(processed_txt)

    def __count(self, count_list, pattern):
        if pattern == 'ner':
            count_list = self.ner
        word_freq = collections.Counter(count_list)
        count_seq = sorted(word_freq.items(), key=lambda d: d[1], reverse=True)
        self.__writefile(str(count_seq), 'count', pattern)
        return dict(word_freq.items())

    def process(self, pattern):
        try_count = 0
        process_count = 0
        fail_count = 0
        count_list = []
        processed_sent = []
        fail_list = []
        try:
            for line in self.__file:
                try_count += 1
                line = self.__del_semicolon(line)
                line = self.__del_punc(line)
                result, code = self.get(line, pattern)
                if code == 200:
                    process_count += 1
                    line_json = json.loads(result)[0][0]
                    if pattern == 'ws':
                        sentence_token = self.__ws(line_json)
                    elif pattern == 'pos':
                        sentence_token = self.__pos(line_json)
                    elif pattern == 'ner':
                        sentence_token = self.__ner(line_json)
                    elif pattern == 'dp':
                        pass
                        # sentence_token = self.__dp(line_json)
                    elif pattern == 'sdp':
                        pass
                        # sentence_token = self.__sdp(line_json)
                    elif pattern == 'srl':
                        pass
                        # sentence_token = self.__srl(line_json)
                    else:
                        return -1
                    str_token = ' '.join(sentence_token)
                    print('Success prcoessing', str(process_count), 'sentence.   ', 'Fail', str(fail_count), 'sentence')
                    count_list += sentence_token
                    processed_sent.append(str_token)
                else:
                    fail_count += 1
                    fail_list.append(try_count)
                    processed_sent.append('Processing failed')
                    continue
        except:
            print('final process:', str(process_count))
        self.__writefile('\n'.join(processed_sent), 'output', pattern)
        self.__count(count_list, pattern)



if __name__ == '__main__':
    a = TextAnalysisByLTP(sys.argv[1])
    a.process(sys.argv[2])

