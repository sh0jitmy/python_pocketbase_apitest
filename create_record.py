import requests
import json
import time

# PocketBaseサーバーのURL
base_url = "http://localhost:8090"
collection_name = "example_collection"
records_url = f"{base_url}/api/collections/{collection_name}/records"

# 管理者トークン（適切に置き換えてください）
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2xsZWN0aW9uSWQiOiJwYmNfMzE0MjYzNTgyMyIsImV4cCI6MTczNDAxNzE0MSwiaWQiOiJhNnNlOWU4N2Q3cWN0eHUiLCJyZWZyZXNoYWJsZSI6ZmFsc2UsInR5cGUiOiJhdXRoIn0.vTU8_a90nlMKSePkttgbCrUa7zXSkoQvHrhFBTc1E2Y"
}

# JSONファイルのパス
json_file_path = "records.json"

# コレクション内のレコード数を取得
def get_record_count():
    response = requests.get(records_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["totalItems"], data["items"]
    else:
        print(f"Error fetching records: {response.status_code}")
        print(response.text)
        return 0, []

# レコードを追加または更新
def upsert_record(record, index_to_update=None):
    if index_to_update is None:
        # 新規作成
        response = requests.post(records_url, headers=headers, json=record)
    else:
        # 更新
        record_id = index_to_update["id"]
        update_url = f"{records_url}/{record_id}"
        response = requests.patch(update_url, headers=headers, json=record)
    
    if response.status_code in [200, 204]:
        print(f"Record {'updated' if index_to_update else 'created'} successfully.")
    else:
        print(f"Error {'updating' if index_to_update else 'creating'} record: {response.status_code}")
        print(response.text)

# メイン処理
def main():
    try:
        # レコードデータをJSONファイルから読み込む
        with open(json_file_path, "r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError:
        print(f"Error: {json_file_path} が見つかりません。")
        return
    except json.JSONDecodeError as e:
        print(f"Error: JSONファイルの形式が正しくありません。{e}")
        return

    # コレクション内の既存レコード数を確認
    current_count, existing_records = get_record_count()
    max_records = 1000
    print(f"Current record count: {current_count}")

    # レコードを追加または更新
    for i, record in enumerate(records):
        if current_count < max_records:
            # 最大数に達していない場合は新規作成
            upsert_record(record)
            current_count += 1
        else:
            # 最大数を超えた場合はリングバッファ形式で更新
            index_to_update = existing_records[i % max_records]
            upsert_record(record, index_to_update)

        # デモのためにウェイトを追加（削除可能）
        time.sleep(0.1)

if __name__ == "__main__":
    main()
