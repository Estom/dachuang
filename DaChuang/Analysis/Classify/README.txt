依赖的Python包
numpy 1.13.1
scipy 0.19.1

中文文本分类：使用前需要将train.sql文件导入数据库，并在数据中nwpu_news等表的最后一列加入字段‘class’，最后会将分好的类别放入这一列。

FormatData.py ：一些工具函数的集合

TrainClassification.py :分类器构建程序，运行一次生成分类器文件存在train_word_bag_my文件夹中，不需要多次构建分类器。
classification.py :
    分类文件，使用时需要先选择对那张表进行分类。  