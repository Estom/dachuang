# encoding=utf-8

##############数据表选择开始##############
# table_name = 'nwpu_news'
# table_name = 'shool_news'
table_name = 'wechat_article'
##############数据表选择结束#########

##############数据表参数配置################
if (table_name == 'wechat_article'):
    content_name = 'content_real'
    abstrack_name = 'abstract_auto'
else:
    content_name = 'content'
    abstrack_name = 'abstract'
###############数据表配置结束############################

import jieba
from networkx import from_scipy_sparse_matrix , pagerank
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def cut_sentence(sentence):
    """ 
    分句 
    :param sentence: 
    :return: 
    """
    if not isinstance(sentence, unicode):
        sentence = sentence.decode('utf-8')
    delimiters = frozenset(u'。！？')
    buf = []
    for ch in sentence:
        buf.append(ch)
        if delimiters.__contains__(ch):
            yield ''.join(buf)
            buf = []
    if buf:
        yield ''.join(buf)

def load_stopwords(path='stop_words.txt'):
    """ 
    加载停用词 
    :param path: 
    :return: 
    """
    with open(path) as f:
        stopwords = f.readlines()
    stopwrdlist = []
    for i in stopwords:
        i1 = i.decode('gbk')
        i1 = i1.strip("\r\n")
        stopwrdlist.append(i1)
    return frozenset(stopwrdlist)

def cut_words(sentence):
    """ 
    分词 
    :param sentence: 
    :return: 
    """
    stopwords = load_stopwords()
    return filter(lambda x: not stopwords.__contains__(x), jieba.cut(sentence))


def get_abstract(content, size=3):
    """ 
    利用textrank提取摘要 
    :param content: 
    :param size: 
    :return: 
    """
    docs = list(cut_sentence(content))
    tfidf_model = TfidfVectorizer(tokenizer=jieba.cut, stop_words=load_stopwords())
    tfidf_matrix = tfidf_model.fit_transform(docs)
    normalized_matrix = TfidfTransformer().fit_transform(tfidf_matrix)
    similarity = from_scipy_sparse_matrix(normalized_matrix * normalized_matrix.T)
    scores = pagerank(similarity)
    tops = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)
    size = min(size, len(docs))
    indices = map(lambda x: x[0], tops)[:size]
    return map(lambda idx: docs[idx], indices)

# 连接数据库
conn = MySQLdb.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'root',
    db = 'dcspider',
    charset = 'utf8'
)

cur = conn.cursor()
cur.execute("SET NAMES utf8")
aa = cur.execute("select id , %s from %s" % (content_name, table_name))

contentlist = cur.fetchmany(aa)
for ii in contentlist:
    s = ii[1]
    if len(s) < 2:
        continue
    s1 = get_abstract(s)
    sql = 'update %s set %s = "%s" where id = %d' % (table_name, abstrack_name, s1[0], ii[0])
    try:
        cur.execute(sql)
        conn.commit()
        print sql
    except:
        conn.rollback()

conn.close()

