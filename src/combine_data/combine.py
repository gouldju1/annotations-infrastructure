#Required Packages
import sqlite3
import pandas as pd
import time
import calendar

#Combine Datasets within ONE Database
def combine_within_database(db_path, new_dataset_name, datasets_to_combine):
    """
    db_path             : (str) Path to database where data are stored and new dataset to be created
    new_dataset_name    : (str) Name of new dataset to create
    datasets_to_combine : (list w/ str) List of names of datasets to combine into `new_dataset_name`
    """
    #Connect to DB
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    #Get Current Epoch Time
    epoch = calendar.timegm(time.gmtime())

    #Create a Dataset in Database
    c.execute(f"INSERT INTO dataset VALUES (NULL, '{new_dataset_name}', {epoch},'{{}}', 0)")

    #Commit to Database
    conn.commit()

    #Get New ID
    new_dataset_id = pd.read_sql_query(f"SELECT id FROM dataset WHERE name = '{new_dataset_name}'", conn)["id"][0]

    #Get IDs of Datasets to Combine
    example_dfs = []
    for dataset in datasets_to_combine:
        #ID of Dataset to Combine
        id = pd.read_sql_query(f"SELECT id FROM dataset WHERE name = '{dataset}'", conn)["id"][0]
        
        #Get All Examples of Dataset to Combine------
        #Determine which Examples to Pull
        links = pd.read_sql_query(f"SELECT example_id FROM link WHERE dataset_id = {id}", conn)["example_id"].values.tolist()

        #Pull Examples
        examples = pd.read_sql_query(f"""SELECT input_hash, task_hash, content FROM example WHERE id IN({",".join([(lambda x: str(x))(x) for x in links])})""", conn)
        
        #Add to Examples df
        example_dfs.append(examples)

    #Combine DataFrames into One
    examples_to_add = pd.concat(example_dfs).reset_index(drop=True)

    #Add Examples to Database
    for index, row in examples_to_add.iterrows():
        #INSERT INTO example Table
        c.execute(f"""INSERT INTO example VALUES (NULL, {row['input_hash']}, {row['task_hash']}, '{row['content'].decode("utf-8").replace("'", "''")}')""")
        conn.commit()
        
        #Get Example ID
        example_id = pd.read_sql_query(f"SELECT MAX(id) AS id FROM example", conn)["id"][0]
        
        #INSERT INTO link Table
        c.execute(f"INSERT INTO link VALUES (NULL, {example_id}, {new_dataset_id})")
        conn.commit()
    
    #Close Database
    conn.close()

    print(f"Completed! Added {datasets_to_combine} as {new_dataset_name} in {db_path}")

#Combine Datasets across MULTIPLE Databases
def combine_databases(d, fix_error=False):
    """
    d : (dict) Containing the following
        d = {"databases" : 
                {
                "PATH_TO_DATABASE_TO_COMBINE" :  {
                                    "datasets_to_combine" : ["DATASET_1", "DATASET_2", ...]
                                    },
                "PATH_TO_DATABASE_TO_COMBINE" :  {
                                    "datasets_to_combine" : ["DATASET_1", "DATASET_2", ...]
                                    },
                                    ...
                        },
        "new_dataset_name" : "NAME_OF_DATASET_TO_CREATE",
        "db_path_to_save"  : "PATH_TO_DATABASE_TO_STORE_COMBINED_DATA"
            }
    """
    #Set up Input Variables
    db_path_to_save = d["db_path_to_save"]
    new_dataset_name = d["new_dataset_name"]

    #List for Example DataFrames
    example_dfs = []

    #Get Current Epoch Time
    epoch = calendar.timegm(time.gmtime())

    #Connect to Database to Save
    conn_save = sqlite3.connect(db_path_to_save)
    c_save = conn_save.cursor()

    #Create a Dataset in Database
    c_save.execute(f"INSERT INTO dataset VALUES (NULL, '{new_dataset_name}', {epoch},'{{}}', 0)")

    #Commit to Database
    conn_save.commit()

    #Get New ID
    new_dataset_id = pd.read_sql_query(f"SELECT id FROM dataset WHERE name = '{new_dataset_name}'", conn_save)["id"][0]

    #Iterate through Each Input Database
    for database in d["databases"].keys():
        #Set Input Values
        db_path = database
        datasets_to_combine = d["databases"][database]["datasets_to_combine"]
        
        #Connect to DB
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        #Get IDs of Datasets to Combine
        for dataset in datasets_to_combine:
            #ID of Dataset to Combine
            id = pd.read_sql_query(f"SELECT id FROM dataset WHERE name = '{dataset}'", conn)["id"][0]

            #Get All Examples of Dataset to Combine------
            #Determine which Examples to Pull
            links = pd.read_sql_query(f"SELECT example_id FROM link WHERE dataset_id = {id}", conn)["example_id"].values.tolist()

            #Pull Examples
            examples = pd.read_sql_query(f"""SELECT input_hash, task_hash, content FROM example WHERE id IN({",".join([(lambda x: str(x))(x) for x in links])})""", conn)

            #Add to Examples df
            example_dfs.append(examples)
    
    if fix_error:
        drop_range = list(range(250, 300))

        example_dfs[-1] = example_dfs[-1].drop(drop_range).reset_index(drop=True)

    #Combine DataFrames into One
    examples_to_add = pd.concat(example_dfs).reset_index(drop=True)

    #Add Examples to Database
    for index, row in examples_to_add.iterrows():
        #INSERT INTO example Table
        try:
            new_text = row['content'].decode("utf-8").replace("'", "''")
        except:
            #new_text = row['content'].replace("'", "''")
            continue
        
        if "FAIL_CODE" in new_text:
            continue
        else:
            c_save.execute(f"""INSERT INTO example VALUES (NULL, {row['input_hash']}, {row['task_hash']}, '{new_text}')""")
            conn.commit()

            #Get Example ID
            example_id = pd.read_sql_query(f"SELECT MAX(id) AS id FROM example", conn_save)["id"][0]

            #INSERT INTO link Table
            c_save.execute(f"INSERT INTO link VALUES (NULL, {example_id}, {new_dataset_id})")
            conn_save.commit()

    #Close Database
    conn_save.close()

    print(f"Completed! Added data as {new_dataset_name} in {db_path_to_save}")