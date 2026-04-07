from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models import db, User, Report, Disease, AlertThreshold, AuditLog
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def log_audit_action(action, target_table, target_id, details):
    log = AuditLog(
        admin_id=current_user.id,
        action=action,
        target_table=target_table,
        target_id=target_id,
        details=details
    )
    db.session.add(log)
    db.session.commit()

@admin_bp.route('/')
@admin_required
def dashboard():
    total_users = User.query.count()
    total_reports = Report.query.count()
    pending_reports = Report.query.filter_by(status='pending').count()
    total_diseases = Disease.query.count()
    
    return render_template('admin/dashboard.html', 
                           total_users=total_users, 
                           total_reports=total_reports, 
                           pending_reports=pending_reports,
                           total_diseases=total_diseases)

@admin_bp.route('/reports')
@admin_required
def reports():
    reports = Report.query.order_by(Report.report_date.desc()).all()
    return render_template('admin/reports.html', reports=reports)


@admin_bp.route('/report/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_report(id):
    report = Report.query.get_or_404(id)
    if request.method == 'POST':
        # Update fields
        old_status = report.status
        report.patient_name = request.form.get('patient_name')
        report.age = request.form.get('age')
        report.disease = request.form.get('disease')
        report.symptoms = request.form.get('symptoms')
        report.severity = request.form.get('severity')
        report.location_city = request.form.get('location_city')
        report.location_state = request.form.get('location_state')
        report.status = request.form.get('status')
        report.notes = request.form.get('notes')
        report.updated_at = datetime.utcnow()
        db.session.commit()
        
        details = f"Updated report status from {old_status} to {report.status}. Severity: {report.severity}"
        log_audit_action('UPDATE', 'reports', report.id, details)
        
        flash('Report updated successfully.', 'success')
        return redirect(url_for('admin.reports'))
    
    diseases = Disease.query.all()
    return render_template('admin/report_edit.html', report=report, diseases=diseases)

@admin_bp.route('/report/<int:id>/delete', methods=['POST'])
@admin_required
def delete_report(id):
    report = Report.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    
    log_audit_action('DELETE', 'reports', id, f"Deleted report for {report.disease} in {report.location_city}")
    flash('Report deleted.', 'info')
    return redirect(url_for('admin.reports'))

@admin_bp.route('/users')
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/diseases')
@admin_required
def diseases():
    diseases = Disease.query.all()
    return render_template('admin/diseases.html', diseases=diseases)

@admin_bp.route('/alerts')
@admin_required
def alerts():
    alerts = AlertThreshold.query.all()
    return render_template('admin/alerts.html', alerts=alerts)

@admin_bp.route('/audit')
@admin_required
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('admin/audit.html', logs=logs)

# Add CSV Export placeholder
@admin_bp.route('/export')
@admin_required
def export_csv():
    # Will implement full CSV export later
    flash('Export started', 'info')
    return redirect(url_for('admin.reports'))
