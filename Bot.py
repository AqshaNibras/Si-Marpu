import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from dictionary import *

import datetime as dt
from datetime import datetime as dtime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=".", 
                      intents=intents, 
                      case_insensitive=True, 
                      help_command=None)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(".help"))
    print("Bot berhasil aktif!")
    await client.tree.sync()

# ===========================
# @client.event()
# ===========================

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    content = msg.content.lower().strip()
    if content in (("oi marpu", "oi")):
        await msg.channel.send("Oi")

    if content in (sapa_waktu):
        ucapan = sapa_waktu[content]
        await msg.channel.send(f"{ucapan} juga {msg.author.mention}")

    if content in (sapa_kata):
        ucapan = sapa_kata[content]
        await msg.channel.send(f"{ucapan} juga {msg.author.mention}")

    await client.process_commands(msg)

# ===========================
# @client.tree.command()
# ===========================

@client.tree.command(name="say", description="Bikin si marpu ngomong!")
async def say(interaction: discord.Interaction, say: str):
    await interaction.response.send_message(say)

# ===========================
# @client.command()
# ===========================

# help
@client.command(name="help")
async def custom_help(ctx):
    embed = discord.Embed(
        title="Command List",
        color= discord.Color.from_rgb(10, 10, 10)
    )
    embed.add_field(
        name="🎉 Fun",
        value="say, hari, harilahir, tanggal, jam",
        inline=False
    )
    embed.add_field(
        name="ℹ️ Info",
        value="help",
        inline=False
    )
    embed.add_field(
        name="／ Slash",
        value="/say",
        inline=False
    )
    await ctx.send(embed=embed)

# fun
@client.command()
async def say(ctx, *, message: str=None):
    if message is None:
        await ctx.send("**Error:**   (pastikan input teks)\n" \
        "Contoh ->   **.say aku keren**")
        return
    await ctx.send(message)

# datetime
@client.command()
async def tanggal(ctx):
    tanggal_today = dt.date.today()
    await ctx.send(f"sekarang tanggal **{tanggal_today}**")

@client.command()
async def hari(ctx):
    hari_en = dtime.today().strftime("%A")

    hari_id = hari_dict.get(hari_en)
    await ctx.send(f"sekarang hari **{hari_id}**")

@client.command()
async def jam(ctx):
    jam = dtime.now()
    jam = dtime.isoformat(jam)
    await ctx.send(f"Saat ini pukul **{jam[11:-7]}** WIB")

@client.command()
async def harilahir(ctx):
    try:
        input_tanggal = ctx.message.content[10:]
        tahun_lahir, bulan_lahir, hari_lahir = map(int, input_tanggal.split("-"))
        hari = dt.date(tahun_lahir, bulan_lahir, hari_lahir)

        hari_en = hari.strftime("%A")
        hari_id = hari_dict.get(hari_en)

        await ctx.send(f"Hari lahir kamu adalah **Hari {hari_id}**")
    
    except:
        await ctx.send("**Error:**   (pastikan input **TAHUN-BULAN-HARI**)\n" \
        "Contoh ->   **.harilahir 1945-8-17**")

client.run(TOKEN)