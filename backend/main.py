import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_train_info():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("APIキーが設定されていません。 .envファイルを確認してください。")

    url = "https://api.odpt.org/api/v4/odpt:TrainInformation"
    params = {"acl:consumerKey": api_key}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_train_info(data):
    if not data:
        return []

    parsed_list = []
    for info in data:
        line_name_full = info.get('odpt:railway', '不明')
        # 'odpt.Railway:Company.Line' の形式から 'Line' の部分を抽出
        line_name = line_name_full.split('.')[-1]

        status_ja = info.get('odpt:trainInformationStatus', {}).get('ja')
        if status_ja and '遅延' in status_ja:
            status = "遅延あり"
        else:
            status = "平常運転"

        description = info.get('odpt:trainInformationText', {}).get('ja', '情報なし')

        parsed_list.append({
            "line_name": line_name,
            "status": status,
            "description": description
        })
    return parsed_list

if __name__ == '__main__':
    raw_info = get_train_info()
    if raw_info:
        parsed_info = parse_train_info(raw_info)
        for train in parsed_info:
            print(f"路線名: {train['line_name']}")
            print(f"  運行状況: {train['status']}")
            print(f"  詳細: {train['description']}")
            print("---")
    else:
        print("情報の取得に失敗しました。")
