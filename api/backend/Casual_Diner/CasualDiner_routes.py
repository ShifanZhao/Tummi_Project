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
    



# Get all posts associated with CD,
#followeeid is the ID of the user, seeing all posts made by people they follow
@casualdiner.route('/CDPost/<followeeid>', methods=['GET'])
def get_cdposts(followeeid):

    cursor = db.get_db().cursor()
    the_query = '''SELECT cdp.PostId, cdp.CDId, cdp.Likes, cdp.rating, cdp.share, cdp.bookmark
FROM CDPost cdp
         JOIN CasualDiner cd ON cd.CDId = cdp.CDId
         JOIN Following f ON f.FollowerId = cd.CDId
WHERE f.followeeID = %s;'''
    cursor.execute(the_query, (followeeid,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


