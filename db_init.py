import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 接続先は .env の DATABASE_URL から読む。パスワードを含むので、このファイルには書かない
# （.env は .gitignore に入っているので GitHub に上がらない）。
# .env の例: DATABASE_URL=postgresql://ユーザー:パスワード@ホスト名.singapore-postgres.render.com/DB名?sslmode=require
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL", "")
if not DATABASE_URL:
    raise SystemExit("DATABASE_URL がありません。.env に Render の External Database URL を書いてください。")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
if "render.com" in DATABASE_URL and "sslmode=" not in DATABASE_URL:
    DATABASE_URL += ("&" if "?" in DATABASE_URL else "?") + "sslmode=require"

# エンジンを作成
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# アプリと同じ構造のテーブルを作るSQL
schema_sql = """
CREATE TABLE IF NOT EXISTS recipes (
  id          SERIAL PRIMARY KEY,
  title       VARCHAR(200) NOT NULL,
  minutes     INTEGER NOT NULL CHECK (minutes >= 1),
  description TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

# 初回だけ入れるサンプルデータ
seed_sql = """
INSERT INTO recipes (title, minutes, description)
VALUES
  (:t1, :m1, :d1),
  (:t2, :m2, :d2);
"""

with engine.begin() as conn:
    # テーブル作成（IF NOT EXISTSなので2回目以降も安全）
    conn.execute(text(schema_sql))

    # もうデータが入ってるなら追加しない
    count = conn.execute(text("SELECT COUNT(*) FROM recipes;")).scalar_one()
    if count == 0:
        conn.execute(
            text(seed_sql),
            dict(
                t1="卵焼き",
                m1=10,
                d1="卵・砂糖・塩を混ぜて焼くシンプルな定番。",
                t2="味噌汁",
                m2=15,
                d2="出汁を取り、味噌を溶き、豆腐とわかめを加える。",
            ),
        )

print("OK: テーブル作成と初期データ投入まで完了しました。")