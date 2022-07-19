from aqt import mw

def query_existing_model(asset):
    model = mw.col.models.by_name(asset.name)

    return True if model else False

def add_fields(model, afields):
    for afield in afields:
        field = mw.col.models.new_field(afield)
        mw.col.models.add_field(model, field)

# Build the given template and attach it to the model
def build_template(model, atemplate):
    template = mw.col.models.new_template(atemplate['name'])
    template['qfmt'] = atemplate['qfmt']
    template['afmt'] = atemplate['afmt']
    mw.col.models.add_template(model, template)

# Build a new note model for a given asset if it doesn't already exist
def build_asset(asset):
    # Check if model already exists
    if query_existing_model(asset): return

    # Create a new card type
    model = mw.col.models.new('prettify-nord-basic-fl')

    # Add fields
    add_fields(model, asset.fields)

    # Add templates
    for template in asset.templates:
        build_template(model, template)

    # Add css
    model['css'] = asset.css

    mw.col.models.add_dict(model)