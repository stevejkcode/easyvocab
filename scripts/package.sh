# ensure dependencies are installed and ready to go
./install_deps.sh

cd ..

# Clean out any pycache files to prevent their inclusion
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

# Build deployment archive
zip -9 -r easyvocab.ankiaddon \
    *.py \
    src/*.py \
    manifest.json \
    src/ui/*.py \
    src/assets/* \
    site-packages