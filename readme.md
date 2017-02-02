# OpenStreetMap Project

At first, convert osm to json using:
`> python import_data.py`

Then, import the json file to MongoDB:
`> mongoimport.exe /file:schwabach.osm.json /d osm /c schwabach`

Or in PowerShell:
`> & 'C:\Program Files\MongoDB\Server\3.4\bin\mongoimport.exe' "/file:schwabach.osm.json" "/d osm" "/c schwabach"`

To delete the collection form the database, start mongo and enter:
`db.schwabach.remove({})`
