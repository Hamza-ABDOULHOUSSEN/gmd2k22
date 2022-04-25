from wtforms import Form, StringField, IntegerField, SelectField
from wtforms.validators import input_required

## EXEMPLE FOR DRUGBANK QUERY
class FormQuery(Form):
    query = StringField(id="insert your symptom", validators=[input_required()])