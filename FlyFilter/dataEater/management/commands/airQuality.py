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
isoConverter = {} #Contains iso3 and the iso2 representation
inputPathISO = "/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/dataEater/management/commands/Files/isoConverter.csv"
inputPathWB = "/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/dataEater/management/commands/Files/airQuality.csv"
inputPathFiltersWeather = "/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/filtersWeather.json"

FiltersWeather = {}

def readFileISOS(inputPath):
    """
        Given a input path reads the file
    """
    with open(inputPath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count != 0 and row[1] and row[2]:
                isoConverter[row[1]] = row[2]


def getInfoCSV(inputPath):
    """
        From the WB .csv read the info and writes it on the dict of contries.
    """
    with open(inputPath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0 and row[1] and row[2] and row[1] in isoConverter and isoConverter[row[1]] in FiltersWeather:
                FiltersWeather[isoConverter[row[1]]]["AirQuality"] = [row[2]]*12
            line_count += 1
    
    with open('filters.json', 'w') as json_file:
        json.dump(FiltersWeather, json_file)

class Command(BaseCommand):
    help = ('Reads all the geosales info that we have on our system, and saves to json files. it needs two excels file to work:   (1) [labelDict.xlsx]: contains all the labels that we have check and the isos that we assing. (2) +[regDict.xlsx]: contains all the regions that we can find in the first file, and the resprective isos')

    def add_arguments(self, parser):
        #The excel that contains the dictionary

        parser.add_argument('--verbose',  help="print the logs to stdout", action='store_true', default=False)
        parser.add_argument('-d', '--dryRun', help='Print the parsed WSDL', action="store_true", default=False)

        parser.add_argument('-o','--outputPath',  help="Folder in with the generated files will be stored",type=str, default="")
        parser.add_argument('--inputPathISO',  help="Csv files with iso3 and iso2", type=str, default=False)
        parser.add_argument('--inputPathWB',  help="Csv from WB that contains the air quality of the ", type=str, default=False)


    def handle(self, *args, **options):
        try:

            global FiltersWeather
            with open(inputPathFiltersWeather) as json_file:
                FiltersWeather = json.load(json_file)

            readFileISOS(inputPathISO)
            getInfoCSV(inputPathWB)
            
            

        except Exception as e:
            # ENSURE WE ALWAYS CLOSE THE CONNECTION
            #logging.error("Exception %s", repr(e))

            print("Exception")
            import traceback
            traceback.print_exc()

        except KeyboardInterrupt:
            print "Interrupted manually"
            #logging.error("Interrupted manually")
