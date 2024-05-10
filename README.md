# BCRA Variables

The idea of the script is to get macroeconomic data that BCRA provides us, using its API.
[Here](https://www.bcra.gob.ar/Catalogo/apis.asp?fileName=principales-variables-v1) you can find more details about the endpoints used.

## Setup environment

You can find all the packages needed, to run this program in your local computer, within `requirements.txt` file.

## Usage

Running the following command you can get the selected data in your current directory within a folder called `output/<runtime_date>_bcra_dataset`.

```bash
$ python main.py
```

You will be asked to enter some input during the process.

**1. Start and end dates**

It's important to enter the correct formats for start and end date (YYYY-MM-DD).
Otherwise, the script will only consider de last 2 months.

**2. Variable IDs**
Then, you will need to select the ids of the variables you want to analyze in the future.
If you do not provide any id, the script will generate a file with all the variable that are available in the BRCA.

## Contact

You can find me in [LinkedIn](https://www.linkedin.com/in/hugo-rucchetto/).
