from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    name = StringField('Nama Produk')
    capacity = StringField('Kapasitas')
    screen = StringField('Layar')
    chip = StringField('Chip')
    camera = StringField('Kamera')
    submit = SubmitField('Search')

class StockForm(FlaskForm):
    name = StringField('Nama Produk', validators=[DataRequired()])
    capacity = StringField('Kapasitas', validators=[DataRequired()])
    screen = StringField('Layar', validators=[DataRequired()])
    chip = StringField('Chip', validators=[DataRequired()])
    camera = StringField('Kamera', validators=[DataRequired()])
    submit = SubmitField('Simpan')
