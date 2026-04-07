from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Report, Disease
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.report_date.desc()).all()
    return render_template('dashboard.html', reports=reports)

@main_bp.route('/report/new', methods=['GET', 'POST'])
@login_required
def new_report():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        disease_name = request.form.get('disease')
        symptoms = request.form.get('symptoms')
        severity = request.form.get('severity')
        location_city = request.form.get('location_city')
        location_state = request.form.get('location_state')
        location_country = request.form.get('location_country', 'India')

        report = Report(
            user_id=current_user.id,
            patient_name=patient_name,
            age=age,
            disease=disease_name,
            symptoms=symptoms,
            severity=severity,
            location_city=location_city,
            location_state=location_state,
            location_country=location_country,
            report_date=datetime.utcnow().date()
        )
        db.session.add(report)
        db.session.commit()
        flash('Report submitted successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    diseases = Disease.query.all()
    return render_template('report_form.html', diseases=diseases, report=None)

@main_bp.route('/report/<int:id>')
@login_required
def view_report(id):
    report = Report.query.get_or_404(id)
    if report.user_id != current_user.id and not current_user.is_admin():
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.dashboard'))
    return render_template('report_detail.html', report=report)

@main_bp.route('/map')
def view_map():
    return render_template('map.html')
