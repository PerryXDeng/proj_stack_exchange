from sys import argv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from joblib import load
from sklearn.linear_model import SGDClassifier

pairs = [["stackoverflow.com", "academia.stackexchange.com"],["stackoverflow.com", "softwareengineering.stackexchange.com"]]

def main():
    if len(argv) != 4:
        print("usage: python tasktype sitepair post")
        print("tasktype is either SVM or NB")
        print("sitepair is either 1 (for so/ac) or 2 (for so/se)")
        exit()
    else:
        task_type = argv[1]
        sitepair = int(argv[2])
        message = argv[3]
        model = None
        if task_type == "SVM":
            if sitepair == 1:
                model = load("10k_so_ac_SVM_model.joblib")
            else:
                model = load("10k_so_se_SVM_model.joblib")
        elif task_type == "NB":
            if sitepair == 1:
                model = load("10k_so_ac_bayes_model.joblib")
            else:
                model = load("10k_so_se_bayes_model.joblib")
        if model is None:
            print("incorrect args")
            exit()
        else:
            prediction = model.predict([message])[0]
            print("Message belongs to site: " + pairs[sitepair - 1][prediction - 1])

main()
