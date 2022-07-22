cd ..

python -m venv env
source env/bin/activate

pip install -r requirements.txt

# TODO: find a better way to get the python version from the virtual env
mkdir site-packages
cp -r env/lib/python3.10/site-packages/* site-packages