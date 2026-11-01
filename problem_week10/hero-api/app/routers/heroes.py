from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.database import SessionDep
from app.models import Hero, HeroCreate, HeroPublic, HeroUpdate, Team

router = APIRouter(prefix="/heroes", tags=["heroes"])

def ensure_team_exists(session, team_id: int | None):
    if team_id is not None and not session.get(Team, team_id):
        raise HTTPException(status_code=400, detail=f"Team {team_id} does not exist")

@router.post("", response_model=HeroPublic, status_code=201, summary="Create a hero",
             responses={400: {"description": "Team does not exist"}})
def create_hero(hero_in: HeroCreate, session: SessionDep):
    ensure_team_exists(session, hero_in.team_id)
    hero = Hero.model_validate(hero_in)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@router.get("", response_model=list[HeroPublic], summary="List heroes")
def list_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
    min_age: int | None = None,
    team_id: int | None = None,
    name: str | None = None,
):
    statement = select(Hero)
    if min_age is not None:
        statement = statement.where(Hero.age >= min_age)
    if team_id is not None:
        statement = statement.where(Hero.team_id == team_id)
    if name:
        statement = statement.where(Hero.name.ilike(f"%{name}%"))
    statement = statement.order_by(Hero.id).offset(offset).limit(limit)
    return session.exec(statement).all()

def get_hero_or_404(session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.get("/{hero_id}", response_model=HeroPublic, summary="Get one hero",
            responses={404: {"description": "Hero not found"}})
def read_hero(hero_id: int, session: SessionDep):
    """Return a single hero by its **id**."""
    return get_hero_or_404(session, hero_id)

@router.patch("/{hero_id}", response_model=HeroPublic, summary="Update a hero partially",
              responses={400: {"description": "Team does not exist"}, 404: {"description": "Hero not found"}})
def update_hero(hero_id: int, hero_in: HeroUpdate, session: SessionDep):
    hero = get_hero_or_404(session, hero_id)
    data = hero_in.model_dump(exclude_unset=True)
    if "team_id" in data:
        ensure_team_exists(session, data["team_id"])
    hero.sqlmodel_update(data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@router.delete("/{hero_id}", status_code=204, summary="Delete a hero")
def delete_hero(hero_id: int, session: SessionDep):
    hero = get_hero_or_404(session, hero_id)
    session.delete(hero)
    session.commit()
