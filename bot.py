import discord
from discord import app_commands
from gtts import gTTS
import asyncio
import os
from dotenv import load_dotenv

# -----------------------------
# 디스코드 봇 기본 설정
# -----------------------------
class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)  # ✅ 명령어 트리 추가
        self.tts_channel_id = None
        self.voice_client = None

    async def on_ready(self):
        guild = discord.Object(id=1416656162996355114)  # ✅ 네 서버 ID
        await self.tree.sync(guild=guild)
        print(f"✅ 로그인 완료: {self.user}")
        print(f"✅ Slash commands synced to: {guild.id}")

    # -----------------------------
    # 메시지가 올 때마다 실행
    # -----------------------------
    async def on_message(self, message):
        if not self.tts_channel_id:  # 설정된 TTS 채널이 없으면 무시
            return
        if message.author.bot:  # 봇 메시지는 무시
            return
        if message.channel.id != self.tts_channel_id:  # 지정된 채널이 아니면 무시
            return
        if not self.voice_client:  # 음성 채널에 없으면 무시
            return

        # 메시지를 음성으로 변환
        tts = gTTS(text=f"{message.author.display_name}의 메시지: {message.content}", lang="ko")
        tts.save("tts.mp3")

        # 재생 중이면 잠깐 대기
        while self.voice_client.is_playing():
            await asyncio.sleep(0.5)

        self.voice_client.play(discord.FFmpegPCMAudio("tts.mp3"))
        while self.voice_client.is_playing():
            await asyncio.sleep(0.5)
        os.remove("tts.mp3")

# -----------------------------
# 클라이언트 생성
# -----------------------------
client = MyClient()

# -----------------------------
# /set_tts_channel 명령어
# -----------------------------
@client.tree.command(name="set_tts_channel", description="TTS를 적용할 채널을 설정합니다.")
@app_commands.describe(channel="TTS를 적용할 텍스트 채널을 선택하세요.")
async def set_tts_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    client.tts_channel_id = channel.id
    await interaction.response.send_message(f"📢 이제부터 {channel.mention}의 메시지를 읽습니다!")

# -----------------------------
# /join 명령어
# -----------------------------
@client.tree.command(name="join", description="현재 음성 채널에 봇을 참가시킵니다.")
async def join(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message("먼저 음성 채널에 들어가세요!")
        return
    channel = interaction.user.voice.channel
    client.voice_client = await channel.connect()
    await interaction.response.send_message(f"🎧 {channel.name}에 연결되었습니다!")

# -----------------------------
# /leave 명령어
# -----------------------------
@client.tree.command(name="leave", description="봇이 음성 채널에서 나갑니다.")
async def leave(interaction: discord.Interaction):
    if client.voice_client:
        await client.voice_client.disconnect()
        client.voice_client = None
        await interaction.response.send_message("👋 음성 채널에서 나갔습니다.")
    else:
        await interaction.response.send_message("현재 음성 채널에 없습니다.")

# -----------------------------
# 봇 실행
# -----------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client.run(TOKEN)