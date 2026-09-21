import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("MTU1MTYwNzY5Nzk2OTkwOTc3MA.GFsvkb.1kQ_NIB_JSNe61fdrfmiNK0u_6xZ5VtuGBQAKg")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
DISCORD_CHAT_CHANNEL_ID = int(os.getenv("1551328177006059601", "0"))
DISCORD_ANNOUNCE_CHANNEL_ID = int(os.getenv("1551328177006059601", "0"))
DISCORD_TICKET_CHANNEL_ID = int(os.getenv("1551328177006059601", "0"))
DISCORD_ADMIN_ROLE = os.getenv("DISCORD_ADMIN_ROLE", "Admin")

MC_HOST = os.getenv("MC_HOST")
MC_RCON_PORT = int(os.getenv("MC_RCON_PORT", "25575"))
MC_RCON_PASSWORD = os.getenv("MC_RCON_PASSWORD")
MC_QUERY_PORT = int(os.getenv("MC_QUERY_PORT", "25565"))

BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
BACKEND_SECRET = os.getenv("BACKEND_SECRET", "changeme")
