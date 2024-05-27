import argparse
import logging

from src.analyzer import Analyzer
from src.importer import Importer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def main():
    
    LOGGER.info('Set parameters')
    parser = argparse.ArgumentParser(description='Script to get BCRA data')
    parser.add_argument(
        '-a',
        '--action', 
        type=str, 
        choices=['import', 'visualize', 'test'], 
        default='visualize'
    )
    parser.add_argument('-i', '--init_date', type=str, required=False)
    parser.add_argument('-f','--final_date', type=str, required=False)
    parser.add_argument('-v','--vars', type=str, required=False)

    args = parser.parse_args()
    action, start_date, end_date, vars = args.action, args.init_date, args.final_date, args.vars
    
    if action in ['import', 'test']:
        
        LOGGER.info('Starting import process')
        
        if action == 'import' and (start_date == None or end_date == None):
            start_date = str(input('Please enter the start date of the analysis (YYYY-MM-DD): '))
            end_date = str(input('Now the end date of the analysis (YYYY-MM-DD): '))
    
        bcra = Importer(action, start_date, end_date, vars)
        bcra.run()

    else:

        LOGGER.info('Visualize BCRA dashboard')
        bcra_analyzer = Analyzer()
        bcra_analyzer.visualize()

if __name__ == "__main__":
    main()
