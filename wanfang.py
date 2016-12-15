import os


data_path = r'C:\Users\51694\PycharmProjects\EventExtract\wanfangzhaiyao\data.txt'
num_docs = 10

start_line = 0
end_line = 0
ab_doc = []

with open(data_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()[:]
for i in range(len(lines)):
    if lines[i] == '\n':
        end_line = i
        ab_doc.append(lines[start_line:end_line])
        start_line = end_line + 1
for doc in ab_doc[:num_docs]:
    print('-----------------------------')
    for sent in doc:
        print(sent)