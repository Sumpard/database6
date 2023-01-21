import json
import re
import pandas as pd

with open("cate.json", "r", encoding="utf8") as fin:
    cate = json.load(fin)

df = pd.read_csv("dangdang-neww.csv")
for idx, row in df.iterrows():
    id = re.search(r"/(\d+)\.html", row["详情页"]).group(1)
    df.loc[idx, "keys"] = json.dumps(cate[id]["keys"], ensure_ascii=False)
    df.loc[idx, "cates"] = json.dumps(cate[id]["cates"], ensure_ascii=False)
    df.loc[idx, "desc"] = cate[id]["desc"]

df.to_csv("dangdang-newww.csv", index=False)