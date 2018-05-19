from flask import Flask, render_template, jsonify, redirect
import sqlalchemy
import pymysql
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

#flask setup
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
inspector = inspect(engine)

#engine setup
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
# Use the Base class to reflect the database tables
Base = automap_base()
Base.prepare(engine, reflect=True)

#mapped classes are created with names matching that of the table
#names
samples = Base.classes.samples
otu = Base.classes.otu
samples_metadata=Base.classes.samples_metadata

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
    sample_names =[]
    columns = inspector.get_columns('samples')
    for column in columns[1:]:
        sample_names.append(column['name'])
    print(sample_names)
    return jsonify(sample_names)

  
    
@app.route('/otu')
  
    #Returns a list of OTU descriptions in the following format

   # [
     #   "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
      #  "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
      #  "Bacteria",
      #  "Bacteria",
      #  "Bacteria",
      #  ...
    #]

@app.route('/metadata/<sample>')
def sample_metadata(sample):
    #save values that you need to a variable, to work with later
    selected=[samples_metadata.SAMPLEID,samples_metadata.ETHNICITY,samples_metadata.GENDER,
    samples_metadata.AGE,samples_metadata.LOCATION, samples_metadata.BBTYPE]
    results=session.query(*sel).filter(samples_metadata.SAMPLEID == sample[3:])
    
    #create empty dictionary
    sample_metadata={}
    #loop thru results and append to dictionary
    for result in results:
        #create a key value 'SAMPLEID' and it's value from results
        sample_metadata['SAMPLEID'] = results[0]
        sample_metadata['ETHNICITY'] = results[1]
        sample_metadata['GENDER'] = results[2]
        sample_metadata['AGE'] = results[3]
        sample_metadata['LOCATION'] = results[4]
        sample_metadata['BBTYPE'] = results[5]
    
    print(sample_metadata)
    return jsonify(sample_metadata)
    #Returns a json dictionary of sample metadata in the format

   # {
       # AGE: 24,
       # BBTYPE: "I",
       # ETHNICITY: "Caucasian",
       # GENDER: "F",
       # LOCATION: "Beaufort/NC",
       # SAMPLEID: 940
    #}
#@app.route('/wfreq/<sample>')
    #Weekly Washing Frequency as a number.

    #Args: Sample in the format: `BB_940`

    #Returns an integer value for the weekly washing frequency `WFREQ`

#@app.route('/samples/<sample>')
    #OTU IDs and Sample Values for a given sample.

    #Sort your Pandas DataFrame (OTU ID and Sample Value)
    #in Descending Order by Sample Value

   # Return a list of dictionaries containing sorted lists  for `otu_ids`
    #and `sample_values`


if __name__ == '__main__':
    app.run(debug=True)





