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

# Food Influencer User Story 2:Tiffany wants to see analytics like follower count, saves,
# shares, and engagement per review, so that she can understand what works and pitch better
# to sponsors or brands.
# localhost:4000/fi/<int:influ_id>/analytics
@foodinfluencer.route('/<int:influ_id>/analytics', methods=['GET'])
def get_influ_analytics(influ_id):
    cursor = db.get_db().cursor()

    # Check if influencer exists
    cursor.execute("SELECT * FROM Influencer WHERE InfId = %s", (influ_id,))
    if not cursor.fetchone():
        return jsonify({"error": "Influencer not found"}), 404

    cursor.execute('SELECT COUNT(*) AS FollowerCount FROM Follow WHERE InfId = %s', (influ_id,))
    follower_count = cursor.fetchone()

    the_query = '''
    SELECT
    P.PostId,
    P.Likes,
    P.Bookmark AS Saves,
    P.Share,
    (P.Likes + P.Bookmark + P.Share) AS TotalEngagement
    FROM InfPost P
    WHERE P.InfId = %s
    '''
    cursor.execute(the_query, (influ_id,))
    posts = cursor.fetchall()
    return jsonify({
        "FollowerCount": follower_count["FollowerCount"],
        "Posts": [dict(row) for row in posts]
    }), 200

# Food Influencer User Story 3: Tiffany needs her posts to be discoverable
# through filters like cuisine, so that users who share similar tastes on this
# food-specific platform can find and follow her easily
# localhost:4000/fi/influ_posts/<influ_username>/<cuisine>
@foodinfluencer.route('/influ_posts/<influ_username>/<cuisine>', methods=['GET'])
def get_influ_posts(influ_username, cuisine):
    cursor = db.get_db().cursor()

    # Check if influencer exists
    cursor.execute("SELECT * FROM Influencer WHERE Username = %s", (influ_username,))
    if not cursor.fetchone():
        return jsonify({"error": "Influencer not found"}), 404

    the_query = '''
    SELECT IP.PostId, IP.Likes, IP.Bookmark, IP.Share, R.Cuisine, R.RestName
    FROM InfPost IP
    JOIN Influencer I ON IP.InfId = I.InfId
    JOIN RestaurantLists RL ON RL.InfId = I.InfId
    JOIN Restaurant R ON RL.RestListID = RL.RestListID
    WHERE I.Username = %s AND R.Cuisine = %s;
    '''

    cursor.execute(the_query, (influ_username, cuisine))
    posts = cursor.fetchall()
    
    if not posts:
        return jsonify({"message": "No posts found for this influencer"}), 200

    return jsonify(posts), 200