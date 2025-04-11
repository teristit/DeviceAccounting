from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

class Role(Enum):
    TESTER = 'tester'
    REPAIRER = 'repairer'
    ADMIN = 'admin'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.TESTER, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(255), nullable=True)  # Путь к изображению
    verified = db.Column(db.Boolean, default=False, nullable=False)  # Добавленное поле

    # Связи с другими моделями
    faults_reported = db.relationship('FaultReport', backref='reporter', lazy=True)
    repairs_made = db.relationship('Repair', backref='repairer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class DeviceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    devices = db.relationship('Device', back_populates='device_type')
    common_failures = db.relationship('CommonFailure', backref='device_type', lazy=True)

    def __repr__(self):
        return f'<DeviceType: {self.name}>'

class Device(db.Model):
    serial_number = db.Column(db.String(128), unique=True, nullable=False, index=True, primary_key=True)
    model_name = db.Column(db.String(64), nullable=True)
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    device_type = db.relationship('DeviceType', back_populates='devices')
    faults = db.relationship('FaultReport', backref='device', lazy=True)
    repairs = db.relationship('Repair', backref='device', lazy=True)
    def get_model_name(self):
        return f"{self.model_name}"
    def __repr__(self):
        return f'<Device: {self.serial_number} - {self.model_name}>'

class CommonFailure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    failure_name = db.Column(db.String(255), nullable=False)
    failure_description = db.Column(db.Text)
    possible_solutions = db.Column(db.Text)
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))

    def __repr__(self):
        return f'<CommonFailure: {self.failure_name}>'

class FaultReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.DateTime, default=datetime.utcnow)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    failure_description = db.Column(db.Text)
    predicted_replacement = db.Column(db.Text)
    repair = db.relationship('Repair', backref='fault_report', uselist=False, lazy=True)

    def __repr__(self):
        return f'<FaultReport for Device {self.device_id} on {self.report_date}>'

class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repair_date = db.Column(db.DateTime, default=datetime.utcnow)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    repairer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    repair_description = db.Column(db.Text)
    replaced_components = db.Column(db.Text)
    fault_report_id = db.Column(db.Integer, db.ForeignKey('fault_report.id'))

    def __repr__(self):
        return f'<Repair for Device {self.device_id} on {self.repair_date}>'
