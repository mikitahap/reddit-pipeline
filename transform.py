import pandas
from extract import Extractor
import re

extractor = Extractor()
data = extractor.extract()

data_csv = []
for post in data:
    title = post['data']['title']

    title = title.lower()
    title = re.sub(r"\s+", " ", title).strip()
    row = {"title": title, "score": post['data']['score'], "classification": "sports"}
    data_csv.append(row)

df = pandas.DataFrame(data_csv)
df.to_csv("posts.csv", index=False)