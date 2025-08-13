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



# Get all posts associated with CD (1 or 5),
#followeeid is the ID of the user, seeing all posts made by people they follow
@casualdiner.route('/CDPost/<followeeid>', methods=['GET'])
def get_cdposts(followeeid):

    cursor = db.get_db().cursor()

    the_query = '''SELECT cdp.PostId, cdp.CDId, cdp.Likes, cdp.Caption, cdp.rating, cdp.share, cdp.bookmark
FROM CDPost cdp
         JOIN CasualDiner cd ON cd.CDId = cdp.CDId
         JOIN Following f ON f.FollowerId = cd.CDId
WHERE f.followeeID = %s;'''
    cursor.execute(the_query, (followeeid,))

    theData = cursor.fetchall()

    if not theData:
            return jsonify({"Sadly": "No Posts Here"}), 200
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Get all bookmarks associated with CD (1 or 5),
#followeeid is the ID of the user, seeing all posts made by people they follow
@casualdiner.route('/Bookmark/<userid>', methods=['GET'])
def get_cdbookmarks(userid):

    cursor = db.get_db().cursor()

    the_query = '''SELECT b.Restaurant
FROM Bookmark b
WHERE b.CDId = %s;'''
    cursor.execute(the_query, (userid,))

    theData = cursor.fetchall()

    if not theData:
            return jsonify({"Sadly": "No Bookmarks Here"}), 200
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


@casualdiner.route('/CDPost', methods=['PUT'])
def like_post():
    current_app.logger.info('PUT /CDPost route')
    cdpost_info = request.json
    PostId = cdpost_info['PostId']

    the_query = 'UPDATE CDPost SET likes = (likes + 1) WHERE PostId = %s'
    data = (PostId)
    cursor = db.get_db().cursor()
    r = cursor.execute(the_query, data)
    db.get_db().commit()
    return 'Likes updated!'

# http://localhost:4000/cd/1/createpost
# {"Rating": 8.9, "Caption":"tasty asl",  "RestId": 1}
# Create a new Post
@casualdiner.route("/<int:userid>/createpost", methods=["POST"])
def create_cdpost(userid):
    cursor = db.get_db().cursor()
    data = request.get_json()

    # Validate required fields
    required_fields = ["Rating", "Caption", "RestId"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400


    # Insert new Post
    query = """
    INSERT INTO CDPost (Rating, Caption, RestId, CDId)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (
            data["Rating"],
            data["Caption"],
            data["RestId"],
            userid
        ),
    )

    db.get_db().commit()
    new_cdpost_id = cursor.lastrowid
    cursor.close()

    return (
        jsonify({"message": "Post created successfully", "cdpostid": new_cdpost_id}),
        201,
    )


## Create a comment on a cdpost
@casualdiner.route("/createcomment", methods=["POST"])
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


## Create Bookmark for a user
@casualdiner.route("/createbm/<int:cdid>", methods=["POST"])
def create_bookmark(cdid):
    cursor = db.get_db().cursor()
    data = request.get_json()

    # Validate required fields
    required_fields = ["rest"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Insert new Post
    query = """
    INSERT INTO Bookmark (CDId, Restaurant)
    VALUES (%s, %s)
    """
    cursor.execute(
        query,
        (
            cdid,
            data["rest"]
        ),
    )

    db.get_db().commit()
    new_comment_id = cursor.lastrowid
    cursor.close()

    return (
        jsonify({"message": "Bookmark created successfully", "Bookmark": new_comment_id}),
        201,
    )



## Create a following instance between 2 user
@casualdiner.route("/createfollow", methods=["POST"])
def create_follow():
    cursor = db.get_db().cursor()
    data = request.get_json()

    # Validate required fields
    required_fields = ["followerid", "followeeid"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # If the folloewing already exists, say already exists
    check_follow_query = '''
        SELECT * FROM Following f WHERE (FollowerId = %s AND FolloweeId = %s);
    '''
    cursor.execute(check_follow_query, (data["followerid"], data["followeeid"]),)
    follow_exists = cursor.fetchone()
    
    if follow_exists:
        return jsonify({"error": "Already follow"}), 200


    # Insert new Post
    query = """
    INSERT INTO Following (FollowerId, FolloweeId)
    VALUES (%s, %s)
    """
    cursor.execute(
        query,
        (
            data["followerid"],
            data["followeeid"]
        ),
    )

    db.get_db().commit()
    new_comment_id = cursor.lastrowid
    cursor.close()

    return (
        jsonify({"message": "Following created successfully", "Follow": new_comment_id}),
        201,
    )


## Create a following instance between user and influencer
@casualdiner.route("/inf_follow", methods=["POST"])
def inf_follow():
    cursor = db.get_db().cursor()
    data = request.get_json()

    # Validate required fields
    required_fields = ["CDId", "InfId"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # If the folloewing already exists, say already exists
    check_follow_query = '''
        SELECT * FROM Follow f WHERE (CDId = %s AND InfId = %s);
    '''
    cursor.execute(check_follow_query, (data["CDId"], data["InfId"]),)
    follow_exists = cursor.fetchone()
    
    if follow_exists:
        return jsonify({"error": "Already follow"}), 200


    # Insert new Post
    query = """
    INSERT INTO Follow (CDId, InfId)
    VALUES (%s, %s)
    """
    cursor.execute(
        query,
        (
            data["CDId"],
            data["InfId"]
        ),
    )

    db.get_db().commit()
    new_comment_id = cursor.lastrowid
    cursor.close()

    return (
        jsonify({"message": "Following created successfully", "Follow": new_comment_id}),
        201,
    )

