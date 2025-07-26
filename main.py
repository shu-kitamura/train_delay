import json
import os
import requests

import streamlit as st
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

def fetch_odpt():
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
    NORMAL_DESCRIPTIONS = ["平常", "遅延はありません"]

    if not data:
        return []

    parsed_list = []
    for info in data:
        line_name_full = info.get('odpt:railway')
        line_name = line_name_full.split(':')[-1]

        description = info.get('odpt:trainInformationText')
        is_delayed = not any(normal in description.get("ja") for normal in NORMAL_DESCRIPTIONS)

        parsed_list.append({
            "line_name": line_name,
            "description": description.get("ja"),
            "is_delayed": is_delayed
        })
    return parsed_list

def get_train_info():
    raw_info = fetch_odpt()
    if raw_info:
        parsed_info = parse_train_info(raw_info)
        return json.dumps(parsed_info, ensure_ascii=False)
    else:
        error_message = {"error": "情報の取得に失敗しました。"}
        return json.dumps(error_message, ensure_ascii=False)

if __name__ == '__main__':
    st.title("鉄道遅延情報")

    st.set_page_config(
        page_title="鉄道遅延情報",
        page_icon="🚆",
    )

    train_info = get_train_info()

    train_info_list = []
    if isinstance(train_info, str):
        try:
            train_info_list = json.loads(train_info)
        except json.JSONDecodeError:
            st.error("運行情報の取得に失敗しました。形式が正しくありません。")
            st.write("受信したデータ:")
            st.code(train_info)
            train_info_list = None

    if isinstance(train_info_list, dict) and "error" in train_info_list:
        st.error(train_info_list["error"])
    else:
        delayed_lines = []
        for info in train_info_list:
            if info.get("is_delayed"):
                delayed_lines.append(info)

        if delayed_lines:
            df = pd.DataFrame(delayed_lines)
            st.dataframe(df)
        else:
            st.success("現在、遅延情報はありません。")

    st.markdown("---")
    st.markdown("### 注意事項")
    st.markdown("本アプリケーションが利用する公共交通データは、公共交通オープンデータセンターにおいて提供されるものです。")
    st.markdown("公共交通事業者により提供されたデータを元にしていますが、必ずしも正確・完全なものとは限りません。"
                "本アプリケーションの表示内容について、公共交通事業者への直接の問合せは行わないでください。")
    st.markdown("本アプリケーションに関する問い合わせは、以下のメールアドレスにお願いします。")
    st.markdown("shusei3316@yahoo.co.jp")