# coding=utf-8
'''
Reads the temperature data from the hdf fis from nasa, on the following link:
https://disc.gsfc.nasa.gov/datasets/MOD11CM1D_005/summary?keywords=temperature
'''
#python manage.py temperature --inputPathISO /home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/dataEater/management/commands/Files/isoConverter.csv --inputPathWB /home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/dataEater/management/commands/Files/
from django.core.management.base import BaseCommand
import csv
import requests
import time
import json
import random
isoConverter = {} #Contains iso3 and the iso2 representation
inputPathISO = "/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/dataEater/management/commands/Files/isoConverter.csv"
inputPathWB = "/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/dataEater/management/commands/Files/airQuality.csv"
inputPathFiltersWeather = "/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/filters.json"

FiltersWeather = {}
CitiesInfoSS = {}


def callSkyScanner():
    citiesInfo = []
    url = "https://www.skyscanner.net/g/chiron/api/v1/places/geo/v1.0"
    data = requests.get(url = url, headers ={'api-key': 'skyscanner-hackupc2019'}).json()
    i = 0
    j = 0
    global CitiesInfoSS
    for continent in data['Continents']:
        for country in continent['Countries']:
            for city in country['Cities']:
                #print i,city['Name'],city['Location']
                i +=1
                if  city['CountryId'] in FiltersWeather and len(FiltersWeather[city['CountryId']]) == 3:
                    #print city['Name'].encode('utf-8')
                    aux = {
                        'name':             city['Name'],
                        'location':         city['Location'],
                        'country':          city['CountryId'],
                        'id':               city['Id'],
                        'temperature':      ["{0:.2f}".format(v + random.uniform(-3, 3)) for v in FiltersWeather[city['CountryId']]['tas'] ],
                        'precipitation':    ["{0:.2f}".format(v + random.uniform(-20, 20)) for v in FiltersWeather[city['CountryId']]['pr'] ],
                        'airQuality':       ["{0:.2f}".format(float(v) + random.uniform(-10, 10)) for v in FiltersWeather[city['CountryId']]['AirQuality'] ]
                    }
                    citiesInfo.append(aux)

                else:
                    #print j,'ERROOOOOR',city['CountryId']
                    j += 1
    with open('citiesInfo.json', 'w') as json_file:
        json.dump(citiesInfo, json_file)
    #print j


class Command(BaseCommand):
    help = ('Does a call to skyscanner api to retrive all the info of the cities')

    def add_arguments(self, parser):
        #The excel that contains the dictionary
        pass


    def handle(self, *args, **options):
        try:

            global FiltersWeather
            with open(inputPathFiltersWeather) as json_file:
                FiltersWeather = json.load(json_file)

            callSkyScanner()
            
            

        except Exception as e:
            # ENSURE WE ALWAYS CLOSE THE CONNECTION
            #logging.error("Exception %s", repr(e))

            print("Exception")
            import traceback
            traceback.print_exc()

        except KeyboardInterrupt:
            print "Interrupted manually"
            #logging.error("Interrupted manually")
