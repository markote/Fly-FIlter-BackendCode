# coding=utf-8
'''
Reads the temperature data from the hdf fis from nasa, on the following link:
https://disc.gsfc.nasa.gov/datasets/MOD11CM1D_005/summary?keywords=temperature
'''
#python manage.py temperature --inputPath /home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/dataEater/management/commands/Files/MOD11CM1_v005_day___lst_2014m01.hdf
from django.core.management.base import BaseCommand
import csv
import requests
import time
import json
isoConverter = {} #Contains iso3 and the iso2 representation


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


def getInfoWeb(verbose):
    """
        Attacks the api for the values

    """
    FiltersDict = {}
    for tyeRequest in ["tas","pr"]:
        for iso in isoConverter:
            url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/mavg/"+ tyeRequest +"/1980/1999/"+ iso + ".json"
            resp = requests.get(url=url, params={})
            try:
                data = resp.json()
                if data and len(data) and 'monthVals' in data[-1]:
                    data = data[-1]['monthVals']
                    FiltersDict.setdefault( isoConverter[iso], {} )[tyeRequest] = data
                    if verbose:
                        if tyeRequest == "tas":
                            print "Temp ", iso, " OK!"
                        else:
                            print "Rain ", iso, " OK!"
                else:
                    if verbose:
                        if tyeRequest == "tas":
                            print "Temp ", iso, " FAAAIL!"
                        else:
                            print "Rain ", iso, " FAAAIL!"
            except:
                if verbose:
                    if tyeRequest == "tas":
                        print "Temp ", iso, " FAAAIL!"
                    else:
                        print "Rain ", iso, " FAAAIL!"
                pass
            time.sleep(1)
    print FiltersDict
    with open('filters.json', 'w') as json_file:
        json.dump(FiltersDict, json_file)

class Command(BaseCommand):
    help = ('Reads all the geosales info that we have on our system, and saves to json files. it needs two excels file to work:   (1) [labelDict.xlsx]: contains all the labels that we have check and the isos that we assing. (2) +[regDict.xlsx]: contains all the regions that we can find in the first file, and the resprective isos')

    def add_arguments(self, parser):
        #The excel that contains the dictionary

        parser.add_argument('--verbose',  help="print the logs to stdout", action='store_true', default=False)
        parser.add_argument('-d', '--dryRun', help='Print the parsed WSDL', action="store_true", default=False)

        parser.add_argument('-o','--outputPath',  help="Folder in with the generated files will be stored",type=str, default="")
        parser.add_argument('--inputPathISO',  help="Csv files with iso3 and iso2", type=str, default=False)


    def handle(self, *args, **options):
        try:

            
            if options['inputPathISO']:
                readFileISOS(options['inputPathISO'])
                getInfoWeb(options['verbose'])
            
            

        except Exception as e:
            # ENSURE WE ALWAYS CLOSE THE CONNECTION
            #logging.error("Exception %s", repr(e))

            print("Exception")
            import traceback
            traceback.print_exc()

        except KeyboardInterrupt:
            print "Interrupted manually"
            #logging.error("Interrupted manually")
