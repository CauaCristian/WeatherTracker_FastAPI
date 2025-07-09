# WeatherTracker_FastAPI
Uma API que permite ao usuário cadastrar cidades que deseja acompanhar. A API consome dados de clima em tempo real (ex: da OpenWeatherMap) e salva no banco PostgreSQL. Para evitar múltiplas chamadas à API externa, os dados climáticos são cacheados no Redis com tempo de expiração
