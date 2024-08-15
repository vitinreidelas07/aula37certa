import requests

response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Pato%20Branco&appid=d77c765fe183231b80c00659032e10cf&units=metric")

data = response.json()
print("Temperatura:", data['main']['temp'], "°C")