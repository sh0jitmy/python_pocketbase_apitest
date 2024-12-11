import requests
import json

# PocketBaseサーバーのURL
url = "http://localhost:8090/api/collections"

# 管理者トークン（適切に置き換えてください）
# トークンは_superusersのrecord edit のImpersonateでtoken生成してコピー
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2xsZWN0aW9uSWQiOiJwYmNfMzE0MjYzNTgyMyIsImV4cCI6MTczNDAxNzE0MSwiaWQiOiJhNnNlOWU4N2Q3cWN0eHUiLCJyZWZyZXNoYWJsZSI6ZmFsc2UsInR5cGUiOiJhdXRoIn0.vTU8_a90nlMKSePkttgbCrUa7zXSkoQvHrhFBTc1E2Y"
}

# JSONファイルのパス
json_file_path = "collection.json"

# JSONファイルを読み込む
try:
    with open(json_file_path, "r", encoding="utf-8") as file:
        collection_definition = json.load(file)
except FileNotFoundError:
    print(f"Error: {json_file_path} が見つかりません。")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: JSONファイルの形式が正しくありません。{e}")
    exit(1)

# POSTリクエストを送信
response = requests.post(url, headers=headers, json=collection_definition)

# 結果を表示
if response.status_code == 200:
    print("コレクションが正常に作成されました。")
else:
    print(f"エラーが発生しました: {response.status_code}")
    print(response.text)
