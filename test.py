import json
import collections

def abstract():
    sum_dict = {}
    with open(r'counter', encoding='utf-8') as f:
        for line in f.readlines()[:1]:
            print(line[8:-2])
            counter = json.loads(line[8:-2])
            for i in counter:
                if i not in sum_dict:
                    sum_dict[i] = counter[i]
                else:
                    sum_dict[i] += counter[i]
        sum_dict = sorted(sum_dict.items(), key=lambda d: d[1], reverse=True)
        #print(sum_dict)


def itcount():
    with open(r'C:\Users\51694\PycharmProjects\EventExtract\wanfangzhaiyao\dp_count_sum.txt', encoding='utf-8') as f:
        a = f.read()[5:]
        print((a))
        counter = json.loads(a)
        # print(counter)



if __name__ == '__main__':
    abstract()
    itcount()