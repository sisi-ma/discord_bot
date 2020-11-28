# discord-bot

## 環境
python 3.8.5

### 依存パッケージ
- [discord.py](https://github.com/Rapptz/discord.py)
- [google-api-python-client](https://github.com/googleapis/google-api-python-client/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

`pip install discord.py google-api-python-client beautifulsoup4`

で全部入ると思うけど問題出るかも。

## その他
Heroku側と連携してて、mainブランチにコミットが上がると向こうで自動デプロイがかかる。

APIトークンとかその辺のヤバいのは別途Herokuの環境変数に入れてあるのでこのままじゃ動かないお。

