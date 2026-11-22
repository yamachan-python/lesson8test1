# レシピ投稿ミニアプリ（Flask ＋ SQLAlchemy ＋ Render PostgreSQL）

レシピの一覧と新しい投稿ができる Web アプリです。

## ファイル

- `app.py`：アプリ本体
- `db_init.py`：テーブルを作り、見本のレシピを2件入れる（最初に1回だけ実行）
- `requirements.txt`：使うライブラリ
- `.gitignore`：`.env` などを GitHub に上げないための設定（下の中身で作ってください）

```
__pycache__/
*.pyc
.env
.vscode/
```

## 大事：データベースの URL をコードに書かない

Render のデータベースの URL には、パスワードが入っています。
`app.py` や `db_init.py` に直接書かず、`.env` というファイルに書きます。
`.env` は `.gitignore` に入れて、GitHub に上げません。

`.env` の中身（1行）：

```
DATABASE_URL=（Render の External Database URL）
```

`db_init.py` は、URL の最後に `?sslmode=require` が無ければ自動で足します。

## 手元で動かす

```
python -m venv env
```

- Windows：`env\Scripts\activate`
- Mac：`source env/bin/activate`（Mac は最初の行も `python3 -m venv env`）
- Windows の PowerShell で「スクリプトの実行が無効」と出たら：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` を1回打つか、コマンドプロンプトに切り替えて打ちます。

```
pip install -r requirements.txt
python db_init.py
python app.py
```

ブラウザで `http://localhost:8000` を開きます。

## Render で公開する

1. Render で PostgreSQL（Free）を作ります。Web サービスと同じリージョンにします。
2. 「New → Web Service」で GitHub のリポジトリを選びます。
   - Build Command：`pip install -r requirements.txt`
   - Start Command：`gunicorn app:app`（`python app.py` でも動きますが、公開には gunicorn を使います。gunicorn は Windows では動かないので、手元は `python app.py` です）
   - 環境変数 `DATABASE_URL`：Internal Database URL
   - 環境変数 `PYTHON_VERSION`（入れる時）：`3.14.10` のように最後の数字まで
3. 公開 URL を開き、一覧と投稿が動くことを確かめます。

## 知っておくこと

- Render の無料のデータベースは、作ってから30日で期限が切れます。その後14日のうちに有料にしないと、データごと消えます。無料のデータベースは1つだけです（2026年11月）。
- このアプリにはログインがありません。練習用として公開し、使い終わったら止めるか消してください。
- この requirements.txt の版は、Python 3.12〜3.15 で入ることを確かめています（2026年11月）。
