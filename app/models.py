# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from sqlalchemy.orm import validates
# from datetime import datetime
from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash


# db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)  # Имя
    last_name = db.Column(db.String(50), nullable=False)   # Фамилия
    password_hash = db.Column(db.String(255), nullable=False) # Пароль
    role = db.Column(db.String(10), default='user')  # Роль


    @validates('first_name', 'last_name')
    def validate_names(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError(f"{key} must be at least 2 characters long")
        return name.strip()

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DeviceType(db.Model):
    """
    Модель для представления типов устройств/плат.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    devices = db.relationship("Device", back_populates="device_type")
    common_failures = db.relationship("CommonFailure", back_populates="device_type") # Список частых ошибок, связанных с типом устройства

    def __repr__(self):
        return f'<DeviceType: {self.name}>'

class Device(db.Model):
    """
    Модель для представления информации об устройстве.  Вместо Device и Board теперь одна модель.
    """
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(128), unique=True, nullable=False, index=True)  # QR-код
    model_name = db.Column(db.String(64), nullable=False)
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))
    device_type = db.relationship("DeviceType", back_populates="devices")
    fault_reports = db.relationship('FaultReport', backref='device', lazy=True)
    repairs = db.relationship('Repair', backref='device', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Device: {self.serial_number} - {self.model_name}>'

class CommonFailure(db.Model):  # модель для частых ошибок
    """
    Модель для хранения описаний частых ошибок.
    """
    id = db.Column(db.Integer, primary_key=True)
    failure_name = db.Column(db.String(255), nullable=False)
    failure_description = db.Column(db.Text)
    possible_solutions = db.Column(db.Text)  # Возможные решения проблемы
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))
    device_type = db.relationship("DeviceType", back_populates="common_failures")

    def __repr__(self):
        return f'<CommonFailure: {self.failure_name}>'

class FaultReport(db.Model):
    """
    Модель для представления отчета об обнаруженном отказе.
    """
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.DateTime, default=datetime.utcnow)  # Дата автоматом
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    failure_description = db.Column(db.Text)
    predicted_replacement = db.Column(db.Text)
    repair_id = db.Column(db.Integer, db.ForeignKey('repair.id'), nullable=True) # Связь с ремонтом, если был создан

    def __repr__(self):
        return f'<FaultReport for Device {self.device_id} on {self.report_date}>'

class Repair(db.Model):
    """
    Модель для представления информации о ремонте.
    """
    id = db.Column(db.Integer, primary_key=True)
    repair_date = db.Column(db.DateTime, default=datetime.utcnow)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    repairer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    repair_description = db.Column(db.Text)
    repair_cost = db.Column(db.Float)
    #repairer_employee = db.relationship("user", back_populates="repairs")
    fault_report_id = db.Column(db.Integer, db.ForeignKey('fault_report.id'), nullable=True)  # Связь с отчетом об отказе
    fault_report = db.relationship("FaultReport", backref="repair")

    def __repr__(self):
        return f'<Repair for Device {self.device_id} on {self.repair_date}>'