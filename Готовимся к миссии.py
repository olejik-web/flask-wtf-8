from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from PIL import Image
from io import BytesIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
inx = 0
slider_images = []

class LoginForm(FlaskForm):
    username = StringField('id астронавта', validators=[DataRequired()])
    password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_name = StringField('id капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/index/<name>')
def index(name):
    return render_template('base.html', title=name)


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<list>')
def list_prof(list):
    return render_template('list_prof.html', list=list)


@app.route('/auto_answer')
@app.route('/answer')
def answer():
    dictt = {
        'title': 'Анкета О. Е.',
        'surname': 'Еремичев',
        'name': 'Олег',
        'education': 'выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': 'True'
    }
    return render_template('auto_answer.html', dict=dictt, title=dictt['title'])


@app.route('/distribution')
def distribution():
    return render_template('distribution.html')


@app.route('/table/<sex>/<age>')
def table(sex, age):
    if sex == 'male':
        color = (100, (int(age) + 100) % 256, 10)
    else:
        color = (180, (int(age) + 200) % 256, 10)
    return render_template('table.html', color='rgb{}'.format(str(color)), 
                           age=int(age))


@app.route('/carousel', methods=['POST', 'GET'])
def carousel():
    global inx
    if request.method == 'GET':
        return render_template('carousel.html', title='Карусель', inx=inx)
    elif request.method == 'POST':
        f = request.files['file']
        if f:
            inx += 1            
            im = Image.open(BytesIO(f.read()))
            path = 'static/img/slider/slider_image{}.png'.format(inx)
            im.save(path)
        return redirect('/carousel')
        

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')