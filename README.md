# WeatherTracker_FastAPI
Uma API que permite ao usuário cadastrar cidades que deseja acompanhar. A API consome dados de clima em tempo real (ex: da OpenWeatherMap) e salva no banco PostgreSQL. Para evitar múltiplas chamadas à API externa, os dados climáticos são cacheados no Redis com tempo de expiração

Tecnologias:
FastAPI (framework principal)

PostgreSQL (armazenar usuários, cidades e histórico de clima)

Redis (cache de dados de clima)

requests (para consumir a API externa)

SQLAlchemy + Alembic (ORM e migrations)

Pydantic (validações)
