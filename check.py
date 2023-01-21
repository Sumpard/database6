import json
import re
import pandas as pd

with open("cate.json", "r", encoding="utf8") as fin:
    cate = json.load(fin)

df = pd.read_csv("dangdang-neww.csv")
for idx, row in df.iterrows():
    id = re.search(r"/(\d+)\.html", row["详情页"]).group(1)
    df.loc[idx, "more"] = json.dumps(cate[id], ensure_ascii=False)

df.to_csv("dangdang-newww.csv", index=False)