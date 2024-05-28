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

- Action (required): Possible values (import, visualize, test).
- Initial and final date (optional).
- Variables (optional).

Running the following command you can store/update data within a sqlite db in `outputs/bcra.db`.

```bash
$ python bcra.py -a action -i init_date -f final_date -v vars 
```

Note: if you only want to test the API connection you can run this command:

```bash
$ python bcra.py -a test
```

**1. Action**

- Import: It updates the data within a sqlite file.
- Visualize: This class is used to build a streamlit app to visualize the data obtained.
- Test: It's used to test that the code does not have issues when new changes are pushed.

**2. Initial and final dates**

It's important to enter the correct format for start and end date (YYYY-MM-DD).
Otherwise, the script will only consider the last 2 months by default.

**3. Variable IDs**

Then, you will need to select the ids of the variables you want to analyze in the future.
If you do not provide any id, the script will generate a file with all the variables that are available in the BRCA.

## Automatic update

In `.github/workflows` folder there is a yaml file with a process to update the database automatically.
The jobs runs daily and updates the db with new values for the variables.

## Visualize

`Visualyzer` class contains the code to build a streamlit application to visualize some tiles with data from the db we created. 
You can check a preliminar version [here](https://bcraapi.streamlit.app/).

## Contact

You can reach me out in [LinkedIn](https://www.linkedin.com/in/hugo-rucchetto/).
