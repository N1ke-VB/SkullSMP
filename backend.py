"""
Backend FastAPI — vorbește cu serverul Minecraft prin RCON.
Expune API-uri pentru site și pentru botul Discord.
"""
import logging
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from mcipc.rcon.je import Client as RconClient
from mcipc.query import Client as QueryClient
from config import (
    MC_HOST, MC_RCON_PORT, MC_RCON_PASSWORD, MC_QUERY_PORT, BACKEND_SECRET
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("backend.log"), logging.StreamHandler()]
)
log = logging.getLogger("backend")

app = FastAPI(title="MC-Discord Backend")


def rcon(cmd: str) -> str:
    """Execută o comandă RCON pe serverul MC."""
    try:
        with RconClient(MC_HOST, MC_RCON_PORT, passwd=MC_RCON_PASSWORD) as c:
            result = c.run(cmd)
            log.info(f"RCON: {cmd} -> {result}")
            return str(result)
    except Exception as e:
        log.error(f"RCON error: {e}")
        raise HTTPException(500, f"RCON error: {e}")


def check_auth(secret: str):
    if secret != BACKEND_SECRET:
        raise HTTPException(401, "Unauthorized")


class CommandBody(BaseModel):
    cmd: str


class AnnounceBody(BaseModel):
    message: str


@app.get("/")
def root():
    return {"service": "mc-discord-backend", "status": "ok"}


@app.get("/server/status")
def server_status():
    """Returnează starea serverului (jucători online etc.)."""
    try:
        with QueryClient(MC_HOST, MC_QUERY_PORT) as q:
            stats = q.stats(full=True)
        return {
            "online": True,
            "players_online": stats.num_players,
            "players_max": stats.max_players,
            "motd": stats.motd,
        }
    except Exception as e:
        log.warning(f"Query failed: {e}")
        return {"online": False, "error": str(e)}
@app.get("/server/players")
def server_players(x_secret: str = Header(...)):
    check_auth(x_secret)
    return {"players": rcon("list")}


@app.post("/server/command")
def server_command(body: CommandBody, x_secret: str = Header(...)):
    check_auth(x_secret)
    return {"result": rcon(body.cmd)}


@app.post("/server/announce")
def server_announce(body: AnnounceBody, x_secret: str = Header(...)):
    check_auth(x_secret)
    safe = body.message.replace('"', "'")
    rcon(f'say {safe}')
    return {"ok": True}


if name == "main":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)