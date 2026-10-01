from sqlmodel import Session, select, SQLModel
from app.database import engine
from app.models import Hero, Team, Mission

def seed_data():
    # Schema is now managed by Alembic, so we don't call create_all here
    
    with Session(engine) as session:
        if session.exec(select(Team)).first():
            print("already seeded")
            return

        team_avengers = Team(name="Avengers", headquarters="New York")
        team_xmen = Team(name="X-Men", headquarters="Westchester")
        team_jl = Team(name="Justice League", headquarters="Watchtower")
        team_ff = Team(name="Fantastic Four", headquarters="Baxter Building")
        
        mission_1 = Mission(title="Battle of Sokovia")
        mission_2 = Mission(title="Protect Genosha")
        mission_3 = Mission(title="Defeat Thanos")
        mission_4 = Mission(title="Save Gotham")
        mission_5 = Mission(title="Explore Negative Zone")

        heroes_data = [
            ("Tony", 45, "Iron Man", team_avengers),
            ("Natasha", 35, "Black Widow", team_avengers),
            ("Peter", 16, "Spider-Man", team_avengers),
            ("Steve", 100, "Captain America", team_avengers),
            ("Thor", 1500, "Thor", team_avengers),
            ("Bruce", 40, "Hulk", team_avengers),
            ("Clint", 40, "Hawkeye", team_avengers),
            ("Wanda", 28, "Scarlet Witch", team_avengers),
            ("Logan", 150, "Wolverine", team_xmen),
            ("Ororo", 30, "Storm", team_xmen),
            ("Scott", 32, "Cyclops", team_xmen),
            ("Jean", 32, "Phoenix", team_xmen),
            ("Charles", 60, "Professor X", team_xmen),
            ("Hank", 45, "Beast", team_xmen),
            ("Clark", 35, "Superman", team_jl),
            ("Bruce W.", 40, "Batman", team_jl),
            ("Diana", 800, "Wonder Woman", team_jl),
            ("Barry", 25, "The Flash", team_jl),
            ("Arthur", 35, "Aquaman", team_jl),
            ("Reed", 45, "Mr. Fantastic", team_ff),
            ("Sue", 40, "Invisible Woman", team_ff),
            ("Johnny", 28, "Human Torch", team_ff),
            ("Ben", 45, "The Thing", team_ff)
        ]

        heroes = []
        for name, age, secret, team in heroes_data:
            h = Hero(name=name, age=age, secret_name=secret, team=team)
            heroes.append(h)

        # Assign some missions
        heroes[0].missions.extend([mission_1, mission_3])
        heroes[1].missions.extend([mission_1, mission_3])
        heroes[2].missions.append(mission_1)
        heroes[8].missions.append(mission_2)
        heroes[9].missions.append(mission_2)
        heroes[15].missions.append(mission_4)
        heroes[14].missions.append(mission_4)
        heroes[19].missions.append(mission_5)
        
        session.add(team_avengers)
        session.add(team_xmen)
        session.add(team_jl)
        session.add(team_ff)
        
        session.commit()
        print("Database seeded!")

if __name__ == "__main__":
    seed_data()
