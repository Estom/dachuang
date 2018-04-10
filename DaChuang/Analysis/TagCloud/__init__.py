dict_hot_word = {}  # 所有的关键词列表
hotwordlist = []  # 关键词列表
i = 0
while True:
    info = Analysis.SQLconfig.sql1.select('dcweb_tag', ['name', 'number'], None, 1, i)
    if len(info) == 0:
        break
    dict_hot_word.update({info[0]: info[1]})
    hotwordlist.append(info[0])
    i += 1
    print "读取第%d条数据" % i

# 读取停用词表
stpwrdlst = []
with open('stop_words.txt', 'rb') as f:
    text = f.readlines()
for ii in text:
    ii1 = ii.decode('utf8')
    ii1 = ii1.strip("\r\n")
    stpwrdlst.append(ii1)
# 读停用词表结束

'''用新文章更新热词词典，并记录新文章的热词'''
dict = {}  # 中间变量
dict_1 = []  # 中间变量
# 文章Tfidf化
vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.2)
tfidf = vectorizer.fit_transform(Data_content)
word = vectorizer.get_feature_names()
weight = tfidf.toarray()
for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
    dict.clear()
    dict_1 = []
    for j in range(len(word)):
        if weight[i][j] > 0.1:  # 如果一个词的Tfidf值大于0.1才进入统计列表
            dict.update({word[j]: weight[i][j]})
    dict_1 = sorted(dict.iteritems(), key=lambda asd: asd[1], reverse=True)
    dict.clear()
    for ii in dict_1:
        if len(dict) < 5:
            dict.update({ii[0]: ii[1]})
            if dict_hot_word.has_key(ii[0]):
                dict_hot_word.update({ii[0]: 1000 * ii[1] + dict_hot_word.get(ii[0])})
            else:
                dict_hot_word.update({ii[0]: 1000 * ii[1]})
    Analysis.SQLconfig.sql1.update('dcweb_article', {'tag_mark': Data_ID[i][1] % 2 ** 2 + 2 ** 1},
                                  'id = %d' % Data_ID[i][0])
    print "%d:id=%d更新状态变量为%d" % (index - 1000 + i, Data_ID[i][0], Data_ID[i][1] % 2 ** 2 + 2 ** 1)
'''以上程序已经实现了热词的更新和当前数据表中文章关键字的提取'''

# #######################热词存回数据库###############################
i = 0
dict_hot_word_list = sorted(dict_hot_word.iteritems(), key=lambda asd: asd[1], reverse=True)
for ii in dict_hot_word_list:
    i += 1
    print "第%d条 : %s : %d\n" % (i, ii[0], ii[1])
    if ii[0] in hotwordlist:  # 如果这条热词已经在数据库了就更新这个热词的权值
        dic = {'number': ii[1]}
        Analysis.SQLconfig.sql1.update('dcweb_tag', dic, 'name="%s"' % ii[0])
    else:
        dic = {'name': ii[0], 'number': ii[1]}
        Analysis.SQLconfig.sql1.add('dcweb_tag', dic)
# #######################热词存回数据库结束##################################