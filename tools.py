import os
import random
import requests
import discord
from discord.ext import commands
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

# const.py用
import const
GOOGLE_API_KEY                 = const.GOOGLE_API_KEY
CUSTOM_SEARCH_ENGINE_ID        = const.CUSTOM_SEARCH_ENGINE_ID
DISCORD_TOKEN                  = const.DISCORD_TOKEN
GOOGLE_APPLICATION_CREDENTIALS = const.GOOGLE_APPLICATION_CREDENTIALS

# Heroku用
# GOOGLE_API_KEY                 = os.environ['GOOGLE_API_KEY']
# CUSTOM_SEARCH_ENGINE_ID        = os.environ['CUSTOM_SEARCH_ENGINE_ID']
# DISCORD_TOKEN                  = os.environ['DISCORD_TOKEN']
# GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

# ! + 関数名 のメッセージ送信でコマンド実行と定義
bot = commands.Bot(command_prefix="!",help_command=None)

# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('login.')

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    if message.author.bot:
        # メッセージ送信者がBotだった場合は無視する
        return
    elif random.randint(1, 200) == 200:
        # メッセージが飛んでくるたび0.5%の確率でワイトもそう思ってくれる
        await message.channel.send('ワイトもそう思います。')

    # on_messageをオーバーライドするとせっかく定義したコマンドが使えなくなるっぽい
    # 下記はそれを回避するおまじない
    await bot.process_commands(message)

# !helpだけでなく!hでも呼べるようにaliasをはってる
@bot.command(aliases=['h'])
async def help(ctx):
    await ctx.send(
        '```\n'
        '!help:     コマンド一覧を表示します（今表示してるこれ）\n'
        '           省略形として「!h」でも表示できます。\n'
        '\n'
        '!dice:     ダイスを振ります。省略形として「!d」で6面ダイス、また「!1d100」で100面ダイスを振れます。\n'
        '\n'
        '!ygoggr:   遊戯王カードWiki内の検索結果を表示します。\n'
        '           効果テキスト欄を持つページを1件先頭から探し、タイトルと効果テキストを返します。\n'
        '           「!ygoggr ホープ」のように指定してください。省略形として「!y ホープ」でもOKです。\n'
        '           「!y ドラグーン　禁止」のようにスペース区切りで複数キーワードも指定できます。\n'
        '           あとはものによりますが「!y レダメ」のように略称も案外いけます。\n'
        '\n'
        '!passive:  天則、憑依華、遊戯王、モンハンの中からランダムに一つ返します。\n'
        '           省略形として「!p」「!pa」でもOKです。\n'
        '\n'
        '!randlist: スプレッドシートの項目からランダムに一つ返します。\n'
        '           https://docs.google.com/spreadsheets/d/1LZq1Pmqt_PRYTnkKz7ershaG2ILQTMTVFnGEAOsaYDQ/edit'
        '           上記のSheet1、セルA1からA10までが対象です。'
        '           省略形として「!r」「!rl」でもOKです。\n'
        '```'
    )

@bot.command(aliases=['d', '1d6'])
async def dice(ctx):
    await ctx.send(random.randint(1, 6))

@bot.command(aliases=['1d100'])
async def d100(ctx):
    await ctx.send(random.randint(1, 100))

@bot.command(aliases=['y', 'ygo'])
async def ygoggr(ctx, *search_words):
    # 検索そのものは別関数に丸投げ
    results = getYGOSearchResponse(' '.join(search_words))

    # 検索結果から<pre>タグを持つページを1件引っ張ってきて文字列加工
    output = '見つかりませんでした……'
    for result in results:
        url = requests.get(result['link'], verify=False)
        soup = BeautifulSoup(url.content, 'html.parser').find_all('pre')
        if soup != []:
            output = '**'+str(result['title'])+'**\n```\n'+str(soup[0])[5:-6]+'\n```'
            break

    await ctx.send(output)

def getYGOSearchResponse(search_words):
    # 受け取った単語で遊戯王Wiki内を検索しページを上から10件返す
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    response = service.cse().list(
        q=search_words,
        cx=CUSTOM_SEARCH_ENGINE_ID,
        lr='lang_ja',
        num=10,
    ).execute()
    results = response['items'] if 'items' in response else []
    return results

@bot.command(aliases=['p', 'pa'])
async def passive(ctx):
    await ctx.send(random.choice(('天則', '憑依華', '遊戯王', 'モンハン')))

@bot.command(aliases=['r', 'rl'])
async def randlist(ctx):
    # Googleスプレッドシート詠唱開始
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_APPLICATION_CREDENTIALS, scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('bot').sheet1

    #  セルA1からA10の範囲の値を取ってきてリストに突っ込む
    results = wks.range('A1:A10')
    output = []
    for result in results:
        if result.value != '':
            output.append(result.value)

    # リストの中からランダムに一つピック
    await ctx.send(random.choice(output))

# Botの起動とDiscordサーバーへの接続
bot.run(DISCORD_TOKEN)