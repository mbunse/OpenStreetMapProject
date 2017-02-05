# OpenStreetMap Project

The main project file is [UND_Project_3.html](https://rawgit.com/mbunse/OpenStreetMapProject/master/UND_Project_3.html).

Auditing of data is performed by: 
```
> python audit.py
```
Two output files will be produced. `investigate_result.txt` shows the XML tree elements for some specified elements (see `INVESTIGATE_STREET`, `INVESTIGATE_HOUSENUMBER` and `INVESTIGATE_AMENITY`). The other file produced is `audit_result.txt`. This file lists all entries deviating from the expectated patterns. This file comes with a `update_tag` function, that updates XML elements according to the findings in the audit phase which ar kept in dictionaries (see `MAPPING` `MAPPING_HOUSENUMBER`, `MAPPING_AMENITY`).

At first, convert osm to json using:
```
> python import_data.py
```
An file `schwabach.osm.json` will be created.

Then, import the json file to MongoDB:
```
> mongoimport.exe /file:schwabach.osm.json /d osm /c schwabach
```

Or in PowerShell:
```
> & 'C:\Program Files\MongoDB\Server\3.4\bin\mongoimport.exe' "/file:schwabach.osm.json" "/d osm" "/c schwabach"
```

To run the analysis code open the jupyter notebook `UND - Project 3.ipynb`.

To delete the collection form the database, start mongo and enter:
```
db.schwabach.remove({})
```

