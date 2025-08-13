from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

foodinfluencer = Blueprint('foodinfluencer', __name__)

# Food Influencer User Story 1: 
# Tiffany wants to be able to gain followers, and track her follower list
# localhost:4000/fi/<username>/followers
@foodinfluencer.route('/<username>/followers', methods=['GET'])
def get_followers(username):
    cursor = db.get_db().cursor()
    
    # Check if the user exists
    check_user_query = '''
        SELECT 1 FROM Influencer WHERE Username = %s;
    '''
    cursor.execute(check_user_query, (username,))
    user_exists = cursor.fetchone()

    if not user_exists:
        return jsonify({"error": "User not found"}), 404

    the_query = '''
    SELECT U.FirstName, U.LastName, U.Username
    FROM Follow F
    JOIN CasualDiner CD ON F.CDId = CD.CDId
    JOIN Users U ON U.UserId = CD.CDId
    WHERE F.InfId = (
    SELECT InfId FROM Influencer WHERE Username = %s)
    '''

    cursor.execute(the_query, (username,))
    theData = cursor.fetchall()
    if not theData:
        return jsonify({"message": "No follower found for this username"}), 200

    return jsonify(theData), 200