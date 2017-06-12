import jieba.analyse

# 从文件中读取内容到text中，生成一个字符串
fp = open('new.txt', 'r', encoding='utf-8')
text = ''
for sentence in fp.readlines():
    text += str(sentence.strip())
fp.close()
print('Reading is finished\n')

# 使用基于TF-IDF的算法进行关键字的提取
tags = jieba.analyse.extract_tags(text, withWeight=True)
for i in tags:
    print(i)

# 使用基于TextRank的算法进行的关键字提取
tags_TR = jieba.analyse.textrank(text, withWeight=True)
for i in tags:
    print(i)

# 使用基于TextRank的算法进行的关键字提取，这里把窗口改成了100
newclass = jieba.analyse.TextRank()
newclass.span = 100
newclass.textrank(text, withWeight=True)
for i in tags:
    print(i)