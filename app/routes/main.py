from datetime import date
from flask import Blueprint, render_template
from ..models import Package, Schedule

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    packages = Package.query.all()
    upcoming_schedules = Schedule.query.filter(Schedule.tanggal >= date.today()).order_by(Schedule.tanggal.asc(), Schedule.jam_mulai.asc()).limit(6).all()
    return render_template('index.html', packages=packages, schedules=upcoming_schedules)
