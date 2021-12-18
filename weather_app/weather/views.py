import os
from .forms import CityForm
from django.shortcuts import render
import requests
from .models import City
from dotenv import load_dotenv

load_dotenv()
# Create your views here.


def index(request):
    API_KEY = os.getenv('API_KEY')
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid="+API_KEY
    err_msg = ''
    message = ''
    message_class = ''
    cities = City.objects.all()
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist'
            else:
                err_msg = 'City already exists in database!'
    if err_msg:
        message = err_msg
        message_class = 'is-danger'
    else:
        message = 'City added successfully!'
        message_class = 'is-success'
    print(err_msg)
    form = CityForm()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data,
               'form': form,
               'message': message,
               'message_class': message_class}

    return render(request, 'weather/weather.html', context)
