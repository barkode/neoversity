# 1. Запустити контейнери (у папці з docker-compose.yml)
`docker compose up -d`

# 2. Дочекатися запуску (перевірити статус)
`docker compose ps`

# 3. Завдання 1 — PostgreSQL
`pip install psycopg2-binary faker`

`python task_manager/create_tables.py`

`python task_manager/seed.py`

# 4. Завдання 2 — MongoDB
`pip install pymongo`

`python cats_mongo/main.py`

# 5. Зупинити контейнери (дані збережуться у volumes)

`docker compose down`