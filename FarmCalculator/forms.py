from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from FarmCalculator.models import User, Feed, CurrentValues, Movement
from FarmCalculator import db


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Имя пользователя уже занято')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Оставаться в системе')
    submit = SubmitField('Вход')


class CurrentValuesForm(FlaskForm):
    young = IntegerField('Молодняк', validators=[DataRequired()])
    adult = IntegerField('Взрослый', validators=[DataRequired()])
    old = IntegerField('Старый', validators=[DataRequired()])
    submit = SubmitField('Изменить')


class MoveForm(FlaskForm):
    feed_type = StringField('Тип корма', validators=[DataRequired()])
    amount = IntegerField('Кол-во корма (кг)', validators=[DataRequired()])
    date = DateField('Дата поступления')
    provider = StringField('Поставщик', validators=[DataRequired()])
    submit = SubmitField('Добавить')


# class GroupForm(FlaskForm):
#     group_number = StringField('Номер группы', validators=[DataRequired()])
#     file_name = FileField('Загрузить расписание',
#                           validators=[DataRequired(), FileAllowed(['pdf'])])
#     submit = SubmitField('Добавить расписание')
