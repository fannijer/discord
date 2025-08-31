import discord
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .envからAPIキー取得
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# キャラ設定（関西弁おっさん）
SYSTEM_PROMPT = """
語尾はクロちゃんみたいな話し方にして「～しん、～だしんよ～」など
"""

# カロリーが高かったらキレ散らかしてええで！
# ユーザーが送ってきた食事メニューについて、
# だいたいの摂取カロリー、各栄養素をざっくり計算して、
# 関西弁でツッコミや励ましを交えて答えるんやで！

# 【例】
# ユーザー: 唐揚げ定食
# 返答: おっ、唐揚げ定食かいな。だいたい800kcal前後やな。美味いけど脂っこいで〜。夜に食うならサラダも一緒にや！

# ユーザー: おにぎり2個と味噌汁
# 返答: 軽めでええやんか。おにぎり2個でだいたい400kcal、味噌汁は50kcalくらいやな。バランスはまあまあやで！

# あくまでざっくりやからな！専門家ちゃうけど、気持ち的には管理栄養士のつもりでやってまっせ！

# Gemini API設定
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")  # 速さ重視なら flash / 精度なら pro

# Discord Bot設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} が起動しました！")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # チャンネル名が bot じゃなかったら無視
    if message.channel.name != "bot":
        return

    user_prompt = message.content.strip()
    if not user_prompt:
        return

    try:
        # Geminiは systemロール非対応なので、プロンプトに組み込む
        full_prompt = SYSTEM_PROMPT + "\n\nユーザー: " + user_prompt

        response = model.generate_content(full_prompt)
        reply = response.text.strip()
        await message.channel.send(reply)

    except Exception as e:
        await message.channel.send(f"エラーやで: {e}")

# Botを起動
client.run(DISCORD_TOKEN)
