from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# 下記は、下記でもOK
# ref）https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/patterns/sqlalchemy.html

# engine = create_engine('sqlite:///models/onegai.db', convert_unicode=True)


# 本ファイルと同じパスにonegai.dbを指定
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'onegai.db')
# SQLiteを利用して1.で定義した絶対パスにDBを構築する
engine = create_engine('sqlite:///' + databese_file, convert_unicode=True)


# DB接続用インスタンスを生成
# secoped_session を利用するSession 作成方法
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine))
# Baseインスタンスを作成する
Base = declarative_base()
# セッションを利用してDB情報を流し込む
Base.query = db_session.query_property()

# DBを初期化のための関数を定義した
def init_db():
    import models.models
    Base.metadata.create_all(bind=engine)