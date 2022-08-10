VERSION=$(./python_version.sh)
# echo "$VERSION"

cd ..

python -m venv env
source env/bin/activate

pip install -r requirements.txt

# TODO: find a better way to get the python version from the virtual env
rm -rf site-packages
mkdir site-packages
cp -r env/lib/python$VERSION/site-packages/* site-packages