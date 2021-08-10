#COPYRIGHT Justin A. Gould

#Required Packages
import pandas as pd
import numpy as np
import sqlite3
import json

#Suppress warnings
import warnings
warnings.filterwarnings("ignore")

def create_master(path, entities):
    #Create num_classes variable
    num_classes = len(entities)
    
    #Read JSONL
    with open(path, "r") as f:
        json_list = list(f)

    #List of JSONL bases
    bases = []
    for json_str in json_list:
        bases.append(json.loads(json_str))
    
    #Loop Through Base Object to Build LoL for DataFrame
    df_master_values = []
    for base in bases:
        _values = []
        #Get Document ID
        document_id = base["_input_hash"]

        #Get all Tokens
        for token in base["tokens"]:
            token_name = token["text"]
            token_id = token["id"]

            #Add to Internal List
            _values = [token_name, token_id, document_id]

            #`0` values for NER Classes
            _values.extend([(lambda x: 0)(x) for x in range(0, num_classes + 1)]) #Add NA class

            #Add Values to Master List
            df_master_values.append(_values) 
    
    #Define Entities and Columns
    columns = ["token_value", "token_id", "document_id"]

    #Add entities as columns (wide format)
    columns.extend(entities)
    columns.extend(["NA"]) #Not Annotated Class

    #DataFrame
    master = pd.DataFrame(data=df_master_values, columns=columns)
    
    return master

def populate_master(db_paths, dataset_name, master):
    #Connect to DB
    for db_path in db_paths:
        print(db_path, "\n")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        #Get all data within specified set

        dataset_id = pd.read_sql_query(f"SELECT id FROM dataset WHERE name = '{dataset_name}'", conn)["id"][0]

        #Get all examples within dataset------
        #Determine which Examples to Pull
        links = pd.read_sql_query(f"SELECT example_id FROM link WHERE dataset_id = {dataset_id}", conn)["example_id"].values.tolist()

        #Pull Examples
        examples = pd.read_sql_query(f"""SELECT * FROM example WHERE id IN({",".join([(lambda x: str(x))(x) for x in links])})""", conn)

        #Loop through examples
        for index, row in examples.iterrows():
            #Extract annotated content
            content = json.loads(row["content"].decode("utf-8"))

            #Get input_hash (document_id)
            document_id = row["input_hash"]

            #Query subset of master dataframe...current document
            subset = master[master["document_id"] == document_id]

            #If not rejected
            if content["answer"] in ["reject", "ignore"]:
                #Add 1 for each token to NA entity
                subset["NA"] = [x+1 for x in subset["NA"].values.tolist()]

                #Update Master with new values
                master.update(subset)
            else:
                #Iterate through annotated spans from DB
                if "spans" in list(content.keys()):
                    spans = content["spans"]
                    
                    if "token_start" in list(spans[0].keys()):
                        #Iterate through spans
                        tokens_annotated = []
                        for span in spans:
                            #ID Information
                            start = span["token_start"]
                            end = span["token_end"]
                            entity = span["label"]

                            ##############################################################################
                            # Handle wrong entity name...                                                #
                            ##############################################################################

                            if entity == "PARTN_NAME":
                                entity = "PART_NAME"
                            elif entity == "TIMESTAMP}":
                                entity = "TIMESTAMP"
                            else:
                                entity = entity

                            ##############################################################################
                            # END Handle wrong entity name...                                            #
                            ##############################################################################

                            #List of tokens w/ span's label
                            tokens_with_shared_label = [start] if start == end else list(range(start, end + 1))

                            #Add to list of tokens NOT to update NA value
                            tokens_annotated.extend(tokens_with_shared_label)

                            #Iterate through shared tokens
                            for token in tokens_with_shared_label:
                                #Token-level information...create a subset (row)
                                token_subset = subset[subset["token_id"] == token]

                                #Get index and column IDs for updating value
                                token_entry_index = token_subset.index.tolist()[0]

                                #Update by 1
                                master.at[token_entry_index, entity] += 1

                        #Update unused Tokens' NA count
                        for index, row in subset.iterrows():
                            #If token is NOT included in list, NA +=1
                            if row["token_id"] not in tokens_annotated:
                                #Token Value list to update
                                value_list = subset.loc[index].values.tolist()

                                #Update by 1
                                master.at[index, "NA"] += 1
                    #INSERT
                    else:
                        #Add 1 for each token to NA entity
                        subset["NA"] = [x+1 for x in subset["NA"].values.tolist()]

                        #Update Master with new values
                        master.update(subset)
                else:
                    #Add 1 for each token to NA entity
                    subset["NA"] = [x+1 for x in subset["NA"].values.tolist()]

                    #Update Master with new values
                    master.update(subset)
    
    return master