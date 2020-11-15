#/bin/bash -e
git pull
python3 fetch.py
python3 fetch_ESR.py
python3 fetch_cases_by_DHB.py
git commit -am "auto update to $(cat last_modified.txt)"
git push
