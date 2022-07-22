# ensure dependencies are installed and ready to go
./install_deps.sh

cd ..

# Clean out any pycache files to prevent their inclusion
rm -r **/__pycache__

# Build deployment archive
zip -9 -r anki-card-builder.ankiaddon \
    *.py \
    manifest.json \
    ui/*.py \
    assets/* \
    site-packages