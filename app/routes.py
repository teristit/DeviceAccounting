from sqlite3 import IntegrityError

from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models import User, Device, DeviceType, FaultReport, Repair, CommonFailure, Role, DeviceType
from app.forms import (LoginForm, RegistrationForm, DeviceForm, FaultReportForm, RepairForm, ProfileForm, TypeForm)
from .decorators import role_required, admin_required



bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index.html')

# Регистрация и аутентификация
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        # Ищем пользователя в базе данных
        user = User.query.filter_by(email=form.email.data).first()

        # Проверяем пароль
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('main.login'))

        # Аутентифицируем пользователя
        login_user(user, remember=form.remember_me.data)

        # Перенаправляем на запрошенную страницу или на главную
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))

    # Рендерим шаблон для GET запроса или невалидной формы
    return render_template('auth/login.html', title='Вход', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            patronymic=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('main.login'))

    # Добавьте этот return для GET-запросов
    return render_template('auth/register.html', title='Регистрация', form=form)
# Устройства
@bp.route('/devices')
@login_required
def device_list():
    devices = Device.query.all()
    return render_template('devices/list.html', devices=devices)

@bp.route('/device/add', methods=['GET', 'POST'])
@login_required
def add_device():
    form = DeviceForm()
    form.device_type.choices = [(t.id, t.name) for t in DeviceType.query.all()]
    if form.validate_on_submit():
        device = Device(
            serial_number=form.serial_number.data,
            model_name=form.model_name.data,
            device_type_id=form.device_type.data
        )
        db.session.add(device)
        db.session.commit()
        flash('Устройство добавлено')
        return redirect(url_for('main.device_list'))
    return render_template('devices/add.html', form=form)

@bp.route('/device/<int:id>')
def device_detail(id):
    device = Device.query.get_or_404(id)
    return render_template('devices/detail.html', device=device)

@bp.route('/type')
@login_required
def type_list():
    types = DeviceType.query.all()
    return render_template('type/list.html', types=types)
@bp.route('/type/<int:type_id>')
def show_type_detail(type_id):
    type = DeviceType.query.get_or_404(type_id)
    return render_template('type/detail.html', type=type)


#@bp.route('/type/add', methods=['GET', 'POST'])
#@login_required
#def add_type():
#    form = TypeForm()
#    if form.model_name.data and form.device_type.data:
#        types = DeviceType(
#            name=form.model_name.data,
#            common_failures=form.common_failures.data
#        )
#        db.session.add(types)
#        db.session.commit()
#        flash('Модель добавлена добавлено')
#        return redirect(url_for('main.type_list'))
#    return render_template('type/add.html', types=form)


@bp.route('/type/add', methods=['GET', 'POST'])
@login_required
def add_type():
    form = TypeForm()  # Создаем экземпляр формы

    # Для GET-запроса просто отображаем форму
    if request.method == 'GET':
        return render_template('type/add.html', form=form)  # Ключевое исправление

    # Для POST-запроса обрабатываем данные
    if form.model_name.data and form.device_type.data:
        try:
            print(1)
            if form.common_failures.data:
                new_type = DeviceType(
                    name=form.model_name.data,
                    common_failures=form.common_failures.data
                )
            else:
                new_type = DeviceType(
                    name=form.model_name.data
                )
            db.session.add(new_type)
            db.session.commit()
            flash('Тип устройства успешно добавлен', 'success')
            return redirect(url_for('main.type_list'))
        except IntegrityError:
            db.session.rollback()
            flash('Тип с таким названием уже существует', 'danger')

    return render_template('type/add.html', form=form)


# Отчеты об отказах
@bp.route('/faults')
@login_required
def fault_list():
    faults = FaultReport.query.order_by(FaultReport.report_date.desc()).all()
    return render_template('faults/list.html', faults=faults)

@bp.route('/fault/report', methods=['GET', 'POST'])
@login_required
def report_fault():
    form = FaultReportForm()
    if form.validate_on_submit():
        fault = FaultReport(
            device_id=form.device.data,
            reporter_id=current_user.id,
            failure_description=form.failure_description.data
        )
        db.session.add(fault)
        db.session.commit()
        flash('Отчет об отказе создан')
        return redirect(url_for('main.fault_list'))
    return render_template('faults/report.html', form=form)

# Ремонты
@bp.route('/repairs')
@login_required
def repair_list():
    repairs = Repair.query.order_by(Repair.repair_date.desc()).all()
    return render_template('repair/list.html', repairs=repairs)

@bp.route('/repair/add', methods=['GET', 'POST'])
@login_required
def add_repair():
    form = RepairForm()
    if form.validate_on_submit():
        repair = Repair(
            device_id=form.device.data,
            repairer_id=current_user.id,
            repair_description=form.repair_description.data,
            repair_cost=form.repair_cost.data,
            fault_report_id=form.fault_report.data
        )
        db.session.add(repair)
        db.session.commit()
        flash('Ремонт добавлен')
        return redirect(url_for('main.repair_list'))
    return render_template('repair/add.html', form=form)

@bp.route('/logout')
@login_required
def logout():  # Имя функции должно быть logout
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('main.login'))


@bp.route('/repairs')
@login_required
def repair_list_route():  # Изменили имя функции
    repairs = Repair.query.order_by(Repair.repair_date.desc()).all()
    return render_template('repairs/list.html', repairs=repairs)

@bp.route('/repair/add', methods=['GET', 'POST'])
@login_required
def add_repair_route():  # Изменили имя функции
    form = RepairForm()
    if form.validate_on_submit():
        repair = Repair(
            device_id=form.device.data,
            repairer_id=current_user.id,
            repair_description=form.repair_description.data,
            repair_cost=form.repair_cost.data,
            fault_report_id=form.fault_report.data
        )
        db.session.add(repair)
        db.session.commit()
        flash('Ремонт добавлен')
        return redirect(url_for('main.repair_list_route'))  # Обновили ссылку
    return render_template('repairs/add.html', form=form)

@bp.route('/users')
@login_required
def user_list():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('user/list.html', users=users)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = RepairForm()
    if form.validate_on_submit():
        repair = Repair(
            device_id=form.device.data,
            repairer_id=current_user.id,
            repair_description=form.repair_description.data,
            repair_cost=form.repair_cost.data,
            fault_report_id=form.fault_report.data
        )
        db.session.add(repair)
        db.session.commit()
        flash('Ремонт добавлен')
        return redirect(url_for('main.repair_list_route'))  # Обновили ссылку
    return render_template('user/add.html', form=form)

@bp.route('/users/<int:user_id>')
def edit_profile(user_id):
    type = DeviceType.query.get_or_404(user_id)
    return render_template('type/detail.html', type=type)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.bio = form.bio.data

        if form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.avatar.data.save(filepath)
            current_user.avatar = filename

        db.session.commit()
        flash('Профиль обновлен!', 'success')
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.bio.data = current_user.bio

    return render_template('profile.html', form=form)

@bp.route('/test_device/<int:device_id>', methods=['POST'])
@role_required(Role.TESTER)
def test_device(device_id):
    # Логика тестирования устройства
    pass

@bp.route('/repair_device/<int:device_id>', methods=['POST'])
@role_required(Role.REPAIRER)
def repair_device(device_id):
    # Логика ремонта устройства
    pass

@bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@bp.route('/admin')
@admin_required  # Теперь без скобок!
def admin_panel():
    return render_template('admin.html')