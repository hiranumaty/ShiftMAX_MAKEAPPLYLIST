[Pythonパッケージについて]
tkinter(pythonのインストーラーでインストールできる)
tkcalendar
selenium
python-dotenv
openpyxl

[ChromeDriverについて]
自信のChromeのversionを確認して、
https://chromedriver.chromium.org/downloads を開き同じversionのドライバーをインストールしてください

[ChromeDriverの指定について]
setting.envのDRIVEURLに[ChromeDriverについて]でダウンロードしたドライバーの
絶対パスを記入してください

[使用方法]MakeApplyList
1 IDとPASSに申請情報を取得したい社員のIDとパスワードを入力します
2 申請一覧ボタンを押下するとChromeが立ち上がり自動ログインの後申請一覧の情報を取得していきます
3 申請名を選択すると休暇申請またはシフト勤務申請に絞って抽出します
4 日付の欄を入力して検索するとその期日移行の対象日を含む申請データを絞り込みます
 (2021/7/1-2021/7/31と選択した場合 2021/7/30-2021/8/2の休暇申請が取得できる)
5 抽出の終了後OutPutフォルダーにAPPLYLIST_社員番号_本日の日付."xlsx"というファイルが作成される
  (現在テンプレート等を用意していないため新規ファイルを作成し直書きされる)
  
[使用方法]MakeMultiApplyList
1 取得対象の社員一覧(xlsx)のテキストボックスをクリックし
 取得したい社員の一覧のexcelを選択してください
2 申請一覧ボタンを押下するとChromeが立ち上がり自動ログインの後申請一覧の情報を取得していきます
3 申請名を選択すると休暇申請またはシフト勤務申請に絞って抽出します
4 日付の欄を入力して検索するとその期日移行の対象日を含む申請データを絞り込みます
 (2021/7/1-2021/7/31と選択した場合 2021/7/30-2021/8/2の休暇申請が取得できる)
5 抽出の終了後OutPutフォルダーにAPPLYLIST_本日の日付."xlsx"というファイルが作成され
 シートごとに社員の申請データが出力されます。
(現在テンプレート等を用意していないため新規ファイルを作成し直書きされる)