from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, \
    SelectField, FloatField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=4, max=25)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Введите корректный email адрес')
    ])
    first_name = StringField('Имя', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    last_name = StringField('Фамилия', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6, message='Пароль должен быть не менее 6 символов')
    ])
    confirm_password = PasswordField('Повторите пароль', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')

class DeviceForm(FlaskForm):
    serial_number = StringField('Серийный номер', validators=[DataRequired()])
    model_name = StringField('Модель', validators=[DataRequired()])
    device_type = SelectField('Тип устройства', coerce=int)
    submit = SubmitField('Добавить')

class FaultReportForm(FlaskForm):
    device = SelectField('Устройство', coerce=int)
    failure_description = TextAreaField('Описание отказа', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

class RepairForm(FlaskForm):
    device = SelectField('Устройство', coerce=int)
    fault_report = SelectField('Отчет об отказе', coerce=int)
    repair_description = TextAreaField('Описание ремонта', validators=[DataRequired()])
    repair_cost = FloatField('Стоимость ремонта')
    submit = SubmitField('Сохранить')

class RepairForm(FlaskForm):
    device = SelectField('Устройство', coerce=int, validators=[DataRequired()])
    fault_report = SelectField('Отчет об отказе', coerce=int)
    repair_description = TextAreaField('Описание ремонта', validators=[DataRequired()])
    repair_cost = FloatField('Стоимость ремонта', validators=[DataRequired()])
    submit = SubmitField('Сохранить')