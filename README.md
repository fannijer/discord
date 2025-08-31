# discord

環境構築

```
git clone https://github.com/fannijer/discord.git
# 仮想環境作成
python3 -m venv venv
source venv/bin/activate

# ライブラリインストール
pip install --upgrade pip
pip install discord.py python-dotenv google-generativeai
```

# 環境変数設定

/mcp-discord-bot/.env
を作成して API キーを記載
DISCORD_TOKEN=bot の API キー
GEMINI_API_KEY=gemini の API キー

実行

```
python3 mcp-discord-bot/bot.py
```
