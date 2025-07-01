import os
import pytest
from unittest.mock import patch, Mock
from dotenv import load_dotenv
from main import get_train_info, parse_train_info

# .envファイルから環境変数を読み込む
load_dotenv()

@patch('main.requests.get')
def test_get_train_info_success(mock_get):
    # 環境変数からAPIキーを取得
    api_key = os.getenv("API_KEY")
    assert api_key is not None, "API_KEYが.envファイルに設定されていません。"

    # モックの準備
    mock_response = Mock()
    expected_json = [{"odpt:trainInformationText": "平常運転です。"}]
    mock_response.status_code = 200
    mock_response.json.return_value = expected_json
    mock_get.return_value = mock_response

    # テスト対象の関数を呼び出し
    train_info = get_train_info()

    # アサーション
    expected_url = "https://api.odpt.org/api/v4/odpt:TrainInformation"
    expected_params = {"acl:consumerKey": api_key}
    mock_get.assert_called_once_with(expected_url, params=expected_params)
    assert train_info == expected_json

@patch('main.requests.get')
def test_get_train_info_failure(mock_get):
    # 環境変数からAPIキーを取得
    api_key = os.getenv("API_KEY")
    assert api_key is not None, "API_KEYが.envファイルに設定されていません。"

    # モックの準備 (ステータスコード500を想定)
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    # テスト対象の関数を呼び出し
    train_info = get_train_info()

    # アサーション
    assert train_info is None

def test_parse_train_info():
    # テスト用のAPIレスポンスデータ
    sample_data = [
        {
            'odpt:railway': 'odpt.Railway:TokyoMetro.Ginza',
            'odpt:trainInformationText': {'ja': '現在、平常どおり運転しています。'}
        },
        {
            'odpt:railway': 'odpt.Railway:MIR.TsukubaExpress',
            'odpt:trainInformationStatus': {'ja': '遅延'},
            'odpt:trainInformationText': {'ja': 'つくばエクスプレス線は、落雷の影響で、上下線に遅れがでています。'}
        }
    ]

    # 期待される出力
    expected = [
        {
            "line_name": "Ginza",
            "status": "平常運転",
            "description": "現在、平常どおり運転しています。"
        },
        {
            "line_name": "TsukubaExpress",
            "status": "遅延あり",
            "description": "つくばエクスプレス線は、落雷の影響で、上下線に遅れがでています。"
        }
    ]

    # 関数の呼び出しとアサーション
    assert parse_train_info(sample_data) == expected
