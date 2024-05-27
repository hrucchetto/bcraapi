# BCRA Importer

During 2024 BCRA launched some endpoints to import the most revelant Argentine economic variables. 
The idea of the script is to automate the import and visualize the results.
More details about the endpoints can be found [here](https://www.bcra.gob.ar/Catalogo/apis.asp?fileName=principales-variables-v1).

## Setup environment

You can find all the packages needed, to run this program in your local computer, within `requirements.txt` file.

```bash
$ python install -r requirements.txt
```

Note: I suggest creating a virtual enviroment to isolate the project.

## Usage

The script has four arguments:

- Environment (required): Possible values (production, test).
- Initial and final date (optional).
- Variables (optional).

Running the following command you can get the data in your current directory within a file called `outputs/bcra_dataset.csv`.

```bash
$ python bcra.py -e environment -i init_date -f final_date -v vars 
```

Note: if you only want to test the API connection you can run this command:

```bash
$ python bcra.py -e test
```

**1. Environment**

Possible values: production or test.

**2. Initial and final dates**

It's important to enter the correct format for start and end date (YYYY-MM-DD).
Otherwise, the script will only consider de last 2 months.

**3. Variable IDs**

Then, you will need to select the ids of the variables you want to analyze in the future.
If you do not provide any id, the script will generate a file with all the variables that are available in the BRCA.

## Analysis (To be replaced)

The `Analyzer` class will take the csv got from the previous step and create a tile with the data obtained. The result will be stored in the `outputs` folder. 

You can find a link with a tile with the following varibles: UVA, monetary policy and BADLAR rate.

You can use the downloaded file and analyze it with a different tool, such as `duckdb`.
Please check the full documentation [here](https://duckdb.org/docs/index).

## Contact

You can reach me out in [LinkedIn](https://www.linkedin.com/in/hugo-rucchetto/).
