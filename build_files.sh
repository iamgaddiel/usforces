sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
python -m pip install -U pip
pip install --upgrade setuptools 
pip install ez_setup
pip install -r requirements.txt
python3 manage.py collectstatic


