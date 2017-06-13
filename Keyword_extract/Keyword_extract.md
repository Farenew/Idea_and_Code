
# 牛刀小试--用不同算法提取论文的关键字

----------

## 1.0 前言

上一次说到用Python配合jieba做文本分析，在最后我说要写一个用jieba里提供的关键词提取的方法来提取一下关键字。这两天写完论文了，看了一下这些算法。主要用到了两个算法，第一个是TF-IDF算法，另一个是TextRank算法，这里简单讲解一下，并以我的论文做个demo

## 2.0 算法

### TF-IDF思想

所谓TF-IDF，即term frequency-inverse document frequency，通过**词频**和**逆向文件频率**的一个算法，用来在文本中提取关键内容，计算某个字词对于一个文件或者语料库的重要程度。它的**大小与字词出现的次数成正比**，与**在语料库出现的频率成反比**。

TF-IDF由两部分组成，一部分是**TF**，一部分是**IDF**，两部分的实现，都可各自可以衍生出多种算法。

第一部分term frequency，**tf(t,d)**，表示t(text，词)在d(document，文件)中出现的频率，最简单的算法就是词频。即tf(t,d) = f(t,d)。
其它常用的计算方法：
![Markdown](http://i1.buimg.com/589212/0eeca1eb2f08500a.png)

第二部分inverse document frequency，**idf(t,D)**，表示t(词)在D(语料库)中出现的频率的逆序。基本的算法是：
![Markdown](http://i1.buimg.com/589212/af770f20d97ce2a4.png)
这里的N值是语料库总文件数量，分母是有t出现的文档的数量。但这里可能为0，也就是说一个词可能在给定的语料库中并不出现，所以一个常用的手段就是在分母加1。

TF-IDF就是把两部分相乘：
![Markdown](http://i1.buimg.com/589212/d43795e498552472.png)

TF-IDF的用法简单，速度也比较快，目前得到了广泛的应用。其实可以想到，根据语料库的差异，我们能很容易给出不同领域不同用法的关键字。并且在jieba里支持自定义的语料库。但注意TF-IDF仅仅是一个heuristic technique(启发法)，也就是说它并没得到科学的证明。


### TextRank

TextRank方法是类似于PageRank的，这里说一句，PageRank实在是一个太过于成功的做法，不仅在google身上取得了极大的成功，并且这将近20年的时间里，一直是很多设计者和开发者在使用的方法，即便现在，Google可能仍然在使用着基于PageRank的做法。这里假设对PageRank已经有所了解了，如果有疑问，在附录里给出简单的说明。

而TextRank则是类似PageRank的一种实现，PageRank是基于hyperlink做的有向无权图，而对于文本来说，它和hyperlink差别较大，如果界定词之间的联系，即如何建立起图，是一个需要思考的问题。在Rada Mihalcea和Paul Tarau的文章里，他们给出的是通过co-occurrence来界定词的联系。什么意思呢，举个例子，假设我有一个句子：

	东方的大梦没法子不醒了，炮声压下去马来与印度野林的虎啸，半醒的人们，揉着眼，祷告着祖先与神灵，不大会儿，失去了国土，自由和主权。

然后就把它拆分:
	
	东方的,大梦,没法子,不醒了,炮声,压下去,马来,与,印度,野林,的,虎啸，半醒的,人们，揉着眼，祷告着,祖先与神灵，不大会儿，失去了,国土，自由,和,主权。

这个拆分是我随便写的，然后如果两个词有联系，那么它们之间的距离应该在一个值N之间，这个值称为窗口值。比如说，我们假设窗口为5。那么如果一个词和另一个词距离有3个词，如东方和炮声，它们就是有联系的。

通过这个方法，就可以按照词建立起来一个图了，而重复的出现，则相当于给我们的边加权。所以这个方法的好处在于不需要外部的内容，完全靠文本本身的分析，但也同时继承了PageRank的缺点，甚至对一些缺点造成了放大，比如这种马尔科夫链的方式并不能完全说明词之间的联系。特别是中文，举个例子：

	我路过街边那家拉面店的橱窗的时候看到了你。

分词的结果可能就是：

	我,路过,街边,那家,拉面店,的,橱窗,的,时候,看到了,你。

而关键的联系**我**和**你**却因为距离太长而被忽略，这就是马尔科夫链的局限性，记得在吴军的<数学之美>里也说过这个问题。这个问题在自然语言处理中现在也有了一些新的处理手段了，限于篇幅，不展开了。

另外，需要注意，如果是句子的话用法稍微不同，对于句子的提取，则是基于句子之间的相似性，这个相似性可以有多种描述，原始文章中，对于相似性的描述是通过同类型的词出现的次数，也可以通过其他算法。这个相似性就相当于图中边的权重。

## 3.0 实现

其实jieba里面已经封装得非常好了，所以代码炒鸡简单~一看就懂：
```python
import jieba.analyse

# 从文件中读取内容到text中，生成一个字符串
fp = open('new.txt', 'r', encoding='utf-8')
text = ''
for sentence in fp.readlines():
    text += str(sentence.strip())
fp.close()
print('Reading is finished\n')

# 使用基于TF-IDT的算法进行关键字的提取
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
```

结果如下：

- 使用TF-IDT的关键词提取，结果如下：

```python
('活性剂', 0.29478338219295586)
('表面', 0.20239036650729286)
('除油', 0.1465449745693888)
('除油剂', 0.1390986461939572)
('FSO', 0.11971279612710635)
('复配', 0.11401528376553868)
('表面张力', 0.10509536672936809)
('100', 0.09494463141115331)
('浓度', 0.07614070498244475)
('配方', 0.05836943907961671)
('测试', 0.05799728374807666)
('溶液', 0.05748713968386741)
('油率', 0.051600343158235494)
('cm', 0.04953632943190607)
('测定', 0.04792416187904524)
('除油率', 0.04540830197924724)
('CMC', 0.04334428825291781)
('效果', 0.042304209625464426)
('离子型', 0.04169337814518301)
('性能', 0.040285387974540746)
```

- 使用TextRank的关键词提取，这里窗口大小为默认的5，结果如下：
```python
('活性剂', 0.29478338219295586)
('表面', 0.20239036650729286)
('除油', 0.1465449745693888)
('除油剂', 0.1390986461939572)
('FSO', 0.11971279612710635)
('复配', 0.11401528376553868)
('表面张力', 0.10509536672936809)
('100', 0.09494463141115331)
('浓度', 0.07614070498244475)
('配方', 0.05836943907961671)
('测试', 0.05799728374807666)
('溶液', 0.05748713968386741)
('油率', 0.051600343158235494)
('cm', 0.04953632943190607)
('测定', 0.04792416187904524)
('除油率', 0.04540830197924724)
('CMC', 0.04334428825291781)
('效果', 0.042304209625464426)
('离子型', 0.04169337814518301)
('性能', 0.040285387974540746)
```

- 使用TextRank的关键字提取，由于文章比较长，这里把窗口改变为100，结果如下：
```python
('活性剂', 0.29478338219295586)
('表面', 0.20239036650729286)
('除油', 0.1465449745693888)
('除油剂', 0.1390986461939572)
('FSO', 0.11971279612710635)
('复配', 0.11401528376553868)
('表面张力', 0.10509536672936809)
('100', 0.09494463141115331)
('浓度', 0.07614070498244475)
('配方', 0.05836943907961671)
('测试', 0.05799728374807666)
('溶液', 0.05748713968386741)
('油率', 0.051600343158235494)
('cm', 0.04953632943190607)
('测定', 0.04792416187904524)
('除油率', 0.04540830197924724)
('CMC', 0.04334428825291781)
('效果', 0.042304209625464426)
('离子型', 0.04169337814518301)
('性能', 0.040285387974540746)
```

## 4.0 讨论

这个关键词的提取结果和我的预料还是比较一致的，我估计也差不多是这个，一开始我就定的关键字是**表面活性剂**，**除油剂**，**复配**。但我希望的是能把表面活性剂放到一起，而不是把表面和活性剂分开，对于TF-IDF而言，需要修改语料库才能实现，我查了一下默认的语料库，发现内容确实太过于丰富，并不适合这种科学文章的使用。而对于TextRank，其实可以通过修改分词词库实现的，这个就不做了，各位有兴趣可以玩玩。

## 5.0 附录

PageRank
Page的思路是这样的：一个page对另一个page的hyperlink表示为对这个page的vote，而这个vote的权重，则由page本身的PageRank值表示。
也就是说，一个PR高的页面，引用了一个页面，那么被引用的页面的PR也会变高，而一个页面引用的页面越多，那么它对于引用页面的PR贡献就越小。

公式如下：
![Markdown](http://i1.buimg.com/589212/b5272f208d7ea9f0.png)

- 这里c指的是正交因子，用来把全式子正交化。Bu表示了引用了u的全部page，Nv表示v page的全部hyperlink之和。
因为把PageRank的和定义为为了全部网页的和，即有多少网页就存在多少的PageRank。

- 这里如果把A看成是对应网页的矩阵，那么如果存在u和v之间的链接，那么A就等于
![Markdown](http://i1.buimg.com/589212/6e18b7f3bf1e52a4.png)
否则就是0
把R看成是网页的向量，那么上式就是
![Markdown](http://i1.buimg.com/589212/39697bd7480bc2d3.png)
	
- 所以R就是A的特征向量，而c则是A的特征值。

举例来说，假如WikiPedia引用了我的页面，那么我的页面很可能就会出现在google搜索中，然而如果Wiki引用了500个页面，我的只是其中之一，那么可能我的页面就没那么靠前了。

## 6.0 引用

- 结巴的介绍
https://github.com/fxsjy/jieba

- Rada Mihalcea, Paul Tarau. TextRank算法
http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf

- TF-IDF介绍
https://en.wikipedia.org/wiki/Tf%E2%80%93idf

- PageRank算法，即佩里当年的论文（话说这个文章被引了一万多次。。。。就问你们怕不怕）
https://web.stanford.edu/class/cs54n/handouts/24-GooglePageRankAlgorithm.pdf