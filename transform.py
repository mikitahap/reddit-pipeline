from extract import Extractor
import re
import joblib
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

extractor = Extractor()
data = extractor.extract()

model = joblib.load('model.pkl')
vectorizer = joblib.load("vectorizer.pkl")

engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/reddit_pipeline")
metadata = MetaData()
posts = Table(
    "posts", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String),
    Column("score", Integer),
    Column("classification", String),
)

def save_to_db(transformed_data):
    with engine.connect() as connection:
        connection.execute(posts.insert(), transformed_data)
        connection.commit()

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

transformed_data = []
data_list = list(zip(titles, scores, y_pred))
data_list = sorted(data_list, key=lambda x: x[1], reverse=True)

for title, score, classifier in data_list:
    row = {"title": title, "score": score, "classification": classifier}
    transformed_data.append(row)

save_to_db(transformed_data)