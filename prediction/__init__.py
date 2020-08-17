ai_modeles = []
methods_dic = {}

class AppScope():  
    """
    This class allows to load all models at the beginning of the application, 
    and these models have an application scope (i.e. they are available during the whole life of the application).
    see prediction.views.app_scope method
    """
    def __init__(self):
        pass

    def start_app_scope(self):
        from .utils import mybag_predict, tfidf_predict, bert_predict
        global methods_dic, ai_modeles
        methods_dic["Bag of word + Logistic Regression"] = mybag_predict
        methods_dic["TD-IDF + Logistic Regression"] = tfidf_predict
        methods_dic["BERT + Logistic Regression"] = bert_predict
        methods_dic["bert fine_tuning"] = bert_predict
        methods_dic["albert fine_tuning"] = bert_predict
        methods_dic["roberta fine_tuning"] = bert_predict
        methods_dic["xlnet fine_tuning"] = bert_predict
        ai_modeles = list(methods_dic.keys())