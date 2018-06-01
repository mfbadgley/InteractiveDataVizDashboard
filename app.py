from flask import Flask, render_template, jsonify, redirect
import sqlalchemy
import pymysql
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

#flask setup
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy


#engine setup
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
inspector = inspect(engine)
# Use the Base class to reflect the database tables
Base = automap_base()
Base.prepare(engine, reflect=True)

#mapped classes are created with names matching that of the table
#names
samples = Base.classes.samples
otu = Base.classes.otu
Samples_Metadata=Base.classes.samples_metadata

session = Session(engine)

#to check your sqlite database, go into terminal, in the folder where the database is stored, type sqlite3 'thenameofthedatabase'.sqlite enter
#then type your sql commands.ie...so Select * From Samples; <enter> to see the samples table shown in the terminal; 
#if data is there, then you are in a position to start with your SQL commands and retreieve your data!

@app.route("/")
    #Return the dashboard homepage.
def index():
    return render_template("index.html")

@app.route('/names')
def names():
    #create an empty array to store names
    sample_names =[]
    #get the columns from 'samples' table
    columns = inspector.get_columns('samples')
    for column in columns[1:]:
        sample_names.append(column['name'])
    print(sample_names)# prints in terminal for debugging..
#in flask app, use return, not print..jsonify will turn list into json object, the preferred method for web browsers;
#return jsonify(otu_list)
    return jsonify(sample_names)

  
    
@app.route('/otu')
  
def otuDesc():
#save results to a varaible, make results = session.query..etc....'lowest_taxonomic_unit_found' was 
#identified as the column desired from inspecting the columnn names 'inspector.get_columns('otu')...
    results=session.query(otu.lowest_taxonomic_unit_found).all()
#np.ravel..turns everything in to a list, 'unravels' and turns into a list; alternatively could also create an empty list and loop thru
#and append to the list; 
    otu_list=list(np.ravel(results))
    print(otu_list)
    return jsonify(otu_list)

@app.route('/metadata/<sample>')
def sample_metadata(sample):
    #storing query results (a sequel alchemy obj) in a variable
    sel=[Samples_Metadata.SAMPLEID,Samples_Metadata.ETHNICITY,Samples_Metadata.GENDER,
    Samples_Metadata.AGE,Samples_Metadata.LOCATION, Samples_Metadata.BBTYPE]
    
    #prints the obj (must loop thru to see values)
    print(sel)
    
    #queries the whole table (*sel), filter where SampleID matches the user input <sample>,  taking out the prefix 'BB_' which is 3 characters
    #*SEL is like SELECT * from SQL
    results=session.query(*sel).filter(Samples_Metadata.SAMPLEID == sample[3:]).all()
        
    print(results)
    #create empty dictionary
    sample_metadata={}
    #loop thru results and append to dictionary
    for result in results:
        #create a key value 'SAMPLEID' and it's value from results
        sample_metadata['SAMPLEID'] = result[0]
        sample_metadata['ETHNICITY'] = result[1]
        sample_metadata['GENDER'] = result[2]
        sample_metadata['AGE'] = result[3]
        sample_metadata['LOCATION'] = result[4]
        sample_metadata['BBTYPE'] = result[5]
    
    print(sample_metadata)
    return jsonify(sample_metadata)
    
@app.route('/wfreq/<sample>')
def sample_wfreq(sample):
    
    results=session.query(Samples_Metadata.WFREQ).filter(Samples_Metadata.SAMPLEID == sample[3:]).all()
    #turn results into list
    WFREQ = np.ravel(results)

    return jsonify(int(WFREQ))

@app.route('/samples/<sample>')
def samples(sample):
    """Return a list dictionaries containing `otu_ids` and `sample_values`."""
    #return the whole samples table into a variable
    stmt = 'SELECT * FROM samples'
    #load into pandas dataframe
    df = pd.read_sql_query(stmt, session.bind)

    # Make sure that the sample was found in the columns, else throw an error
    if sample not in df.columns:
        return jsonify(f"Error! Sample: {sample} Not Found!"), 400

    # Return any sample values greater than 1
    df = df[df[sample] > 1]

    # Sort the results by sample in descending order
    df = df.sort_values(by=sample, ascending=0)

    # Format the data to send as json, convert to list first
    data = [{
        "otu_ids": df[sample].index.values.tolist(),
        "sample_values": df[sample].values.tolist()
    }]
    return jsonify(data)
    

if __name__ == '__main__':
    app.run(debug=True)





