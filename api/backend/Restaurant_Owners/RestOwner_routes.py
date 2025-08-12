from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

restowners = Blueprint('restowners', __name__)

@restowners.route('/restowners', methods=['GET'])
def get_all_restowners():
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT OwnerId, OwnerFName, OwnerLName
    FROM RestaurantOwner
    '''

    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response