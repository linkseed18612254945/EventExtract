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


DIV = '--------------------------------------------------------------------------------'


class TextAnalysisByLTP:

    def __init__(self, path, dir_path_flag=0):
        self.dir_flag = dir_path_flag
        self.__url_get_base = "http://api.ltp-cloud.com/analysis/?"
        self.__api_key = 'z8o079p31CVWTcjD2s2hBgjTxhWPOBzNcpYWMi2q'
        self.__format = 'json'
        self.__path = path
        self.__output = 'output'
        self.__output_num = 1
        self.ner = []
        self.punctuation = ',.，。：、'
        self.hed = []
        self.result_path = os.getcwd() + '\\' + 'LTP_result'
        self.filename = ''
        self.process_count = 0
        self.fail_count = 0


    @staticmethod
    def readfile(path):
        with open(path, 'r', encoding='utf-8') as f:
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
    def stopword(sentence):
        with open('stopword', encoding='utf-8') as f:
            stopword = f.readlines()
        for word in sentence:
            if word in stopword:
                sentence.pop(word)

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

    def __writefile(self, processed_txt, pattern, count_flag=False):
        if count_flag:
            output_file = self.result_path + '\\' + pattern + '_' + 'count' + '_' + self.filename + '.txt'
        else:
            output_file = self.result_path + '\\' + pattern + '_' + self.filename + '.txt'
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(processed_txt)

    def __count(self, count_list, pattern):
        if pattern == 'ner':
            count_list = self.ner
        if pattern == 'dp':
            count_list = self.hed
            self.filename = 'sum'
        word_freq = collections.Counter(count_list)
        count_seq = sorted(word_freq.items(), key=lambda d: d[1], reverse=True)
        self.__writefile(str(count_seq), pattern, count_flag=True)
        return dict(word_freq.items())

    def process(self, pattern, output_count=1):
        count_list = []
        dir_name = 'LTP_result'
        for i in range(1, 100):
            if dir_name in os.listdir(os.getcwd()):
                self.result_path = self.result_path + '(' + str(i) + ')'
                dir_name = dir_name + '(' + str(i) + ')'
                continue
            else:
                os.makedirs(self.result_path)
                break
        if self.dir_flag:
            file_names = os.listdir(self.__path)
            file_count = 0
            for file_name in file_names:
                file_count += 1
                self.filename = file_name
                path = self.__path + '\\' + file_name
                file = self.readfile(path)
                processed_sent, count_list = self.__ltpget(file, pattern)
                self.__writefile('\n'.join(processed_sent), pattern)
                if output_count:
                    self.__count(count_list, pattern)
                print('Complete ' + str(file_count) + ' files.')
                print('The failed line: ', self.fail_list)
        else:
            file = self.readfile(self.__path)
            processed_sent, count_list = self.__ltpget(file, pattern)
            self.__writefile('\n'.join(processed_sent), pattern)
            if output_count:
                self.__count(count_list, pattern)
            print('The failed line: ', self.fail_list)
        return count_list

    def __ltpget(self, file, pattern):
        try_count = 0
        count_list = []
        processed_sent = []
        self.fail_list = []
        try:
            for line in file:
                if line == '\n':
                    processed_sent.append('\n')
                    continue
                try_count += 1
                line = self.__del_semicolon(line)
                line = self.__del_punc(line)
                result, code = self.get(line, pattern)
                if code == 200:
                    self.process_count += 1
                    line_json = json.loads(result)[0][0]
                    if pattern == 'ws':
                        sentence_token = self.__ws(line_json)
                    elif pattern == 'pos':
                        sentence_token = self.__pos(line_json)
                    elif pattern == 'ner':
                        sentence_token = self.__ner(line_json)
                    else:
                        return -1
                    str_token = ' '.join(sentence_token)
                    print('Success prcoessing', str(self.process_count), 'sentence.   ', 'Fail', str(self.fail_count), 'sentence')
                    count_list += sentence_token
                    processed_sent.append(str_token)
                else:
                    self.fail_count += 1
                    self.fail_list.append(try_count)
                    processed_sent.append('Processing failed')
                    continue
        except:
            print('final process:', str(self.process_count))
        return processed_sent, count_list

if __name__ == '__main__':
    f_count = 1
    f_dir = 0
    f_n = sys.argv[1]
    f_ad = sys.argv[2]
    if len(sys.argv) > 3:
        for i in sys.argv[3:]:
            if i[:-2] == 'dir':
                f_dir = int(i[-1])
                continue
            if i[:-2] == 'count':
                f_count = int(i[-1])
    a = TextAnalysisByLTP(f_n, f_dir)
    a.process(f_ad, f_count)
