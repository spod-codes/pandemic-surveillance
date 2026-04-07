from flask import Blueprint, jsonify
from models import db, Report
from sqlalchemy import func

api_bp = Blueprint('api', __name__)

@api_bp.route('/stats')
def stats():
    total = Report.query.count()
    return jsonify({"total_reports": total})

@api_bp.route('/reports/by-disease')
def by_disease():
    stats = db.session.query(
        Report.disease, 
        func.count(Report.id)
    ).group_by(Report.disease).all()
    
    return jsonify({
        "labels": [row[0] for row in stats],
        "data": [row[1] for row in stats]
    })

@api_bp.route('/reports/by-location')
def by_location():
    stats = db.session.query(
        Report.location_city,
        func.avg(Report.latitude),
        func.avg(Report.longitude),
        func.count(Report.id)
    ).group_by(Report.location_city).filter(Report.location_city != None).all()
    
    return jsonify({
        "labels": [row[0] or 'Unknown' for row in stats],
        "latitudes": [row[1] for row in stats],
        "longitudes": [row[2] for row in stats],
        "data": [row[3] for row in stats]
    })
