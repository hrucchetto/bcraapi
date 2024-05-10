from bcra.bcra_vars import BCRAVars

def main():
    
    start_date = str(input('Please enter the start date of the analysis (YYYY-MM-DD): '))
    end_date = str(input('Now the end date of the analysis (YYYY-MM-DD): '))

    conditions = start_date >= '2010-01-01' and end_date >= '2010-01-01' and end_date > start_date

    if not conditions:
        start_date = end_date = None

    bcra = BCRAVars(start_date, end_date)
    bcra.run()

if __name__ == "__main__":
    main()
