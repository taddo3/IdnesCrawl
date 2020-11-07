from src.categorization.analyzer import Analyzer
from src.categorization.predictor import Predictor
from os import path
from json import loads, dumps


def split_train_test(file_name):
    article_number = 0
    if path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as c:
            while True:
                article_number += 1
                line = c.readline()
                if not line:
                    break
                data = line
                while True:
                    line = c.readline()
                    data += line
                    if line[0] == "}":
                        break
                json_data = loads(data)

                if article_number % 10 != 0:
                    with open('../data/train.txt', 'a+', encoding='utf-8') as train_file:
                        train_file.write(dumps(json_data, indent=4))
                        train_file.write('\n')
                else:
                    with open('../data/test.txt', 'a+', encoding='utf-8') as test_file:
                        test_file.write(dumps(json_data, indent=4))
                        test_file.write('\n')


def count_statistics(train_file_name):
    analyzer = Analyzer()
    if path.exists(train_file_name):
        analyzer.make_keywords_statistics(train_file_name)
    return analyzer


def make_predictions(analyzer, category, test_file_name):
    predictor = Predictor(analyzer.category_keyword_score, analyzer.total_keyword_score)
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    if path.exists(test_file_name):
        with open(test_file_name, 'r', encoding='utf-8') as test_file:
            while True:
                line = test_file.readline()
                if not line:
                    break
                data = line
                while True:
                    line = test_file.readline()
                    data += line
                    if line[0] == "}":
                        break
                json_data = loads(data)
                predicted_category = predictor.predict_category(json_data['keywords'])
                if category == predicted_category and json_data['category'] == category:
                    true_positive += 1
                elif category == predicted_category and json_data['category'] != category:
                    false_positive += 1
                elif category != predicted_category and json_data['category'] == category:
                    false_negative += 1
                elif category != predicted_category and json_data['category'] != category:
                    true_negative += 1

    return true_positive, false_positive, false_negative, true_negative


split_train_test('../data/category_keywords_1.txt')
analyzer = count_statistics('../data/train.txt')
TP, FP, FN, TN = make_predictions(analyzer, 'zahranicni', '../data/test.txt')
print('True positive: ' + str(TP))
print('False positive: ' + str(FP))
print('False negative: ' + str(FN))
print('True negative: ' + str(TN))
precision = TP/(TP+FP)
print('Precision: ' + str(precision))
recall = TP/(TP+FN)
print('Recall: ' + str(recall))
accuracy = (TP+TN)/(TP+TN+FP+FN)
print('Accuracy: ' + str(accuracy))
specificity = TN/(TN+FP)
print('Specificity: ' + str(specificity))
fall_out = FP/(TN+FP)
print('Fall-out: ' + str(fall_out))
BACC = (recall+specificity)/2
print('Balanced accuracy: ' + str(BACC))
F1 = 2/((1/precision)+(1/recall))
print('F1: ' + str(F1))

