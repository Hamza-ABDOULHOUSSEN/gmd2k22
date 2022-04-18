from wtforms import Form, StringField, IntegerField, SelectField
from wtforms.validators import input_required

## EXEMPLE FOR DRUGBANK QUERY
class DrugbankFormQuery(Form):
    query = StringField(id="drugbank query", validators=[input_required()])