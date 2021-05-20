import os
import datetime
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from FarmCalculator import app, bcrypt, db
from FarmCalculator.models import User, Feed, CurrentValues, Movement
from FarmCalculator.forms import RegistrationForm, LoginForm, CurrentValuesForm, MoveForm

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
    calculate()
    return render_template('home.html', title=title, feed=feed)


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/current_values', methods=['GET', 'POST'])
@login_required
def current_values():
    title = 'Текущие значения'
    cur_val = [item for item in CurrentValues.query.all()]
    form = CurrentValuesForm()
    if form.validate_on_submit():
        CurrentValues.query.get(1).amount = form.young.data
        CurrentValues.query.get(2).amount = form.adult.data
        CurrentValues.query.get(3).amount = form.old.data
        db.session.commit()
        flash('Текущие значения обновлены', 'success')
        return redirect(url_for('current_values'))
    return render_template('order_graphs/current_values.html', title=title, cur_val=cur_val, form=form)


@app.route('/receits', methods=['GET', 'POST'])
@login_required
def receits():
    title = 'Поступления'
    feed = [item.name for item in Feed.query.all()]
    movs = [item for item in Movement.query.all() if item.type == 'Receits']
    form = MoveForm()
    if form.validate_on_submit():
        if Movement.query.filter_by(feed_type=form.feed_type.data).filter_by(type='Receits').first():
            Movement.query.filter_by(feed_type=form.feed_type.data).filter_by(type='Receits').first().date=form.date.data
            Movement.query.filter_by(feed_type=form.feed_type.data).filter_by(type='Receits').first().amount=form.amount.data
            Movement.query.filter_by(feed_type=form.feed_type.data).filter_by(type='Receits').first().provider=provider=form.provider.data
            db.session.commit()
        db.session.commit()
        flash('Поступления добавлены', 'success')
        return redirect(url_for('receits'))
    return render_template('order_graphs/receits.html', title=title, feed=feed, movs=movs, form=form)


@app.route('/transfers', methods=['GET', 'POST'])
@login_required
def transfers():
    title = 'Перемещения'
    feed = [item.name for item in Feed.query.all()]
    movs = [item for item in Movement.query.all() if item.type == 'Transfers']
    form = MoveForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        if Movement.query.filter_by(feed_type=form.feed_type.data).filter_by(type='Transfers').first():
            Movement.query.filter_by(feed_type=form.feed_type.data).filter_by(type='Transfers').first().date=form.date.data
            Movement.query.filter_by(feed_type=form.feed_type.data).filter_by(type='Transfers').first().amount=form.amount.data
            Movement.query.filter_by(feed_type=form.feed_type.data).filter_by(type='Transfers').first().provider=provider=form.provider.data
            db.session.commit()
        flash('Перемещения добавлены', 'success')
        return redirect(url_for('transfers'))
    return render_template('order_graphs/transfers.html', title=title, feed=feed, movs=movs, form=form)


@app.route('/docs')
@login_required
def docs():
    title = 'Документы'
    return render_template('docs.html', title=title)


def calculate():
    all_stock = []
    for f in Feed.query.all():
        t = Movement.query.filter_by(feed_type=f.name).filter_by(type='Transfers').first().amount
        r = Movement.query.filter_by(feed_type=f.name).filter_by(type='Receits').first().amount
        young = CurrentValues.query.filter_by(rabbit_type='Молодняк').first().amount
        adult = CurrentValues.query.filter_by(rabbit_type='Взрослый').first().amount
        old = CurrentValues.query.filter_by(rabbit_type='Молодняк').first().amount
        f.amount = r - t
        f.stock = f.amount / 1200
        all_stock.append(f.stock)
    for f in Feed.query.all():
        f.quarter = ((young+adult+old)*1.2*(91-sum(all_stock)))/6
    db.session.commit()
