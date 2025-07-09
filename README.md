# WeatherTracker_FastAPI
Uma API que permite ao usuário cadastrar cidades que deseja acompanhar. A API consome dados de clima em tempo real da OpenWeatherMap e salva no banco PostgreSQL. Para evitar múltiplas chamadas à API externa, os dados climáticos são cacheados no Redis com tempo de expiração

🔧 Tecnologias:

FastAPI (framework principal)

PostgreSQL (armazenar usuários, cidades e histórico de clima)

Redis (cache de dados de clima)

requests (para consumir a API externa)

SQLAlchemy + Alembic (ORM e migrations)

Pydantic (validações)

📌 Exemplo de fluxo:

Usuário seleciona a cidade "Goiânia" 

A API busca o clima atual dessa cidade via OpenWeatherMap.

Salva o retorno no Redis com TTL de 30 minutos.

Salva também o retorno no PostgreSQL (histórico de clima).

Nova chamada em menos de 30 min → serve do Redis.

Após 30 min → busca novamente na API externa.
