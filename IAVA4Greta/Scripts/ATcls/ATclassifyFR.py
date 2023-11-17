from sklearn.svm import LinearSVC

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import warnings
warnings.simplefilter('ignore')
import itertools
import sys
import pickle
import torch
from transformers import AutoModel, AutoTokenizer

from transformers.utils import logging
logging.get_logger("transformers").setLevel(logging.ERROR)
# import transformers
# from transformers import BertTokenizer

# @author Kazuhrio Shidara
# @author Jieyeon Woo

class AT_model_tfidf(object):
    def __init__(self):
        self.line = license
        self.merge = pd.read_csv('./Scripts/ATcls/automaticthought_book_fr.csv',header=0)
        
    def tfidf_loo(self, train_sentences, test_sentences):
        cv = CountVectorizer()
        wc_train = cv.fit_transform(train_sentences)
        wc_test = cv.transform(test_sentences)
        ttf = TfidfTransformer()
        tfidf_train = ttf.fit_transform(wc_train)
        tfidf_test = ttf.transform(wc_test)
        df_tfidf_train = (pd.DataFrame(tfidf_train.toarray(), columns=cv.get_feature_names(), index=train_sentences))
        df_tfidf_test = (pd.DataFrame(tfidf_test.toarray(), columns=cv.get_feature_names(), index=test_sentences))
        return  df_tfidf_train, df_tfidf_test
    
    def ATsvm(self, sentence):
        lines = self.merge.iloc[:, [4]].values.tolist()
        labels = self.merge.iloc[:, [13]].values.tolist()
        
        for key, val in enumerate(lines):
            lines[key][0] = val[0].replace(',',"")
        lines = list(itertools.chain.from_iterable(lines))
        x_merge = np.array(lines)
        y_merge = np.array(labels)

        y_train=np.reshape(y_merge,(-1))

        df_tfidf_train, df_tfidf_test = self.tfidf_loo(x_merge, [sentence])
        clf = LinearSVC()
        clf.fit(df_tfidf_train, y_train) 
        y_pred = clf.predict(df_tfidf_test) # 1=success to identiry, 0=fail to identify
        return y_pred[0]

class AT_model_bert(object):
    def __init__(self):
        self.line = license
        self.tknz = AutoTokenizer.from_pretrained("dbmdz/bert-base-french-europeana-cased")
        self.bertemb = AutoModel.from_pretrained("dbmdz/bert-base-french-europeana-cased")
        self.merge = pd.read_csv('./Scripts/ATcls/automaticthought_book_fr.csv', header = 0)
        try:
            with open('./Scripts/ATcls/model.pickle', 'rb') as f:
                self.clf = pickle.load(f)
        except:
            labels = self.merge.iloc[:, [13]].values.tolist()
            y_merge = np.array(labels)

            y_train=np.reshape(y_merge,(-1))        
            clf = LinearSVC()

            df_tfidf_train = pd.read_csv('./Scripts/ATcls/Bert_automaticthought_fr.csv', header = None, index_col=0)
            df_tfidf_train = df_tfidf_train.values
            self.clf.fit(df_tfidf_train, y_train) 

            with open('./Scripts/ATcls/model.pickle', 'wb') as f:
                pickle.dump(clf, f)

    def ATsvm_bert(self, sentence):
        x = self.tknz.encode(sentence)
        x = torch.LongTensor(x).unsqueeze(0)
        a=self.bertemb(x)[0][0][0].tolist()
        a = np.array(a)
        a = a.reshape(1, -1)


        y_pred = self.clf.predict(a) # 1=success to identiry, 0=fail to identify
        return y_pred[0]       
        

if __name__ == '__main__':    
    # print('Please input your Automatic Thought!!')
    sentence = sys.stdin.readline()
    AT_model = AT_model_bert()
    pred = AT_model.ATsvm_bert(sentence)
    print("", flush=True)
    if(pred==1):
        print("true", flush=True)
    else:
        print("false", flush=True)

