# Train Delay Information Backend

このプロジェクトは、公共交通オープンデータセンターのAPIを利用して、日本の鉄道の遅延情報を取得し、表示するバックエンドアプリケーションです。

## セットアップ

1.  **依存関係のインストール**:
    `uv` を使用して、必要なPythonパッケージをインストールします。
    ```bash
    uv pip install -r pyproject.toml
    uv pip install pytest python-dotenv
    ```

2.  **APIキーの設定**:
    公共交通オープンデータセンターからAPIキー（`acl:consumerKey`）を取得し、プロジェクトルートに `.env` ファイルを作成して設定します。
    ```
    API_KEY="ここに取得したAPIキーを貼り付け"
    ```
    `.env` ファイルは `.gitignore` に追加されているため、Gitにはコミットされません。

## 実行方法

アプリケーションを実行し、遅延情報をコンソールに表示します。

```bash
uv run python main.py
```

## テストの実行

`pytest` を使用してテストを実行します。

```bash
uv run pytest
```
