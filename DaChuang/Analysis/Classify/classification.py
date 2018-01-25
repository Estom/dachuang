#coding=utf-8

"""
脚本名称 : classification.py
脚本作用 : 文本分类
备   注 ： 使用前先配置以下信息
        最后分类标签放在了表格中“class”字段下
"""

#####################数据表选择#################################
# table_name =  'nwpu_news'
# table_name =  'shool_news'
table_name =  'wechat_article'
#####################################################################

#######################数据库配置############################
# 使用不同的表格需要配置一下信息
# table_name : 表格名称
# title_index : 文章标题索引（从0开始）
# contents_index ： 内容索引
# label_index : 标签索引


if (table_name == 'nwpu_news'):
    title_index = 0
    contents_index = 4
    label_index = 7
elif (table_name == 'shool_news'):
        title_index = 2
        contents_index = 4
        label_index = 6
elif (table_name == 'wechat_article'):
    title_index = 0
    contents_index = 5
    label_index = 8

import sys
import MySQLdb
import FormatData
import cPickle as pickle
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB  # 导入多项式贝叶斯算法

# ###################基础常量###################################
catelist = ['学科竞赛' , '科研信息' , '行政信息' , '招生信息' , '招聘就业' , '校园活动' , '文学艺术'];
wordbag_path = "./train_word_bag_my/train_set_my.dat"
stopword_path = "./train_word_bag_my/hlt_stop_words.txt"
classification_path = "./train_word_bag_my/classification_NB.dat"
###############################################################

conn = MySQLdb.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'ykl123',
    db = 'dcdata',
    charset = "utf8",
)
cur = conn.cursor()
cur.execute("SET NAMES utf8")

sql = 'select * from %s' % (table_name)

str1 = cur.execute(sql)

# 数据库里全部词条
info = cur.fetchmany(str1)

TestData = list(info)

# 开始分词
for ii in TestData:
    ii1 = list(ii)
    if (ii1[contents_index] == unicode('')):
        ii1[contents_index] = FormatData.TextCut(ii1[title_index]);
    else:
        ii1[contents_index] = FormatData.TextCut(ii1[contents_index]);
# 分词结束

# 建立Bounch数据
bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
bunch.target_name.extend(catelist)
for ii in TestData:
    bunch.label.append(ii[label_index])
    bunch.filenames.append(ii[title_index])
    bunch.contents.append(ii[contents_index])

'''''
with open(wordbag_path, "wb") as file_obj:
    pickle.dump(bunch, file_obj)
# 建立Bounch数据结束
'''

# 建立词向量空间
stpwrdlst = FormatData._readfile(stopword_path).splitlines()  # 读取停用词
# bunch = FormatData._writebunchobj(wordbag_path)

train_bunch = FormatData._readbunchobj(wordbag_path)

# 构建tf-idf词向量空间对象
test_tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                   vocabulary = {})

test_tfidfspace.vocabulary = train_bunch.vocabulary
# 构建使用TfidfVectorizer初始化向量空间模型
# 这里面有TF-IDF权重矩阵还有我们要的词向量空间坐标轴信息vocabulary_
test_vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5 ,
                                  vocabulary = train_bunch.vocabulary)
''''' 
关于参数，你只需要了解这么几个就可以了： 
stop_words: 
传入停用词，以后我们获得vocabulary_的时候，就会根据文本信息去掉停用词得到 
vocabulary: 
之前说过，不再解释。 
sublinear_tf: 
计算tf值采用亚线性策略。比如，我们以前算tf是词频，现在用1+log(tf)来充当词频。 
smooth_idf: 
计算idf的时候log(分子/分母)分母有可能是0，smooth_idf会采用log(分子/(1+分母))的方式解决。默认已经开启，无需关心。 
norm: 
归一化，我们计算TF-IDF的时候，是用TF*IDF，TF可以是归一化的，也可以是没有归一化的，一般都是采用归一化的方法，默认开启. 
max_df: 
有些词，他们的文档频率太高了（一个词如果每篇文档都出现，那还有必要用它来区分文本类别吗？当然不用了呀），所以，我们可以 
设定一个阈值，比如float类型0.5（取值范围[0.0,1.0]）,表示这个词如果在整个数据集中超过50%的文本都出现了，那么我们也把它列 
为临时停用词。当然你也可以设定为int型，例如max_df=10,表示这个词如果在整个数据集中超过10的文本都出现了，那么我们也把它列 
为临时停用词。 
min_df: 
与max_df相反，虽然文档频率越低，似乎越能区分文本，可是如果太低，例如10000篇文本中只有1篇文本出现过这个词，仅仅因为这1篇 
文本，就增加了词向量空间的维度，太不划算。 
当然，max_df和min_df在给定vocabulary参数时，就失效了。 
'''

# 此时tdm里面存储的就是if-idf权值矩阵
test_tfidfspace.tdm = test_vectorizer.fit_transform(bunch.contents)

# 导入分类器
clf = MultinomialNB(alpha=0.001).fit(train_bunch.tdm, train_bunch.label)

predicted = clf.predict(test_tfidfspace.tdm)

for file_name, expct_cate in zip(test_tfidfspace.filenames, predicted):
    # print file_name , " -->预测类别:" , expct_cate
    con = 'update %s set class = "%s" where title = "%s"' % (table_name , expct_cate , file_name)
    try:
        cur.execute(con)
        conn.commit()
    except:
        conn.rollback()

cur.close()
conn.commit()
conn.close()

