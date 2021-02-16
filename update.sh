#/bin/bash -e
git pull
python3 fetch.py
#python3 fetch_ESR.py
python3 fetch_cases_by_DHB.py
git -c user.name="nz-covid-bot" -c user.email="ubuntu@elevation.auckland-cer.cloud.edu.au" commit -am "auto update to $(cat last_modified.txt)"
git push
