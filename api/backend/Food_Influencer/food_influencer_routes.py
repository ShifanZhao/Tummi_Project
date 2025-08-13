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
    
    # Check if cuisine exists
    cursor.execute("SELECT * FROM Restaurant WHERE Cuisine = %s", (cuisine,))
    if not cursor.fetchone():
        return jsonify({"error": "Cuisine not found"}), 404
    
    the_query = '''
    SELECT IP.PostId, IP.Likes, IP.Bookmark, IP.Share, R.Cuisine, R.RestName
    FROM InfPost IP
    JOIN Influencer I ON IP.InfId = I.InfId
    JOIN RestaurantLists RL ON RL.InfId = I.InfId
    JOIN ListedRest LR ON RL.RestListID = LR.RestListId
    JOIN Restaurant R ON R.RestId = LR.RestId
    WHERE I.Username = %s AND R.Cuisine = %s
    '''

    cursor.execute(the_query, (influ_username, cuisine))
    posts = cursor.fetchall()
    
    if not posts:
        return jsonify({"message": "No posts found for this influencer"}), 200

    return jsonify(posts), 200

# User Story 4: Tiffany wants to be able to make and save lists of restaurants 
# she has been to, so she and her followers can easily find and view certain dishes, 
# even if she posted them a long time ago
# localhost:4000/fi/<influ_username>/add_restaurant
@foodinfluencer.route('/<influ_username>/add_restaurant', methods=['POST'])
def add_restaurant_to_list(influ_username):
    cursor = db.get_db().cursor()
    
    # Check if influencer exists
    cursor.execute("SELECT * FROM Influencer WHERE Username = %s", (influ_username,))
    if not cursor.fetchone():
        return jsonify({"error": "Influencer not found"}), 404

    data = request.get_json()
    required_fields = ['RestListId', 'RestId']
    for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400


    the_query = '''
    INSERT INTO ListedRest (RestListId, RestId)
    VALUES (%s, %s)
    '''
    cursor.execute(
        the_query,
        (
            data['RestListId'],
            data['RestId'],
        ),
    )
    
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Restaurant added to list successfully"}), 201

# localhost:4000/fi/<int:influ_id>/restautant_list
@foodinfluencer.route('/<int:influ_id>/restautant_list', methods=['GET'])
def get_restaurant_list(influ_id):
    cursor = db.get_db().cursor()

    # Check if influencer exists
    cursor.execute("SELECT * FROM Influencer WHERE InfId = %s", (influ_id,))
    if not cursor.fetchone():
        return jsonify({"error": "Influencer not found"}), 404

    the_query = '''
    SELECT RL.RestListName, R.RestName, R.Cuisine, R.Location
    FROM RestaurantLists RL
    JOIN ListedRest LR ON RL.RestListID = LR.RestListId
    JOIN Restaurant R ON R.RestId = LR.RestId
    WHERE RL.InfId = %s
    '''

    cursor.execute(the_query, (influ_id,))
    restaurants = cursor.fetchall()
    
    if not restaurants:
        return jsonify({"message": "No restaurants found for this influencer"}), 200

    return jsonify(restaurants), 200

# User Story 5: Tiffany wants to be able to see restaurant owners' contact information 
# to easily reach out and form future partnerships
# localhost:4000/fi/restowner_info
@foodinfluencer.route('/restowner_info', methods=['GET'])
def get_restowner_info():
    cursor = db.get_db().cursor()

    the_query = '''
    SELECT RO.OwnerFName,
    RO.OwnerLName,
    R.RestName,
    R.Location,
    R.Cuisine
    FROM RestaurantOwner RO
    JOIN Restaurant R ON RO.RestId = R.RestId;

    '''

    cursor.execute(the_query)
    owners = cursor.fetchall()
    return jsonify(owners), 200

# User Story 6: Tiffany wants to be able to be sponsored by restaurants, 
# see pricing, revenue, profits, and make her post as a sponsored post
# localhost:4000/fi/<int:post_id>/<username>/sponsored
@foodinfluencer.route('/<int:post_id>/<username>/sponsored', methods=['PUT'])
def update_sponsored(post_id, username):
    cursor = db.get_db().cursor()
    
    the_query ='''
    UPDATE InfPost
    SET Sponsored = TRUE
    WHERE PostId = %s
    AND InfId = (
    SELECT InfId FROM Influencer WHERE Username = %s
    )
'''
    cursor.execute(the_query, (post_id, username))

    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Post marked as sponsored successfully"}), 200

@foodinfluencer.route('/influ_posts/<int:postid>', methods=['PUT'])
def like_post(postid):
    current_app.logger.info('PUT /influ_posts/<postid> route')

    the_query = 'UPDATE InfPost SET likes = (likes + 1) WHERE PostId = %s'
    data = (postid,)
    cursor = db.get_db().cursor()
    r = cursor.execute(the_query, data)
    db.get_db().commit()
    return 'Likes updated!'


## Create a comment on a cdpost
@foodinfluencer.route("/createcomment", methods=["POST"])
def create_comment():
    cursor = db.get_db().cursor()
    data = request.get_json()

    # Validate required fields
    required_fields = ["Comment"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Insert new Post
    query = """
    INSERT INTO Comment (Comment, CDPostId, InfPostId)
    VALUES (%s, %s, %s)
    """
    cursor.execute(
        query,
        (
            data["Comment"],
            data.get("CDPostId", None),   
            data.get("InfPostId", None)
        ),
    )

    db.get_db().commit()
    new_comment_id = cursor.lastrowid
    cursor.close()

    return (
        jsonify({"message": "Comment created successfully", "CommentId": new_comment_id}),
        201,
    )