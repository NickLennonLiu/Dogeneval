files = [
    'baidu_stopwords.txt',
    'cn_stopwords.txt',
    'hit_stopwords.txt',
    'scu_stopwords.txt',
]

stopwords = set()

for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
    print(file, len(lines))
    for line in lines:
        stopwords.add(line.strip())

print('Total stopwords:', len(stopwords))
with open('all_stopwords.txt', 'w') as f:
    for word in stopwords:
        f.write(word + '\n')