#/bin/bash -e
git pull
./fetch.py
git commit -am "auto update from $(basename $(cat last_link.txt))"
git push
