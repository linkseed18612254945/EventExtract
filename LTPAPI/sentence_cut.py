import sys


def cut_sent(words):
    start = 0
    i = 0
    sents = []
    punt_list = '，,.。！？'
    for word in words:
        if word in punt_list:
            sents.append(words[start:i+1])
            start = i + 1
            i += 1
        else:
            i += 1
    if start < len(words):
        sents.append(words[start:])
    return sents


if __name__ == '__main__':
    file_path = sys.argv[1]
    res_path = 'sentence_cut.txt'
    with open(file_path, encoding='utf-8') as f:
        sents = f.readlines()
    with open(res_path, 'a', encoding='utf-8') as f:
        for sent in sents:
            for i in cut_sent(sent):
                f.write(i[:-1]+'\n')

