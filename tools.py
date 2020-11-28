import discord
import random
from googleapiclient.discovery import build
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os

GOOGLE_API_KEY          = os.environ['GOOGLE_API_KEY']
CUSTOM_SEARCH_ENGINE_ID = os.environ['CUSTOM_SEARCH_ENGINE_ID']
DISCORD_TOKEN           = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix="!",help_command=None) # ! + 関数名 のメッセージ送信でコマンド実行と定義

# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('login.')

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    elif message.content == '!dice' or message.content == '!d' or message.content == '!1d6':
        await message.channel.send(random.randint(1, 6))
    elif message.content == '!2d6':
        await message.channel.send(str(random.randint(1, 6)) + ', ' + str(random.randint(1, 6)))
    elif message.content == '!3d6':
        await message.channel.send(str(random.randint(1, 6)) + ', ' + str(random.randint(1, 6)) + ', ' + str(random.randint(1, 6)))
    elif message.content == '!d10' or message.content == '!1d10':
        await message.channel.send(random.randint(1, 10))
    elif message.content == '!2d10':
        await message.channel.send(str(random.randint(1, 10)) + ', ' + str(random.randint(1, 10)))
    elif message.content == '!3d10':
        await message.channel.send(str(random.randint(1, 100)) + ', ' + str(random.randint(1, 100)) + ', ' + str(random.randint(1, 100)))
    elif message.content == '!d100' or message.content == '!1d100':
        await message.channel.send(random.randint(1, 100))
    elif message.content == '!2d100':
        await message.channel.send(str(random.randint(1, 100)) + ', ' + str(random.randint(1, 100)))
    elif message.content == '!3d100':
        await message.channel.send(str(random.randint(1, 100)) + ', ' + str(random.randint(1, 100)) + ', ' + str(random.randint(1, 100)))
    elif random.randint(1, 200) == 200:
        await message.channel.send('ワイトもそう思います。')

    # TODO: ここのダイス処理バカクソきたねえからそのうちどうにかしたいわね

    await bot.process_commands(message)

@bot.command(aliases=['h']) # !helpだけでなく!hでも呼べるようにaliasをはってる
async def help(ctx):
    await ctx.send((
        '```\n'
        '!help:    コマンド一覧を表示します（今表示してるこれ）\n'
        '          省略形として「!h」でも表示できます。\n'
        '\n'
        '!dice:    ダイスを振ります。6面、10面、100面ダイスがあり、「!3d6」のように指定することで最大3つまで同時に投げることができます。\n'
        '          省略形として「!d」で6面ダイスを振れます。\n'
        '\n'
        '!ygoggr:  遊戯王カードWiki内を検索し、効果テキスト欄を持つページを1件先頭から探しタイトルと効果テキストを返します。\n'
        '          「!ygoggr ホープ」のように指定してください。省略形として「!y ホープ」でも指定できます。\n'
        '          「!y ドラグーン　禁止」のようにスペース区切りで複数キーワードも指定できます。\n'
        '\n'
        '!passive: 天則、スマブラ、遊戯王の中からランダムに一つ返します。\n'
        '          省略形として「!p」「!pa」でもOKです。\n'
        '```'
    ))

@bot.command(aliases=['y', 'ygo']) # aliasは複数はれる
async def ygoggr(ctx, *search_words):
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
        cx=CUSTOM_SEARCH_ENGINE_ID
        lr='lang_ja',
        num=10,
    ).execute()
    return response['items']

@bot.command(aliases=['p', 'pa'])
async def passive(ctx):
    await ctx.send(random.choice(('天則', 'スマブラ', '遊戯王')))

# Botの起動とDiscordサーバーへの接続
bot.run(DISCORD_TOKEN)