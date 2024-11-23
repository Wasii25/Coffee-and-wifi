from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Regexp
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Regexp

def convert_to_emojis(count, emoji):
    return emoji * count


class CafeForm(FlaskForm):
    # Input Fields
    name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Cafe Location (URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time (e.g., 8:30)', validators=[
        DataRequired(),
        Regexp(r"^\d{1,2}:\d{2}$", message="Enter time in HH:MM format")
    ])
    close_time = StringField('Closing Time (e.g., 5:30)', validators=[
        DataRequired(),
        Regexp(r"^\d{1,2}:\d{2}$", message="Enter time in HH:MM format")
    ])

    # Ratings
    coffee = SelectField(
        'Coffee Rating',
        choices=[('1', '☕'), ('2', '☕☕'), ('3', '☕☕☕'), ('4', '☕☕☕☕'), ('5', '☕☕☕☕☕')],
        validators=[DataRequired()]
    )
    wifi = SelectField(
        'WiFi Rating',
        choices=[('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'), ('5', '💪💪💪💪💪')],
        validators=[DataRequired()]
    )
    power = SelectField(
        'Power Outlet Rating',
        choices=[('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌')],
        validators=[DataRequired()]
    )

    # Submit Button
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_data = form.data
        new_row = [value for (key, value) in new_data.items() if key not in ['submit', 'csrf_token']]

        # Open the file with UTF-8 encoding
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            wr = csv.writer(csv_file)
            wr.writerow(new_row)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        header_row = list_of_rows.pop(0)
    return render_template('cafes.html', cafes=list_of_rows, header_row=header_row)


if __name__ == '__main__':
    app.run(debug=True)
