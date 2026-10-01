from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionDep
from app.models import (
    Hero, HeroCreate, HeroPublic, HeroUpdate,
    Team, TeamCreate, TeamPublic,
    Mission, MissionCreate, MissionPublic
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # We use Alembic now, so we do not call create_all here
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/heroes", response_model=HeroPublic, status_code=201)
def create_hero(hero_in: HeroCreate, session: SessionDep):
    hero = Hero.model_validate(hero_in)
    if hero.team_id is not None:
        team = session.get(Team, hero.team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes", response_model=list[HeroPublic])
def list_heroes(
    session: SessionDep, 
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    min_age: int | None = None,
    team_id: int | None = None,
    name: str | None = None
):
    query = select(Hero)
    if min_age is not None:
        query = query.where(Hero.age >= min_age)
    if team_id is not None:
        query = query.where(Hero.team_id == team_id)
    if name is not None:
        query = query.where(Hero.name.ilike(f"%{name}%"))
        
    query = query.order_by(Hero.id).offset(offset).limit(limit)
    return session.exec(query).all()

@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero_in: HeroUpdate, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
        
    if hero_in.team_id is not None:
        team = session.get(Team, hero_in.team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
    update_data = hero_in.model_dump(exclude_unset=True)
    hero.sqlmodel_update(update_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.delete("/heroes/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()

@app.post("/teams", response_model=TeamPublic, status_code=201)
def create_team(team_in: TeamCreate, session: SessionDep):
    team = Team.model_validate(team_in)
    try:
        session.add(team)
        session.commit()
        session.refresh(team)
        return team
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Team name already exists")

@app.get("/teams", response_model=list[TeamPublic])
def list_teams(session: SessionDep):
    return session.exec(select(Team)).all()

@app.get("/teams/{team_id}/heroes", response_model=list[HeroPublic])
def read_team_heroes(team_id: int, session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team.heroes

@app.post("/missions", response_model=MissionPublic, status_code=201)
def create_mission(mission_in: MissionCreate, session: SessionDep):
    mission = Mission.model_validate(mission_in)
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission

@app.post("/heroes/{hero_id}/missions/{mission_id}", status_code=204)
def assign_mission(hero_id: int, mission_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    mission = session.get(Mission, mission_id)
    if not hero or not mission:
        raise HTTPException(status_code=404, detail="Hero or Mission not found")
        
    if mission not in hero.missions:
        hero.missions.append(mission)
        session.add(hero)
        session.commit()

@app.get("/heroes/{hero_id}/missions", response_model=list[MissionPublic])
def read_hero_missions(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero.missions


@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hero API Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }
            h1 { color: #2c3e50; }
            .container { max-width: 900px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #3498db; color: white; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .btn { display: inline-block; padding: 10px 15px; margin-top: 20px; background-color: #2ecc71; color: white; border-radius: 5px; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦸‍♂️ Hero API Dashboard</h1>
            <p>Welcome to the Hero API! This is a simple dashboard to show that the system is working.</p>
            <a href="/docs" class="btn">View Interactive API Docs (Swagger UI)</a>
            
            <h2>Latest Heroes</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Team ID</th>
                    </tr>
                </thead>
                <tbody id="heroes-table">
                    <tr><td colspan="4">Loading heroes...</td></tr>
                </tbody>
            </table>
        </div>

        <script>
            fetch('/heroes?limit=15')
                .then(response => response.json())
                .then(data => {
                    const table = document.getElementById('heroes-table');
                    table.innerHTML = '';
                    if (data.length === 0) {
                        table.innerHTML = '<tr><td colspan="4">No heroes found. Try running seed.py!</td></tr>';
                    } else {
                        data.forEach(hero => {
                            table.innerHTML += `
                                <tr>
                                    <td>${hero.id}</td>
                                    <td>${hero.name}</td>
                                    <td>${hero.age || 'Unknown'}</td>
                                    <td>${hero.team_id || 'None'}</td>
                                </tr>
                            `;
                        });
                    }
                })
                .catch(error => {
                    document.getElementById('heroes-table').innerHTML = '<tr><td colspan="4">Error loading heroes.</td></tr>';
                    console.error('Error:', error);
                });
        </script>
    </body>
    </html>
    """
    return html_content
