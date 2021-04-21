# discord-bot

## 環境
python 3.8.5

### 依存パッケージ
- [discord.py](https://github.com/Rapptz/discord.py)
- [google-api-python-client](https://github.com/googleapis/google-api-python-client/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [gspread](https://gspread.readthedocs.io/en/latest/)
- [oauth2client](https://oauth2client.readthedocs.io/en/latest/)

`pip install discord.py google-api-python-client beautifulsoup4 gspread oauth2client`

で全部入ると思うけど問題出るかも。

## その他
Heroku側と連携してて、masterブランチにコミットが上がると向こうで自動デプロイがかかる。

APIトークンとかその辺のヤバいのは別途Herokuの環境変数に入れてあるのでこのままじゃ動かないむん。
