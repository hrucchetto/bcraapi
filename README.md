# BCRA Variables

The idea of the script is to get macroeconomic data that BCRA provides us, using its API.
[Here](https://www.bcra.gob.ar/Catalogo/apis.asp?fileName=principales-variables-v1) you can find more details about the endpoints used.

## Setup environment

You can find all the packages needed, to run this program in your local computer, within `requirements.txt` file.

## Usage

Running the following command you can get the selected data in your current directory within a file called `outputs/bcra_dataset`.

```bash
$ python bcra.py -e environment -i init_date -f final_date -v vars 
```

The environment is a mandatory argument. Otherwise the script will fail.

Note: if you only want to test the API connection you can run this command:

```bash
$ python bcra.py -e test
```

**1. Environment**

Possible values are: production or test.

**2. Initial and final dates**

It's important to enter the correct format for start and end date (YYYY-MM-DD).
Otherwise, the script will only consider de last 2 months.

**3. Variable IDs**

Then, you will need to select the ids of the variables you want to analyze in the future.
If you do not provide any id, the script will generate a file with all the variables that are available in the BRCA.

## Analysis

In `outputs` folder you can find a link with a tile for 3 varibles: UVA, monetary policy and BADLAR rate.

You can use the downloaded file with different tools, such as `duckdb`.
You can find the documentation [here](https://duckdb.org/docs/index).

## Contact

You can reach me out in [LinkedIn](https://www.linkedin.com/in/hugo-rucchetto/).
