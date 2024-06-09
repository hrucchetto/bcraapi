import argparse
import logging

from classes.importer import Importer
from classes.visualizer import Visualizer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def main():
    
    parser = argparse.ArgumentParser(description='Script to get BCRA data')
    parser.add_argument(
        '-a',
        '--action', 
        type=str, 
        choices=['import', 'visualize'], 
        default='visualize'
    )
    parser.add_argument('-i', '--init_date', type=str, required=False)
    parser.add_argument('-f','--final_date', type=str, required=False)
    parser.add_argument('-v','--vars', type=str, required=False)

    args = parser.parse_args()
    action, start_date, end_date, vars = args.action, args.init_date, args.final_date, args.vars
    
    if action == 'import':
        
        LOGGER.info('Starting import process')
        
        if start_date == None or end_date == None:
            start_date = str(input('Please enter the start date of the analysis (YYYY-MM-DD): '))
            end_date = str(input('Now the end date of the analysis (YYYY-MM-DD): '))
    
        bcra_importer = Importer(action, start_date, end_date, vars)
        bcra_importer.run()

    else:

        bcra_visualizer = Visualizer()
        bcra_visualizer.run()

if __name__ == "__main__":
    main()
