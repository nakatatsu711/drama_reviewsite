## 概要
Flaskで作るドラマレビューサイトです。

<br>

ドラマのレビューを閲覧、投稿できます。

トップページには、おすすめのドラマを5個ランダムに表示します。また、ドラマレビューランキングと視聴率ランキングも表示します。

登録されていないユーザーは閲覧のみできます。

新規でユーザーを登録できます。  
登録したユーザーでログインすると、レビューの閲覧と投稿ができます。

管理者はこれらに加えて、新しいドラマの追加、編集を行うことができます。



## システム環境
以下で動作確認済みです。  
OS：macOS 11.2.2  
Python：3.6.9



## 実行方法
今回はPipenvを使用して開発を行います。  
まずはPipenvをインストールします。
```
$ pip install pipenv
```


### Pipenvでの開発環境構築
以下の2通りの方法がありますので、どちらかで構築してください。

#### 個別にインストール
```
$ cd drama_reviewsite
$ pipenv --python 3.6.9
$ pipenv install Flask
$ pipenv install Flask-SQLAlchemy
$ pipenv install Flask-Script
```

#### Pipfileを使ったインストール
```
$ cd drama_reviewsite
$ pipenv install
```

<br>

インストールが終わったら、以下のコマンドで仮想環境に入ります。
```
$ pipenv shell
```

ちなみに抜けるのは、以下のコマンドです。このタイミングではしなくて大丈夫です。
```
$ exit
```

また、仮想環境のパスは以下で確認できますので、必要なら確認してみてください。
```
$ pipenv --venv
```


### モデルをデータベースへ反映させる
モデルで定義した内容をデータベースに反映させます。  
反映作業はモデルを定義した後に1度だけで大丈夫です。
```
$ python manage.py init_db
```

実行後、`flask_drama`以下に`flask_drama.db`というファイルが作成されます。


### サイトのロゴを決める
ヘッダーにあるサイトのロゴは以下のサイトで作成しました。  
http://ja.flamingtext.com

ロゴは`static`ディレクトリ内に`logo.png`というファイル名で追加してください。  
GitHubには事前にサンプルのロゴをアップロードしてあります。


### 実行
コマンドラインで実行します。  
以下を実行して、`http://127.0.0.1:5000/`にアクセスします。
```
$ python server.py
```


### 管理者を登録する
「新規登録」から管理者を登録します。

今回は管理者のユーザー名を「nakatatsu」と`views.py`で決めています。  
パスワードはなんでも大丈夫です。

管理者以外のユーザーは自由に登録してもらって大丈夫です。


### ドラマを追加する
「管理者ページ」から新しいドラマを追加します。

詳細ページにサムネイルを設定したい場合は、`static`ディレクトリ内に追加します。  
その際、ドラマのタイトルと同じファイル名を指定してください。  
GitHubには事前にサンプルのサムネイルをアップロードしてあります。


### レビューを投稿する
ドラマの詳細ページからドラマのレビューを投稿します。

レビューは以下のサイトを参考に追加しました。  
https://www.ch-review.net/



## ページ例
トップページ
![drama-reviewsite-1](https://user-images.githubusercontent.com/62325937/128609940-a7cbb2cf-ccbf-4c29-b098-efeafe82c611.jpg)

一覧ページ
![drama-reviewsite-2](https://user-images.githubusercontent.com/62325937/128609944-e0effb8e-b7c4-445d-ab5c-949e2907fbcf.jpg)

詳細ページ
![drama-reviewsite-3](https://user-images.githubusercontent.com/62325937/128609947-580ef0f9-f60a-44f7-add1-3980d9250560.jpg)
