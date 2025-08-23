import pandas
from extract import Extractor
import re
import joblib

extractor = Extractor()
data = extractor.extract()
model = joblib.load('model.pkl')
vectorizer = joblib.load("vectorizer.pkl")

titles = []
scores = []
for post in data:
    title = post['data']['title']

    title = title.lower()
    title = re.sub(r"\s+", " ", title).strip()
    titles.append(title)

    scores.append(post['data']['score'])
x_vec = vectorizer.transform(titles)
y_pred = model.predict(x_vec)

data_csv = []
data_list = list(zip(titles, scores, y_pred))
data_list = sorted(data_list, key=lambda x: x[1], reverse=True)

for title, score, classifier in data_list:
    row = {"title": title, "score": score, "classifier": classifier}
    data_csv.append(row)

df = pandas.DataFrame(data_csv)
df.to_csv("posts.csv", index=False)