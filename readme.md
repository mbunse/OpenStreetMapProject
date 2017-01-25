# OpenStreetMap Project

At first, convert osm to json using:
`> python import_data.py`

Then, import the json file to MongoDB:
`> mongoimport.exe /file:schwabach.osm.json /d osm /c schwabach`