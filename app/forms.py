from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, \
    SelectField, FloatField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed

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
    model_name = StringField('Название', validators=[DataRequired()])
    device_type = SelectField('Тип устройства', coerce=int)
    submit = SubmitField('Добавить')

class TypeForm(FlaskForm):
    model_name = StringField('Название', validators=[DataRequired()])
    device_type = StringField('Модель', validators=[DataRequired()])
    common_failures = SelectField('Частые ошибки', choices=[])
    submit = SubmitField('Добавить')

class CommonFailures(FlaskForm):
    pass

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

class ProfileForm(FlaskForm):
    full_name = StringField('Полное имя')
    bio = TextAreaField('О себе')
    avatar = FileField('Аватар', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')
    ])
    submit = SubmitField('Обновить')
