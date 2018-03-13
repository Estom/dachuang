#!/user/bin/python
# coding:utf-8
__author__ = 'yan.shi'
import nltk
import numpy
import jieba
import codecs

# 文本摘要方法有很多，主要分为抽取式和生成式，应用比较多的是抽取式，也比较简单，就是从文本中抽取重要的句子或段落。本方法主要是利用句子中的关键词的距离，主要思想和参考来自阮一峰的网络日志http://www.ruanyifeng.com/blog/2013/03/automatic_summarization.html


N=100#单词数量
CLUSTER_THRESHOLD=5#单词间的距离
TOP_SENTENCES=5#返回的top n句子

#分句
def sent_tokenizer(texts):
    start=0
    i=0#每个字符的位置
    sentences=[]
    punt_list='.!?。！？'.decode('utf8') #',.!?:;~，。！？：；～'.decode('utf8')
    for text in texts:
        if text in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sentences.append(texts[start:i+1])#当前标点符号位置
            start=i+1#start标记到下一句的开头
            i+=1
        else:
            i+=1#若不是标点符号，则字符位置继续前移
            token=list(texts[start:i+2]).pop()#取下一个字符
    if start<len(texts):
        sentences.append(texts[start:])#这是为了处理文本末尾没有标点符号的情况
    return sentences

#停用词
def load_stopwordslist(path):
    print('load stopwords...')
    stopwrdlist = []
    f = open('stop_words.txt', 'rb')  # 停止词
    stopwords = f.readlines()
    for i in stopwords:
        i1 = i.decode('gbk')
        i1 = i1.strip("\r\n")
        stopwrdlist.append(i1)
    stopwrods={}.fromkeys(stopwrdlist)
    return stopwrods

#摘要
def summarize(text):
    stopwords=load_stopwordslist('stop_words.txt')
    sentences=sent_tokenizer(text)
    words=[w for sentence in sentences for w in jieba.cut(sentence) if w not in stopwords if len(w)>1 and w!='\t']
    wordfre=nltk.FreqDist(words)
    topn_words=[w[0] for w in sorted(wordfre.items(),key=lambda d:d[1],reverse=True)][:N]
    scored_sentences=_score_sentences(sentences,topn_words)
    #approach 1,利用均值和标准差过滤非重要句子
    avg=numpy.mean([s[1] for s in scored_sentences])#均值
    std=numpy.std([s[1] for s in scored_sentences])#标准差
    mean_scored=[(sent_idx,score) for (sent_idx,score) in scored_sentences if score>(avg+0.5*std)]
    #approach 2，返回top n句子
    top_n_scored=sorted(scored_sentences,key=lambda s:s[1])[-TOP_SENTENCES:]
    top_n_scored=sorted(top_n_scored,key=lambda s:s[0])
    return dict(top_n_summary=[sentences[idx] for (idx,score) in top_n_scored],mean_scored_summary=[sentences[idx] for (idx,score) in mean_scored])

 #句子得分
def _score_sentences(sentences,topn_words):
    scores=[]
    sentence_idx=-1
    for s in [list(jieba.cut(s)) for s in sentences]:
        sentence_idx+=1
        word_idx=[]
        for w in topn_words:
            try:
                word_idx.append(s.index(w))#关键词出现在该句子中的索引位置
            except ValueError:#w不在句子中
                pass
        word_idx.sort()
        if len(word_idx)==0:
            continue
        #对于两个连续的单词，利用单词位置索引，通过距离阀值计算族
        clusters=[]
        cluster=[word_idx[0]]
        i=1
        while i<len(word_idx):
            if word_idx[i]-word_idx[i-1]<CLUSTER_THRESHOLD:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster=[word_idx[i]]
            i+=1
        clusters.append(cluster)
        #对每个族打分，每个族类的最大分数是对句子的打分
        max_cluster_score=0
        for c in clusters:
            significant_words_in_cluster=len(c)
            total_words_in_cluster=c[-1]-c[0]+1
            score=1.0*significant_words_in_cluster*significant_words_in_cluster/total_words_in_cluster
            if score>max_cluster_score:
                max_cluster_score=score
        scores.append((sentence_idx,max_cluster_score))
    return scores;


if __name__=='__main__':
    '''
    dict=summarize(u'腾讯科技讯（刘亚澜）10月22日消息，'
        u'前优酷土豆技术副总裁黄冬已于日前正式加盟芒果TV，出任CTO一职。'
        u'资料显示，黄冬历任土豆网技术副总裁、优酷土豆集团产品技术副总裁等职务，'
        u'曾主持设计、运营过优酷土豆多个大型高容量产品和系统。'
        u'此番加入芒果TV或与芒果TV计划自主研发智能硬件OS有关。'
        u'今年3月，芒果TV对外公布其全平台日均独立用户突破3000万，日均VV突破1亿，'
        u'但挥之不去的是业内对其技术能力能否匹配发展速度的质疑，'
        u'亟须招揽技术人才提升整体技术能力。'
        u'芒果TV是国内互联网电视七大牌照方之一，之前采取的是“封闭模式”与硬件厂商预装合作，'
        u'而现在是“开放下载”+“厂商预装”。'
        u'黄冬在加盟土豆网之前曾是国内FreeBSD（开源OS）社区发起者之一，'
        u'是研究并使用开源OS的技术专家，离开优酷土豆集团后其加盟果壳电子，'
        u'涉足智能硬件行业，将开源OS与硬件结合，创办魔豆智能路由器。'
        u'未来黄冬可能会整合其在开源OS、智能硬件上的经验，结合芒果的牌照及资源优势，'
        u'在智能硬件或OS领域发力。'
        u'公开信息显示，芒果TV在今年6月对外宣布完成A轮5亿人民币融资，估值70亿。'
        u'据芒果TV控股方芒果传媒的消息人士透露，芒果TV即将启动B轮融资。')'''
    s = u'''要说现在当红的90后男星，那就不得不提鹿晗、吴亦凡、杨洋、张艺兴、黄子韬、陈学冬、刘昊然，
    2016年他们带来不少人气爆棚的影视剧。这些90后男星不仅有颜值、有才华，还够努力，2017年他们又有哪
    些傲娇的作品呢？到底谁会成为2017霸屏男神，让我们拭目以待吧。鹿晗2016年参演《盗墓笔记》、《长城》
    、《摆渡人》等多部电影，2017年他将重心转到了电视剧。他和古力娜扎主演的古装奇幻电视剧《择天记》将在
    湖南卫视暑期档播出，这是鹿晗个人的首部电视剧，也是其第一次出演古装题材。该剧改编自猫腻的同名网络小
    说，讲述在人妖魔共存的架空世界里，陈长生(鹿晗饰演)为了逆天改命，带着一纸婚书来到神都，结识了一群志
    同道合的小伙伴，在国教学院打开一片新天地。吴亦凡在2017年有更多的作品推出。周星驰监制、徐克执导的春
    节档《西游伏魔篇》，吴亦凡扮演“有史以来最帅的”唐僧。师徒四人在取经的路上，由互相对抗到同心合力，成
    为无坚不摧的驱魔团队。吴亦凡还和梁朝伟、唐嫣合作动作片《欧洲攻略》，该片讲述江湖排名第一、第二的林先
    生(梁朝伟饰)和王小姐(唐嫣饰)亦敌亦友，二人与助手乐奇(吴亦凡饰)分别追踪盗走“上帝之手”地震飞弹的苏菲，
    不想却引出了欧洲黑帮、美国CIA、欧盟打击犯罪联盟特工们的全力搜捕的故事。吴亦凡2017年在电影方面有更大
    突破，他加盟好莱坞大片《极限特工3：终极回归》，与范·迪塞尔、甄子丹、妮娜·杜波夫等一众大明星搭档，为
    电影献唱主题曲《JUICE》。此外，他还参演吕克·贝松执导的科幻电影《星际特工：千星之城》，该片讲述一个发
    生在未来28世纪星际警察穿越时空的故事，影片有望2017年上映。'''
    dict = summarize(s)
    print('-----------approach 1-------------')
    for sent in dict['top_n_summary']:
        print(sent)
    print('-----------approach 2-------------')
    for sent in dict['mean_scored_summary']:
        print(sent)