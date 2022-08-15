#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: logistic_regression.py
@time: 4/19/21 7:01 PM
@desc:
"""
from ui_text_classification.utility import load_data_set, load_data_set_by_label
from classification.utility import load_data_set as load_data_set_descip
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix
import datetime
# %matplotlib inline
import matplotlib.pyplot as plt
import random
from nltk.tokenize.toktok import ToktokTokenizer
import json
import random

# path_training = "../data/dataset/training.txt"
# path_training = "../data/dataset/training_large.txt"
# path_test = "../data/dataset/test.txt"
# path_training = "../data/ui_text_dataset/traditional/training_set.txt"
# path_validation = "../data/ui_text_dataset/traditional/validation_set.txt"

# path_training = "../data/final_dataset/dataset_traditional/training_set.txt"
# path_validation = "../data/final_dataset/dataset_traditional/validation_set.txt"
# path_test = "../data/ui_text_dataset/traditional/test_set.txt"
path_training = "data/dataset_traditional/training_set.txt"
path_validation = "data/dataset_traditional/validation_set.txt"
path_test = "data/dataset_traditional/test_set.txt"
training_texts, training_labels = load_data_set(path_training)
validation_texts, validation_labels = load_data_set(path_validation)
test_texts, test_labels = load_data_set(path_test)
# test_texts, test_labels = [], []

# iot_texts, _ = load_data_set_by_label(path_training, 1)
num_features = 3200

file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')

performance = []
feature_vector = []


def evaluate_test(predict_labels, use_validation=True):
    if use_validation:
        real_labels = validation_labels
    else:
        real_labels = test_labels
    f1 = f1_score(real_labels, predict_labels)
    accuracy = accuracy_score(real_labels, predict_labels)
    precision = precision_score(real_labels, predict_labels)
    recall = recall_score(real_labels, predict_labels)
    print("F1: {}".format(f1), file=file_tuning)
    print("Accuracy: {}".format(accuracy), file=file_tuning)
    print("Precision: {}".format(precision), file=file_tuning)
    print("Recall: {}\n".format(recall), file=file_tuning)
    performance.append([f1, accuracy, precision, recall])


def tune_grams():
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(1, 3), max_df=0.7)
    tfidf_converter.fit(training_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    validation_set = tfidf_converter.transform(validation_texts).toarray()
    clf = LogisticRegression(C=10, class_weight='balanced', solver='liblinear')
    clf.fit(training_set, training_labels)
    prediction = clf.predict(validation_set)
    evaluate_test(prediction)


def evaluate_num_features():
    num_features = 1000
    print("\n{}".format(datetime.datetime.now()), file=file_tuning)
    print("Evaluate # of features", file=file_tuning)
    while num_features <= 4000:
        feature_vector.append(num_features)
        tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(1, 1), max_df=0.9)
        tfidf_converter.fit(training_texts)
        training_set = tfidf_converter.transform(training_texts).toarray()
        validation_set = tfidf_converter.transform(validation_texts).toarray()
        clf = LogisticRegression(C=10, class_weight='balanced', solver='liblinear')
        clf.fit(training_set, training_labels)
        prediction = clf.predict(validation_set)
        print("num_features = {}".format(num_features), file=file_tuning)
        print("num_features = {}".format(num_features))
        evaluate_test(prediction)
        num_features += 100
    print(feature_vector)


def plot_figure():
    plt.style.use('seaborn-whitegrid')
    plt.plot(feature_vector, performance, linestyle='solid')
    plt.show()


def plot_performance():
    # feature_vector = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000, 5100, 5200, 5300, 5400, 5500, 5600, 5700, 5800, 5900, 6000]
    # performance = [[0.8896741264232431, 0.8976693372177713, 0.965076660988075, 0.8252002913328478], [0.9211332312404289, 0.9249817916970139, 0.9709443099273608, 0.8761835396941005], [0.9288956127080181, 0.9315367807720321, 0.966168371361133, 0.8943918426802622], [0.9327286470143612, 0.9351784413692644, 0.969363707776905, 0.898761835396941], [0.9376876876876877, 0.9395484340859432, 0.9674670797831139, 0.909686817188638], [0.9375470278404816, 0.9395484340859432, 0.9696498054474708, 0.9075018208302986], [0.9375470278404816, 0.9395484340859432, 0.9696498054474708, 0.9075018208302986], [0.9372416384817738, 0.9391842680262199, 0.968167701863354, 0.9082301529497451], [0.9375470278404816, 0.9395484340859432, 0.9696498054474708, 0.9075018208302986], [0.9371471584493789, 0.9391842680262199, 0.969626168224299, 0.9067734887108522], [0.9356417011667293, 0.937727603787327, 0.9680685358255452, 0.9053168244719592], [0.9373358348968104, 0.9391842680262199, 0.9667182662538699, 0.909686817188638], [0.9328330206378986, 0.9348142753095412, 0.9620743034055728, 0.9053168244719592], [0.9343832020997375, 0.9362709395484341, 0.9629057187017002, 0.9075018208302986], [0.9366804046459347, 0.9384559359067735, 0.9645061728395061, 0.9104151493080845], [0.9374766005241483, 0.9391842680262199, 0.9645608628659477, 0.9118718135469774], [0.9401197604790419, 0.9417334304442826, 0.9668976135488837, 0.9147851420247632], [0.9376167351512887, 0.9391842680262199, 0.9624233128834356, 0.9140568099053168], [0.93717277486911, 0.9388201019664967, 0.9631053036126057, 0.9126001456664239], [0.9375700934579438, 0.9391842680262199, 0.9631336405529954, 0.9133284777858703], [0.937125748502994, 0.9388201019664967, 0.9638183217859893, 0.9118718135469774], [0.9364248317127899, 0.9380917698470502, 0.962336664104535, 0.9118718135469774], [0.9384098544232923, 0.9399126001456665, 0.9624808575803981, 0.9155134741442098], [0.9414397612831032, 0.9428259286234523, 0.9648318042813455, 0.9191551347414421], [0.942803738317757, 0.9442825928623453, 0.9685099846390169, 0.9184268026219956], [0.9416167664670658, 0.9431900946831755, 0.968437259430331, 0.9162418062636563], [0.9416604338070307, 0.9431900946831755, 0.96771714066103, 0.9169701383831027], [0.9406051550242809, 0.9420975965040058, 0.9654907975460123, 0.9169701383831027], [0.9424083769633509, 0.943918426802622, 0.9684857801691007, 0.9176984705025492], [0.942846469929025, 0.9442825928623453, 0.9677914110429447, 0.9191551347414421], [0.9420993649607771, 0.9435542607428987, 0.9670245398773006, 0.9184268026219956], [0.9417040358744394, 0.9431900946831755, 0.9669992325402916, 0.9176984705025492], [0.9402092675635275, 0.9417334304442826, 0.965464313123561, 0.9162418062636563], [0.9402985074626865, 0.9417334304442826, 0.9640397857689365, 0.9176984705025492], [0.9402539208364451, 0.9417334304442826, 0.9647509578544061, 0.9169701383831027], [0.9413084112149533, 0.9428259286234523, 0.966973886328725, 0.9169701383831027], [0.9417040358744394, 0.9431900946831755, 0.9669992325402916, 0.9176984705025492], [0.9406051550242809, 0.9420975965040058, 0.9654907975460123, 0.9169701383831027], [0.9436356849570736, 0.9450109249817917, 0.9678407350689127, 0.9206117989803351], [0.942846469929025, 0.9442825928623453, 0.9677914110429447, 0.9191551347414421], [0.9443822321761852, 0.9457392571012382, 0.9686064318529862, 0.9213401310997815], [0.9443822321761852, 0.9457392571012382, 0.9686064318529862, 0.9213401310997815], [0.9431988041853512, 0.9446467589220685, 0.9685341519570223, 0.9191551347414421], [0.942803738317757, 0.9442825928623453, 0.9685099846390169, 0.9184268026219956], [0.9425373134328358, 0.943918426802622, 0.9663351185921959, 0.9198834668608885], [0.9443822321761852, 0.9457392571012382, 0.9686064318529862, 0.9213401310997815], [0.9431988041853512, 0.9446467589220685, 0.9685341519570223, 0.9191551347414421], [0.9447348767737117, 0.9461034231609614, 0.9693486590038314, 0.9213401310997815], [0.9432412247946229, 0.9446467589220685, 0.967816091954023, 0.9198834668608885], [0.944693572496263, 0.9461034231609614, 0.9700690713737529, 0.9206117989803351], [0.944693572496263, 0.9461034231609614, 0.9700690713737529, 0.9206117989803351], [0.9443822321761852, 0.9457392571012382, 0.9686064318529862, 0.9213401310997815], [0.9467014535967201, 0.9479242534595775, 0.9694656488549618, 0.9249817916970139], [0.9462686567164179, 0.9475600873998543, 0.9701606732976281, 0.9235251274581209], [0.9455630126771066, 0.9468317552804079, 0.9686783804430863, 0.9235251274581209], [0.9443822321761852, 0.9457392571012382, 0.9686064318529862, 0.9213401310997815], [0.9443822321761852, 0.9457392571012382, 0.9686064318529862, 0.9213401310997815], [0.9432412247946229, 0.9446467589220685, 0.967816091954023, 0.9198834668608885], [0.9442990654205606, 0.9457392571012382, 0.9700460829493087, 0.9198834668608885], [0.9427609427609427, 0.9442825928623453, 0.9692307692307692, 0.9176984705025492]]
    f1 = [p[0] for p in performance]
    accuracy = [p[1] for p in performance]
    precision = [p[2] for p in performance]
    recall = [p[3] for p in performance]
    # for i, f in enumerate(feature_vector):
    #     if f==3000:
    #         print(performance[i])
    plt.plot(feature_vector, f1, marker='o', label="F1-score")
    plt.plot(feature_vector, accuracy, marker='*', label="Accuracy")
    plt.plot(feature_vector, precision, marker='v', label="Precision")
    plt.plot(feature_vector, recall, marker='^', label="Recall")
    plt.legend()
    plt.show()


# training_texts = training_texts + validation_texts
# training_labels = list(training_labels) + list(validation_labels)
# training_labels = np.asarray(training_labels, dtype=np.int)


def classify_test_set():
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(1, 3))

    tfidf_converter.fit(training_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    # validation_set = tfidf_converter.transform(validation_texts).toarray()
    test_set = tfidf_converter.transform(test_texts).toarray()
    clf = LogisticRegression(C=10, class_weight='balanced', solver='liblinear')
    clf.fit(training_set, training_labels)
    prediction = clf.predict(test_set)
    evaluate_test(prediction, use_validation=False)


if __name__ == '__main__':
    # evaluate_num_features()
    # plot_performance()
    classify_test_set()
