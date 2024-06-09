import requests
import os
import json
from pprint import pprint

#リポジトリの設定
URL = 'https://api.github.com/repos/shingo-fukamatsu/AsciiDoc_plantUML/{}'
AUTH = 'token {}'
headers = {'Authorization': AUTH.format(os.getenv('GITHUB_ACCESS_TOKEN'))}

# openのPRを取得
#r = requests.get(URL.format('pulls?&state=open'), headers=headers)
r = requests.get(URL.format('pulls?&state=close'), headers=headers)

# JSONファイルとして保存
with open('r.json', 'w', encoding='utf-8') as f:
    json.dump(r.json(), f, ensure_ascii=False, indent=4)

pprint (r.json())
pprint ("-----------------------------------------------")

#PR1のコメントを取得
r = requests.get(URL.format('issues/1/comments'), headers=headers)
pprint (r.json())
pprint ("-----------------------------------------------")

for i in range(len(r.json())):      #PRのコメント数を取得
    pprint (r.json()[i]["body"])    #PRのコメント内容を取得
