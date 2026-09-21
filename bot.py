"""
Bot Discord — comenzi slash, tickete, notificări.
Comunică cu backend-ul FastAPI pentru a controla serverul MC.
"""
import logging
import discord
from discord import app_commands
from discord.ext import commands
import requests
from config import (
    DISCORD_TOKEN, DISCORD_GUILD_ID, DISCORD_CHAT_CHANNEL_ID,
    DISCORD_ANNOUNCE_CHANNEL_ID, DISCORD_TICKET_CHANNEL_ID,
    DISCORD_ADMIN_ROLE, BACKEND_SECRET
)

BACKEND = "http://127.0.0.1:8000"
HEADERS = {"x-secret": BACKEND_SECRET}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
log = logging.getLogger("bot")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
GUILD = discord.Object(id=DISCORD_GUILD_ID)


def is_admin(interaction: discord.Interaction) -> bool:
    return any(r.name == DISCORD_ADMIN_ROLE for r in interaction.user.roles)


# ---------- COMENZI SLASH ----------

@bot.tree.command(name="status", description="Starea serverului Minecraft")
async def status(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        r = requests.get(f"{BACKEND}/server/status", timeout=5)
        data = r.json()
        if data.get("online"):
            await interaction.followup.send(
                f"✅ Server **online**\n"
                f"👥 Jucători: **{data['players_online']}/{data['players_max']}**\n"
                f"📝 MOTD: {data.get('motd', '-')}"
            )
        else:
            await interaction.followup.send(f"❌ Server offline: {data.get('error')}")
    except Exception as e:
        await interaction.followup.send(f"❌ Backend indisponibil: {e}")


@bot.tree.command(name="players", description="Lista jucătorilor online")
async def players(interaction: discord.Interaction):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ Doar adminii.", ephemeral=True)
        return
    await interaction.response.defer()
    r = requests.get(f"{BACKEND}/server/players", headers=HEADERS, timeout=5)
    await interaction.followup.send(f"```{r.json().get('players', '?')}```")


@bot.tree.command(name="say", description="Trimite un mesaj global pe serverul MC")
@app_commands.describe(mesaj="Mesajul de trimis")
async def say(interaction: discord.Interaction, mesaj: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ Doar adminii.", ephemeral=True)
        return
    await interaction.response.defer()
    r = requests.post(f"{BACKEND}/server/announce",
                      json={"message": mesaj}, headers=HEADERS, timeout=5)
    if r.status_code == 200:
        await interaction.followup.send(f"✅ Trimis: `{mesaj}`")
    else:
        await interaction.followup.send(f"❌ Eroare: {r.text}")


@bot.tree.command(name="kick", description="Dai kick unui jucător")
@app_commands.describe(jucator="Numele jucătorului", motiv="Motivul")
async def kick(interaction: discord.Interaction, jucator: str, motiv: str = "Fără motiv"):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ Doar adminii.", ephemeral=True)
        return
    await interaction.response.defer()
    cmd = f"kick {jucator} {motiv}"
    r = requests.post(f"{BACKEND}/server/command",
                      json={"cmd": cmd}, headers=HEADERS, timeout=5)
    await interaction.followup.send(f"✅ `{cmd}` → {r.json().get('result', '?')}")


@bot.tree.command(name="ban", description="Banezi un jucător")
@app_commands.describe(jucator="Numele jucătorului", motiv="Motivul")
async def ban(interaction: discord.Interaction, jucator: str, motiv: str = "Fără motiv"):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ Doar adminii.", ephemeral=True)
... (104 rânduri rămase)
