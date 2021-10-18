#/bin/bash -e
git pull
python3 fetch.py
#python3 fetch_ESR.py
python3 fetch_cases_by_DHB.py
python3 fetch_vaccinations.py
python3 fetch_healthpoint.py
python3 fetch_bookmyvaccine.py
python3 csv_to_geojson.py
git commit -am "auto update to $(cat last_modified.txt)" --author="nz-covid-bot <ubuntu@elevation.auckland-cer.cloud.edu.au"
git push
