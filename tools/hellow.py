import requests

print("pythonが実行されました")
print("GithubActionsでpythonを動かすことに成功しました")

# Webサイトの情報を変数rに格納し、そのうちのテキスト部分を出力
r = requests.get("https://news.yahoo.co.jp/")
print(r.text)