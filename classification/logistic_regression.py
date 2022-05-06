#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@license: (C) Copyright 2013-2019.
@contact: xin.jin0010@gmail.com
@software: pycharm
@file: logistic_regression.py
@time: 2/9/21 11:39 AM
@desc:
"""

from classification.utility import load_data_set, load_data_set_by_label
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
path_training = "../data/final_dataset/dataset_traditional/training_set.txt"
path_validation = "../data/final_dataset/dataset_traditional/validation_set.txt"
path_test = "../data/final_dataset/dataset_traditional/test_set.txt"
training_texts, training_labels = load_data_set(path_training)
validation_texts, validation_labels = load_data_set(path_validation)
test_texts, test_labels = load_data_set(path_test)
iot_texts, _ = load_data_set_by_label(path_training, 1)
num_features = 4000
# tfidf_converter_bigram = TfidfVectorizer(max_features=num_features, ngram_range=(2, 2))
# tfidf_converter_bigram.fit(training_texts)
# tfidf_converter_bigram = TfidfVectorizer(max_features=num_features, ngram_range=(2, 2))
file_tuning = open("../data/classifier/logistic_regression/tuning_history.txt", 'a+')


def get_not_used_description():
    used = set()
    with open("../data/dataset/training.txt", 'r') as file:
        for line in file:
            js = json.loads(line)
            used.add(js["pkg_name"])
    with open("../data/dataset/test.txt", 'r') as file:
        for line in file:
            js = json.loads(line)
            used.add(js["pkg_name"])
    res = []
    with open("../data/dataset/non_iot.txt", 'r') as file:
        for line in file:
            js = json.loads(line)
            if js["pkg_name"] not in used:
                res.append(js["description"])
    return res


def tune_parameter():
    num_features = 400
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(iot_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    # test_set = tfidf_converter.transform(test_texts).toarray()
    classifier = LogisticRegression(solver='liblinear', class_weight='balanced')
    c_space = np.arange(1, 15)
    # weights = []
    # for i in range(1, 10):
    #     weights.append({0: i * 0.1, 1: 1 - i * 0.1})
    param_grid = {'C': c_space}
    logreg_cv = GridSearchCV(classifier, param_grid, scoring='f1', cv=5)
    logreg_cv.fit(training_set, training_labels)

    print("\n\nInitial tuning on 200 features", file=file_tuning)
    print("Tuned Logistic Regression Parameters: {}".format(logreg_cv.best_params_), file=file_tuning)
    print("Best score is {}".format(logreg_cv.best_score_), file=file_tuning)


performance = []
feature_vector = []


def evaluate_num_features():
    num_features = 100
    print("\n{}".format(datetime.datetime.now()), file=file_tuning)
    print("Evaluate # of features", file=file_tuning)
    while num_features <= 6000:
        feature_vector.append(num_features)
        tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
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


def print_features(path_file, feature_list):
    with open(path_file, 'w+') as file:
        for feature in feature_list:
            print(feature, file=file)


def get_features():
    iot_texts, iot_labels = load_data_set_by_label(path_training, 1)
    num_features = 200
    # print(len(iot_texts), len(iot_labels))
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(iot_texts)
    print(tfidf_converter.get_feature_names())
    print_features("../data/classifier/features/200_features_purely_from_iot_description.txt", tfidf_converter.get_feature_names())

    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(training_texts)
    print(tfidf_converter.get_feature_names())
    print(len(training_texts), len(training_labels))
    print_features("../data/classifier/features/200_features_from_both_description.txt", tfidf_converter.get_feature_names())


def get_num_words_each_description():
    import json
    import statistics
    word_nums = []
    with open("../data/classifier/features/num_words_in_descriptions_test.txt", 'w+') as file:
        for text in test_texts:
            words = ToktokTokenizer().tokenize(text)
            print(len(words), file=file)
            word_nums.append(len(words))
    print(statistics.mean(word_nums))


def selective_feature_classification():
    # num_features = 200

    # iot features classification
    print("\n----iot features classification----")
    iot_texts, _ = load_data_set_by_label(path_training, 1)
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(iot_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    test_set = tfidf_converter.transform(test_texts).toarray()
    # print(test_set[0])
    # print(test_texts[0])
    clf = LogisticRegression(C=10, class_weight={0: 0.4, 1: 0.6}, solver='liblinear')
    clf.fit(training_set, training_labels)
    prediction = clf.predict(test_set)
    print("F1: {}".format(f1_score(test_labels, prediction)))
    print("Accuracy: {}".format(accuracy_score(test_labels, prediction)))
    print("Precision: {}".format(precision_score(test_labels, prediction)))
    print("Recall: {}".format(recall_score(test_labels, prediction)))

    # all features classification
    print('\n----both features classification----')
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(training_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    test_set = tfidf_converter.transform(test_texts).toarray()
    clf = LogisticRegression(C=10, class_weight={0: 0.4, 1: 0.6}, solver='liblinear')
    clf.fit(training_set, training_labels)
    prediction = clf.predict(test_set)
    print("F1: {}".format(f1_score(test_labels, prediction)))
    print("Accuracy: {}".format(accuracy_score(test_labels, prediction)))
    print("Precision: {}".format(precision_score(test_labels, prediction)))
    print("Recall: {}".format(recall_score(test_labels, prediction)))


def evaluate_grams():
    num_gram = 1
    num_features = 200
    print("\n{}".format(datetime.datetime.now()), file=file_tuning)
    print("Evaluate # of grams", file=file_tuning)
    while num_gram <= 5:
        feature_vector.append(num_gram)
        tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(num_gram, num_gram))
        training_set = tfidf_converter.fit_transform(training_texts).toarray()
        test_set = tfidf_converter.transform(test_texts).toarray()
        clf = LogisticRegression(C=10, class_weight={0: 0.4, 1: 0.6}, solver='liblinear')
        clf.fit(training_set, training_labels)
        prediction = clf.predict(test_set)
        print("num_gram = {}".format(num_features), file=file_tuning)
        evaluate_test(prediction)
        num_features += 50
        num_gram += 1


def load_test_pkg_names():
    pkgs = []
    with open("../data/dataset/test.txt", 'r') as file:
        for line in file:
            js = json.loads(line)
            pkgs.append(js["pkg_name"])
    return pkgs


def get_failure_samples():
    pkgs = load_test_pkg_names()
    num_features = 200
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    training_set = tfidf_converter.fit_transform(training_texts).toarray()
    features = list(tfidf_converter.get_feature_names())
    test_set = tfidf_converter.transform(test_texts).toarray()
    clf = LogisticRegression(C=10, class_weight={0:0.4, 1:0.6}, solver='liblinear')
    clf.fit(training_set, training_labels)
    prediction = clf.predict(test_set)
    print(accuracy_score(prediction, test_labels))
    tn, fp, fn, tp = confusion_matrix(test_labels, prediction).ravel()
    print(tn, fp, fn, tp)
    # features_str = ""
    # value_str = ""
    for i, predicted in enumerate(prediction):
        features_str = ""
        value_str = ""
        if predicted == 0 and test_labels[i] == 1:
            print("{},{},{}".format(i, pkgs[i], test_texts[i]))
            vectorized = list(test_set[i])
            print(vectorized)
            for i, v in enumerate(vectorized):
                features_str = features_str+features[i] + ','
                value_str = value_str + str(v) +','

                if v > 0:
                    print("\"{}\": {}".format(features[i], v))
            print(features_str)
            print(value_str)


def drop_sample(train_texts, train_labels, ratio):
    texts = []
    labels = []
    for i, sample in enumerate(train_texts):
        if random.random() > ratio:
            continue
        texts.append(sample)
        labels.append(train_labels[i])
    return texts, labels


def get_features_more_non_iot():

    # 200 features for initial training set
    num_features = 200
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(training_texts)
    print(tfidf_converter.get_feature_names())

    # 200 features for initial training set + 30*291 non_iot samples
    non_iot_texts, non_iot_labels = get_non_iot_smaples_randomly(30*291)
    new_training_texts = training_texts + non_iot_texts
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(new_training_texts)
    print(tfidf_converter.get_feature_names())


def add_more_non_iot_samples():
    # num_features = 200
    non_iot_sizes = [i * 291 for i in range(0, 31)]
    for i in non_iot_sizes:
        print("{} new non iot samples".format(i))

        non_iot_texts, non_iot_labels = get_non_iot_smaples_randomly(i)
        feature_vector.append((len(training_texts) / 2 + len(non_iot_texts)) * 1.0 / (len(training_texts) + len(non_iot_texts)))
        num_features = int((len(training_texts) + len(non_iot_texts)) * 200 * 1.0 / 582)
        tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
        new_training_texts = training_texts + non_iot_texts
        new_training_labels = np.asarray(list(training_labels) + list(non_iot_labels), dtype=int)
        # iot_texts, _ = load_data_set_by_label(path_training, 1)
        # tfidf_converter.fit(iot_texts)
        # print(tfidf_converter.get_feature_names())
        new_training_set = tfidf_converter.fit_transform(new_training_texts).toarray()
        test_set = tfidf_converter.transform(test_texts).toarray()
        clf = LogisticRegression(C=10, class_weight='balanced', solver='liblinear')
        clf.fit(new_training_set, new_training_labels)
        prediction = clf.predict(test_set)
        print("num_non_iot_samples = {}".format((len(training_texts) / 2 + len(non_iot_texts)) ), file=file_tuning)
        evaluate_test(prediction)


available_non_iot_descriptions = get_not_used_description()


def get_non_iot_smaples_randomly(num_samples):
    texts = random.sample(available_non_iot_descriptions, num_samples)
    labels = [0] * num_samples
    labels = np.asarray(labels, dtype=np.int)
    return texts, labels

def decrease_size_of_training_set():
    num_features = 200
    for i in range(1, 11):
        ratio = i * 0.1
        train_texts, train_labels = drop_sample(training_texts, training_labels, ratio)
        feature_vector.append(len(train_texts))
        tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
        training_set = tfidf_converter.fit_transform(train_texts).toarray()
        test_set = tfidf_converter.transform(test_texts).toarray()
        clf = LogisticRegression(C=10, class_weight={0: 0.5, 1: 0.5}, solver='liblinear')
        clf.fit(training_set, train_labels)
        prediction = clf.predict(test_set)
        print("num_size = {}".format(len(train_texts)), file=file_tuning)
        print("F1: {}".format(f1_score(test_labels, prediction)), file=file_tuning)
        print("Accuracy: {} \n".format(accuracy_score(test_labels, prediction)), file=file_tuning)
        performance.append(accuracy_score(test_labels, prediction))


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
    # f1_performance


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
    for i, f in enumerate(feature_vector):
        if f==3000:
            print(performance[i])
    plt.plot(feature_vector, f1, marker='o', label="F1-score")
    plt.plot(feature_vector, accuracy, marker='*', label="Accuracy")
    plt.plot(feature_vector, precision, marker='v', label="Precision")
    plt.plot(feature_vector, recall, marker='^', label="Recall")
    plt.legend()
    plt.show()


def classify_test_set():
    tfidf_converter = TfidfVectorizer(max_features=num_features, ngram_range=(2, 3))
    tfidf_converter.fit(training_texts)
    training_set = tfidf_converter.transform(training_texts).toarray()
    validation_set = tfidf_converter.transform(validation_texts).toarray()
    test_set = tfidf_converter.transform(test_texts).toarray()
    clf = LogisticRegression(C=10, class_weight='balanced', solver='liblinear')
    clf.fit(training_set, training_labels)
    prediction = clf.predict(test_set)
    evaluate_test(prediction, use_validation=False)


if __name__ == '__main__':
    classify_test_set()
    # get_failure_samples()
    # tune_parameter()
    # evaluate_num_features()
    # print(feature_vector)
    # print(performance)
    # plot_performance()
    # print(performance)
    # decrease_size_of_training_set()
    # plot_figure()
    # get_features()
    # selective_feature_classification()
    # get_num_words_each_description()
    # add_more_non_iot_samples()
    # plot_figure()
    # get_features_more_non_iot()