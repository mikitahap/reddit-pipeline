from extract import Extractor
import re
import json
import joblib
import os
import logging

class Transformer:
    def __init__(self, raw_data):

        self.__raw_data = raw_data
        self.__transformed_data = []
        base_path = os.path.dirname(__file__)

        self.__model_path = os.path.join(base_path, "model.pkl")
        self.__vectorizer_path = os.path.join(base_path, "vectorizer.pkl")
        self.__model = joblib.load(self.__model_path)
        self.__vectorizer = joblib.load(self.__vectorizer_path)

    def transform(self):
            try:
                titles = []
                scores = []
                for post in self.__raw_data:
                    title = post['data']['title']
                    title = title.lower()
                    title = re.sub(r"\s+", " ", title).strip()
                    titles.append(title)
                    scores.append(post['data']['score'])

                x_vec = self.__vectorizer.transform(titles)
                y_pred = self.__model.predict(x_vec)

                data_list = list(zip(titles, scores, y_pred))
                data_list = sorted(data_list, key=lambda x: x[1], reverse=True)

                for title, score, classifier in data_list:
                    row = {"title": title, "score": score, "classification": classifier}
                    self.__transformed_data.append(row)

                return self.__transformed_data
            except Exception as e:
                print(e)
            return self.__transformed_data
