# flask-tutorial

## やりたいこと
- https://qiita.com/kiyokiyo_kzsby/items/0184973e9de0ea9011ed

## やったこと
### 環境構築
- ターミナルで python -v をしたところ python の バージョンが3.6 だった
- 最新が3.9.7 らしいので上げたい
    - https://www.python.org/downloads/
- python をアップデートするには、pyenv が必要。すでに入っていたが、pyenv のインストールリストにpython 3.6 までしか入っておらず
- pyenv も古いことを知った。更に pyenv を install するための homebrew が古いこともわかった
- この記事を参考に、下記をターミナルから実行して、homebrew を最新化することにした
    - https://apple.stackexchange.com/questions/381970/error-usr-local-must-be-writable-update-homebrew
    - ‘/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"’
- brew -v すると、最新になっていた
    - Homebrew 3.2.12
    - Homebrew/homebrew-core (git revision 63d57801c1; last commit 2021-09-18)
- そこで、brew install pyenv した
    - 途中、’Your Xcode (9.3.1) is outdated’ と出てたが一旦無視
    - link エラーが出た（多分、これと同じ。https://wtnvenga.hatenablog.com/entry/2017/11/15/1254
****
==> ./configure --prefix=/usr/local/Cellar/autoconf/2.71 --with-lispdir=/usr/local/Cellar/autoconf/2.71/share/emacs/site-lisp/autoconf
==> make install
Error: The `brew link` step did not complete successfully
The formula built, but is not symlinked into /usr/local
Could not symlink bin/autoconf
Target /usr/local/bin/autoconf
is a symlink belonging to autoconf. You can unlink it:
  brew unlink autoconf

To force the link and overwrite all conflicting files:
  brew link --overwrite autoconf

To list all files that would be deleted:
  brew link --overwrite --dry-run autoconf
****
    - /usr/local/bin/autoconf がsymlinkとして機能していなさそうなので、brew unlink autoconf して、brew link --overwrite autoconf してlinkできるようにした
        - autoconf や pkg-config はこのあたりの役割をしているのか。-> https://atmarkit.itmedia.co.jp/ait/articles/1107/01/news139.html
    - 同様に、bin/pkg-config 、でも起きたので対応した
    - pyenv 2.0.6 インストールできた！！
- pyenv install —list すると、3.9.7 が入っている！
- python install 3.9.7 して、python -V すると、最新になっていることを確認できた！はずだが・・・
****
ntkmt-no-MacBook-Air:~ tsukamotonao$ pyenv install 3.9.7
python-build: use openssl@1.1 from homebrew
python-build: use readline from homebrew
Downloading Python-3.9.7.tar.xz...
-> https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tar.xz
Installing Python-3.9.7...
python-build: use readline from homebrew
Installed Python-3.9.7 to /Users/tsukamotonao/.pyenv/versions/3.9.7

ntkmt-no-MacBook-Air:~ tsukamotonao$ python -V
Python 3.6.1 :: Anaconda 4.4.0 (x86_64)
****
- なぬ？まだ3.6.1 ・・・
- 調べると、python のバージョンが切り替わっていないことがわかった
- ~/.bash_profile に export PATH="$HOME/.pyenv/shims:$PATH" を追記して、python -V したところ・・・、
ntkmt-no-MacBook-Air:~ tsukamotonao$ python -V
Python 3.9.7
- あがったーーーーー！

### FlaskApp
- Flask のおまじないについて
****
#Flaskオブジェクトの生成
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
****
- Flaskクラスのインスタンスを生成しています。引数の__name__には現在実行中のモジュールの完全修飾名が格納されます。ただし、実行時のトップレベルのモジュールの場合は"__main__"という文字列が格納されます。ここではhello.pyから実行するため、__name__には__main__が入ることになります。なぜここで__name__が必要かというと、後々出てくるtemplates(htmlを格納)やstatic(CSSやJSを格納)の位置をFlaskに知らせるためです。
    - https://blog.pyq.jp/entry/Python_kaiketsu_180207 -> python XX.py のときには、__name__ -> __main__ になるがimport YY では __name__ -> YY となるので、YYのときは実行されてほしくないので、おまじないが必要。
- requestモジュールとは
    - Flaskアプリケーションがリクエストを処理するとき、WSGIサーバから受け取った環境（訳注: WSGIは、WSGIサーバからWSGIアプリケーションに環境情報をdict互換のオブジェクトで渡す仕様になっています）に基づいてRequestオブジェクトを作成します。
- request.argsでよく使うのはget
    - args とはなにか？ 
    - -> https://note.nkmk.me/python-args-kwargs-usage/
    - -> flask.request.argsはURLのパラメータ（query stringと呼ばれたりします）を格納します
- request モジュールで受け取ったクエリパラメータ(string)を、htmlでif分岐させて表示
****
	{% if name %}
        <h1>{{name}}App - ntkmt</h1>
        {% else %}
        <h1>App - ntkmt</h1>
        {% endif %}
****
- app.py で定義した配列を、htmlでforループさせて表示
****	
	<!-- for文 -->
       {% for last_name in okyo %}
        <p>{{last_name}}</p>
        {% endfor %}
****
- requst.form[“name”] を requst.form(“name”) と書いていてinternal errorが出た
    - request.agrsやrequest.formは配列だということを認識しておかなければならない
    - https://www.fixes.pub/program/422193.html -> HTML投稿フォーム、またはJSONエンコードされていないJavaScriptリクエストから、ボディ内のキー/値のペア
- sqlalchemy というモデルに定義した内容についてデータベースに格納できるように変換するためのORマッパーを利用する
    - https://www.sqlalchemy.org/ -> SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- エンジンの記述
    - https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/patterns/sqlalchemy.html
- models.py に記載する内容
    - 必要なライブラリをインポート
****
from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime
****
- database.py ：データベースとの直接的な接続の情報
- from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
    - この記事のチュートリアルは、公式とは全然違うやり方をしている？ https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/database.html
    - session を作成して、データベースへアクセスできるようにする
        - 参考）SQLiteデータベース（および殆どのPythonの他のデータベースライブラリ）を使って作業するとき最初にすることは、データベースへの接続（connection）の作成です。どのような問合せ（queries）や操作（operations）も、connectionを使用しながら実施され、作業が終了した後はconnectionが閉じられ（close）ます。
    - scoped_session について
        - セッション生成方法の種類のうちの1つ
        - https://qiita.com/tosizo/items/86d3c60a4bb70eb1656e　-> scoped_sessionという内部にSession管理レジストリを内包したクラスによる生成方法です。
        - 上記コードのUser.query.～のように、テーブルクラスを起点としてコード(select文)が書けるようになる
    - python には対話環境（インタプリタ？）がある（ruby  とかもあるか・・
        - python インタプリタで、from models.database import init_db をしたら、ModuleNotFoundError: No module named 'models' と出た
        - models.database が読み込めなかったのは、models ディレクトリがapp配下にあったため。app と並列のディレクトリに置く必要がある
    - __repr__ メソッド
        - オブジェクトを表す公式な文字列を生成する
- import models.model from OnegaiContent と記述していて、module not found error がおきた
    - このようにすることで、コードの再利用（一度書いたプログラムの別のプログラムからの利用）が可能になる。このときに、プログラムを保存する先がモジュールだと考えればよい。
    - https://qiita.com/hira03/items/ab34459c4dca7d8f697e　-> from モジュール名 import 定義1,定義2,… というように書くと、モジュールを使用するときは定義名だけで実行することができるようになります。
- フォームのacation属性で「/add」と指定したので、@app.route("/add",methods=["post"])でルーティングを追加します。
- https://qiita.com/tomo0/items/a762b1bc0f192a55eae8 -> sqlalchemy での基本的なクエリが確認できる
- update するとき、db_session.add ではなく、db_session.update という存在しないメソッドを書いてエラーでていたので、下記にならい修正した
    - https://study-flask.readthedocs.io/ja/latest/flask_sqlalchemy.html 
- ただのhtml のはなし
    - そのままチェックボックスを追加しようとするとフォームが入れ子構造になってうまく表示されなくなってしまうため、formタグを外に出して、formタグのid属性と、inputタグのform属性で紐付けるスタイルを採用します。
- request.form => ImmutableMultiDict([('delete', ‘2’),('delete', ‘3’)])
    - request.form.getlist(“delete”) => [‘2’,’3’]で返ってくる
- production を見ていたので、development へ変更するよう bash で設定した
    - https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/config.html -> export FLASK_ENV=developmen
- なぜ、__tablename__ = なのか？
    - https://www.nblog09.com/w/2019/01/11/python_tokushu_method/ -> pythonには、_(アンダースコア)が2つで始まり2つで終わる特殊メソッドと呼ばれるメソッドがある。
****
例えば、
a + b
とするとき、内部で
a.__add__(b)
というようにaインスタンスの__add__()メソッドを呼び出す。
****
- init_db() は、初期化するが、すでに存在するtableに対しては適用されない
- セッション管理するための、SECRET_KEY と SALT を記述する
    - 下記は例
****
ちなみにFlaskのドキュメントには、以下のように生成すると良いと書かれています。:
>>> import os
>>> os.urandom(24)
'\xfd{H\flash: xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8
****
os.urandom(size)
    - https://docs.python.org/ja/3/library/os.html -> 暗号に関する用途に適した size バイトからなるランダムな文字列を返します。この関数は OS 固有の乱数発生源からランダムなバイト列を生成して返します。この関数の返すデータは暗号を用いたアプリケーションで十分利用できる程度に予測不能ですが、実際のクオリティは OS の実装によって異なります。
    - https://pg-chain.com/python-hash-hashlib#toc4　-> PythonのSHA256ハッシュ関数は「hashlib.sha256」を使います。「hashlib.sha256」の引数に文字列を指定します。その際、「encode」する必要があります。そして「hexdigest」で16進形式文字列にします。
    - 
- ソルト付きハッシュについて
    - 実はハッシュ化だけでは不十分である。というのもよくあるパスワードは同じハッシュ値になってしまうからである。攻撃者はあらかじめよくあるパスワードのハッシュ値を計算しておきデータベース内にいっちするものがないか探せば良い。また、同じパスワードを複数人が利用している場合一人のパスワードが発覚してしまえば残りの人のパスワードもわかってしまう。そのために同じパスワードを使っていても違うハッシュ値になり、なおかつ、パスワードが正しいか検証できる方法が必要である。その方法の一つがソルト付きハッシュである。ソルト付きハッシュは平文のパスワードに(一般に)ランダムな文字列を加えて生成する。
- session.pop()は、session.pop('username', None) という形で使うことが多そう

