import argparse
import logging

from src.importer import Importer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def main():
    
    LOGGER.info('Set parameters')
    parser = argparse.ArgumentParser(description='Script to get BCRA data, you need to enter start_date, end_date and environment')
    parser.add_argument(
        '-e',
        '--environment', 
        type=str, 
        choices=['production', 'test'], 
        required=True
    )
    parser.add_argument('-i', '--init_date', type=str, required=False)
    parser.add_argument('-f','--final_date', type=str, required=False)
    parser.add_argument('-v','--vars', type=str, required=False)

    args = parser.parse_args()
    env, start_date, end_date, vars = args.environment, args.init_date, args.final_date, args.vars
    
    LOGGER.info('Get inputs from users')
    if (env == 'production') and (start_date == None or end_date == None):
        start_date = str(input('Please enter the start date of the analysis (YYYY-MM-DD): '))
        end_date = str(input('Now the end date of the analysis (YYYY-MM-DD): '))
    
    bcra = Importer(env, start_date, end_date, vars)
    bcra.run()

if __name__ == "__main__":
    main()
