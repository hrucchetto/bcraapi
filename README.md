# BCRA Importer

During 2024 Central Bank of Argentine Republic (BCRA) published its API with several endpoints to import the most revelant variables. 
The idea of the script is to automate the import and visualize the results using a python program.
More details about the endpoints can be found [here](https://www.bcra.gob.ar/Catalogo/apis.asp?fileName=principales-variables-v1).

## Setup environment

You can find all the packages needed, to run this program in your local computer, within `requirements.txt` file.

```bash
$ python install -r requirements.txt
```

Note: I suggest creating a virtual enviroment to isolate the project.

## Usage

The script has four arguments:

- Action (required): Possible values (import, visualize = default value).
- Initial date (optional).
- Final data (optional).
- Variables (optional).

Running the following command you can store/update data within a sqlite db in `outputs/bcra.db`.

```bash
$ python bcra.py -a action -i init_date -f final_date -v vars 
```

**1. Action**

- Import: It updates a final table stored within a sqlite database.
- Visualize: This class is used to build a streamlit app to visualize the data obtained.

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

`Visualizer` class contains the code to build a streamlit application to visualize some tiles with data from the db we created. 
You can check a preliminar version [here](https://bcraapi.streamlit.app/).
