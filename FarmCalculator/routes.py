import os
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from FarmCalculator import app, bcrypt, db
from FarmCalculator.models import User, Feed, CurrentValues, Movement
from FarmCalculator.forms import RegistrationForm, LoginForm

show_diagrams = False
ALLOWED_EXTENSIONS = set(['pdf'])


# Creating dict from db data
# def show_groups():
#     groups = [item.group_number for item in Group.query.all()]
#     files = [item.file for item in Group.query.all()]
#     print(groups)
#     print(files)
#     a = {item.group_number: item.file for item in Group.query.all()}
#     print(a)
#     return a

@app.route('/', methods=['GET', 'POST'])
def front_page():
    title = 'Farm Calculator'
    print('Front Page was loaded SUCCESSFULY')
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('Пользователь несуществует', 'danger')
        else:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home_page'))
            else:
                flash('Неправильный логин или пароль', 'danger')
    return render_template('front_page.html', title=title, form=form, front=True)


@app.route('/change_password')
def change_password():
    form = LoginForm()
    title = 'Farm Calculator - Смена пароля'
    return render_template('change_pass.html', title=title, front=True, form=form)


@app.route('/home')
@login_required
def home_page():
    title = 'Farm Calculator - Главная'
    feed = [item for item in Feed.query.all()]

    return render_template('home.html', title=title, feed=feed)


@app.route('/register', methods=['GET', 'POST'])
# @login_required
def register_page():
    title = 'Farm Calculator - Регистрация'
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Аккаунт создан', 'success')
        return redirect(url_for('home_page'))
    return render_template('register.html', title=title, form=form)


@app.route('/logout')
def logout_page():
    flash('Вы успешно вышли из учётной записи', 'info')
    logout_user()
    return redirect(url_for('front_page'))


# APP PAGES
@app.route('/order_graph')
@login_required
def order_graph():
    title = 'График заказов'
    feed = [item for item in Feed.query.all()]
    return render_template('order_graphs/order_graph.html', title=title, feed=feed)


@app.route('/current_values')
@login_required
def current_values():
    title = 'Текущие значения'
    cur_val = [item for item in CurrentValues.query.all()]
    return render_template('order_graphs/current_values.html', title=title, cur_val=cur_val)


@app.route('/receits')
@login_required
def receits():
    title = 'Поступления'
    # feed = [item for item in Feed.query.all()]
    movs = [item for item in Movement.query.all() if item.type == 'Receits']
    return render_template('order_graphs/receits.html', title=title, movs=movs)


@app.route('/transfers')
@login_required
def transfers():
    title = 'Перемещения'
    movs = [item for item in Movement.query.all() if item.type == 'Transfer']
    return render_template('order_graphs/transfers.html', title=title, movs=movs)


@app.route('/docs')
@login_required
def docs():
    title = 'Документы'
    return render_template('docs/docs.html', title=title)


@app.route('/docs/receits')
@login_required
def docs_receits():
    title = 'Документы - Поступления'
    return render_template('docs/receits.html', title=title)


@app.route('/docs/transfers')
@login_required
def docs_transfers():
    title = 'Документы - Перемещения'
    return render_template('docs/transfers.html', title=title)
