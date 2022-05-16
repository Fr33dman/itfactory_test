# ITFactory_test

## Start project

```shell
docker build -t itfactory .
docker run -dp 8000:8000 itfactory
```

## Endpoints

/api/shops/view/<phone_number>/ - просмотр торговых точек привязанных к сотруднику
/api/shops/visit/<phone_number>/ - визит сотрудника в торговую точку, ниже приведены параметры для POST запроса на этот эндпоинт
trade_poin - <int> - id торговой точки 
longitude - <string> - долгота
latitude - <string> - широта
