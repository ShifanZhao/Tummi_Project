########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
casualdiner = Blueprint('casualdiner', __name__)

#------------------------------------------------------------
# Get all Casual Diners from the system
@casualdiner.route('/casualdiner', methods=['GET'])
def get_casualdiner():

    cursor = db.get_db().cursor()
    the_query = '''SELECT CDId, Location 
    FROM CasualDiner'''
    cursor.execute(the_query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
