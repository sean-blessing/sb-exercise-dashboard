# sb-exercise-dashboard
This is a personal project w/ 2 goals:
1) Generate personalized Strava reports that I can't get from the app nor website
2) Learn some new stuff in Python: OAuth, Relational DB fundamentals (psycopg, SQLAlchemy, FastAPI/Flask)
3) Learn PostgresQL - I know relational DBs very well but have never played w/ Postgres!




## Java -> Python Analogous Things

| Java ecosystem                    | Python ecosystem                      | Role                                 |
| --------------------------------- | ------------------------------------- | ------------------------------------ |
| JDBC                              | **psycopg**                           | Low-level database connectivity      |
| `Connection`                      | `psycopg.Connection`                  | Database connection                  |
| `Statement` / `PreparedStatement` | `cursor.execute()`                    | Execute SQL                          |
| `ResultSet`                       | `cursor.fetchone()` / `fetchall()`    | Retrieve results                     |
| JPA / Hibernate                   | **SQLAlchemy**                        | ORM                                  |
| Spring Data JPA                   | **SQLAlchemy ORM / SQLModel**         | Higher-level persistence abstraction |
| Spring Boot                       | **FastAPI / Flask**                   | Web/API application framework        |
| `application.properties`          | `.env` + config code                  | Configuration                        |
| Maven `pom.xml`                   | `requirements.txt` / `pyproject.toml` | Dependencies/build configuration     |
