ai_modeles = []
methods_dic = {}

import ktrain
import wget
import os
import shutil
        
free_after_download_and_load = False
cache_path = ".cache"
base_url = "https://selamvp.s3.us-east-2.amazonaws.com/"
to_load = {
    #"roberta_eula_08_17_2020" : ["tf_model.preproc", "config.json" , "tf_model.h5"],
    "distillroberta_eula_08_18_2020" : ["tf_model.preproc", "config.json" , "tf_model.h5"]
}  

class AppScope():  
    """
    This class allows to load all models at the beginning of the application, 
    and these models have an application scope (i.e. they are available during the whole life of the application).
    see prediction.views.app_scope method
    """
    def __init__(self):
        pass

    def start_app_scope(self):
        from .utils import mybag_predict, tfidf_predict, bert_predict, get_ktrain_predict_method
        global methods_dic, ai_modeles

        # 1
        methods_dic["Bag of word + Logistic Regression"] = mybag_predict
        methods_dic["TD-IDF + Logistic Regression"] = tfidf_predict
        ai_modeles = list(methods_dic.keys())

        # 2 : can crash
        """
        methods_dic["BERT + Logistic Regression"] = bert_predict
        reloaded_predictors = self.download()
        roberta_tmp = get_ktrain_predict_method(ktrain_predictor = reloaded_predictors["roberta_eula_08_17_2020"]) 
        methods_dic["bert fine_tuning"] = roberta_tmp
        methods_dic["albert fine_tuning"] = roberta_tmp
        methods_dic["roberta fine_tuning"] = roberta_tmp
        methods_dic["xlnet fine_tuning"] = roberta_tmp
        ai_modeles = list(methods_dic.keys())
        """
        
    def download(self):
        
        reloaded_predictors = {}
        if not os.path.isdir(cache_path):
            os.mkdir(cache_path)
        print(cache_path, "cache_path")
        for model_name, files in to_load.items():
            model_path = os.path.join(cache_path, model_name)
            print(model_path, "model_path")
            if not os.path.isdir(model_path):
                os.mkdir(model_path) 
            for file_name in files :
                file_path = os.path.join(model_path, file_name)
                file_url = os.path.join(base_url, model_name, file_name).replace("\\", "/")
                if not os.path.isfile(file_path):
                    # 1
                    wget.download(
                        file_url, file_path
                    )

                    # 2
                    """
                    import requests
                    response = requests.get(file_url, stream = True)
                    dest_file = open(file_path, "wb")
                    for chunk in response.iter_content(chunk_size=1024):
                        dest_file.write(chunk)
                    dest_file.close()
                    """
            reloaded_predictors[model_name] = ktrain.load_predictor(model_path)
            if free_after_download_and_load :
                try:
                    shutil.rmtree(model_path)
                except OSError:
                    pass
                        
        return reloaded_predictors           