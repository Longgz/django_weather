from urllib.request import Request
import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=2f76566d05d81ceaaf4b1554af8e6e55'
    city = 'Ha Noi'

    if request.method == 'POST':
        form = CityForm(request.POST)
        r_post = request.POST['name']
        r_api = requests.get(url.format(r_post)).json()
        if(r_api['cod'] == 200):
            form.save()
        else:
            pass

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        
        if(r['cod'] == 200):
            city_weather = {
                'city' : city.name,
                'tempurature' : float('{:.2f}'.format(r['main']['temp'] - 273.15)),
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }

            weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)