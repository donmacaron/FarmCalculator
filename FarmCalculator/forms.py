from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from FarmCalculator.models import User, Feed, CurrentValues, Movement
from FarmCalculator import db


# def group_list():
#     return db.session.query(Group).all()


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


# class GroupForm(FlaskForm):
#     group_number = StringField('Номер группы', validators=[DataRequired()])
#     file_name = FileField('Загрузить расписание',
#                           validators=[DataRequired(), FileAllowed(['pdf'])])
#     submit = SubmitField('Добавить расписание')
