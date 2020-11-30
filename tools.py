import os
import random
import requests
import discord
from discord.ext import commands
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

# const.py用
# import const
# GOOGLE_API_KEY          = const.GOOGLE_API_KEY
# CUSTOM_SEARCH_ENGINE_ID = const.CUSTOM_SEARCH_ENGINE_ID
# DISCORD_TOKEN           = const.DISCORD_TOKEN

# Heroku用
GOOGLE_API_KEY          = os.environ['GOOGLE_API_KEY']
CUSTOM_SEARCH_ENGINE_ID = os.environ['CUSTOM_SEARCH_ENGINE_ID']
DISCORD_TOKEN           = os.environ['DISCORD_TOKEN']

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
        '!help:    コマンド一覧を表示します（今表示してるこれ）\n'
        '          省略形として「!h」でも表示できます。\n'
        '\n'
        '!dice:    ダイスを振ります。省略形として「!d」で6面ダイス、また「!1d100」で100面ダイスを振れます。\n'
        '\n'
        '!ygoggr:  遊戯王カードWiki内の検索結果を表示します。\n'
        '          効果テキスト欄を持つページを1件先頭から探し、タイトルと効果テキストを返します。\n'
        '          「!ygoggr ホープ」のように指定してください。省略形として「!y ホープ」でもOKです。\n'
        '          「!y ドラグーン　禁止」のようにスペース区切りで複数キーワードも指定できます。\n'
        '          あとはものによりますが「!y レダメ」のように略称も案外いけます。\n'
        '\n'
        '!passive: 天則、スマブラ、遊戯王の中からランダムに一つ返します。\n'
        '          省略形として「!p」「!pa」でもOKです。\n'
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
    for result in results:
        url = requests.get(result['link'])
        soup = BeautifulSoup(url.content, 'html.parser').find_all('pre')
        if soup != []:
            output = '**'+str(result['title'])+'**\n```\n'+str(soup[0])[5:-6]+'\n```'
            break

    print(output)
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
    return response['items']

@bot.command(aliases=['p', 'pa'])
async def passive(ctx):
    await ctx.send(random.choice(('天則', 'スマブラ', '遊戯王')))

# Botの起動とDiscordサーバーへの接続
bot.run(DISCORD_TOKEN)