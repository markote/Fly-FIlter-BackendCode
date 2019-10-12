# coding=utf-8
'''
Reads the temperature data from the hdf fis from nasa, on the following link:
https://disc.gsfc.nasa.gov/datasets/MOD11CM1D_005/summary?keywords=temperature
'''
#python manage.py temperature --inputPath /home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/dataEater/management/commands/Files/MOD11CM1_v005_day___lst_2014m01.hdf
from django.core.management.base import BaseCommand
import h5py


def readFile(inputPath):
    """
        Given a input path reads the file
    """
    with h5py.File(inputPath, 'r') as f:
        print("Keys: %s" % f.keys())
        a_group_key = list(f.keys())[0]

        # Get the data
        data = list(f[a_group_key])

class Command(BaseCommand):
    help = ('Reads all the geosales info that we have on our system, and saves to json files. it needs two excels file to work:   (1) [labelDict.xlsx]: contains all the labels that we have check and the isos that we assing. (2) +[regDict.xlsx]: contains all the regions that we can find in the first file, and the resprective isos')

    def add_arguments(self, parser):
        #The excel that contains the dictionary

        parser.add_argument('--verbose',  help="print the logs to stdout", action='store_true', default=False)
        parser.add_argument('-d', '--dryRun', help='Print the parsed WSDL', action="store_true", default=False)

        parser.add_argument('-o','--outputPath',  help="Folder in with the generated files will be stored",type=str, default="")
        parser.add_argument('--inputPath',  help="Folder in with the needed files are", type=str, default=False)


    def handle(self, *args, **options):
        try:

            
            if options['inputPath']:
                readFile(options['inputPath'])
                
            
            

        except Exception as e:
            # ENSURE WE ALWAYS CLOSE THE CONNECTION
            #logging.error("Exception %s", repr(e))

            print("Exception")
            import traceback
            traceback.print_exc()

        except KeyboardInterrupt:
            print "Interrupted manually"
            #logging.error("Interrupted manually")
