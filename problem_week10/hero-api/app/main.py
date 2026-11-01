from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.database import engine

from app.routers import heroes, teams, missions

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title="Heroes API",
    version="1.0.0",
    openapi_tags=[
        {"name": "heroes", "description": "Create, read, update and delete heroes."},
        {"name": "teams", "description": "Teams and the heroes that belong to them."}
    ],
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(heroes.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")
app.include_router(missions.router, prefix="/api/v1")

# The assign_mission / list_hero_missions from Week 9 can just sit here, or in heroes
from fastapi import HTTPException
from app.database import SessionDep
from app.models import Hero, Mission, MissionPublic

@app.post("/api/v1/heroes/{hero_id}/missions/{mission_id}", status_code=204, tags=["missions"])
def assign_mission(hero_id: int, mission_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    mission = session.get(Mission, mission_id)
    if not hero or not mission:
        raise HTTPException(status_code=404, detail="Hero or mission not found")
    if mission not in hero.missions:
        hero.missions.append(mission)
        session.add(hero)
        session.commit()

@app.get("/api/v1/heroes/{hero_id}/missions", response_model=list[MissionPublic], tags=["missions"])
def list_hero_missions(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero.missions
