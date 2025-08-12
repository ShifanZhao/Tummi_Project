########################################################
# Sample Internal Analyst blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db 

internal = Blueprint('internal', __name__)

@internal.route('/internal', methods=['GET'])
def get_internal():
    
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT *
        FROM CasualDiner
    '''
    cursor.execute(the_query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response
    
