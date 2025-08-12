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

    the_query = '''SELECT cdp.PostId, cdp.CDId, cdp.Likes, cdp.rating, cdp.share, cdp.bookmark
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

    the_query = '''select
   cdp.PostId,
   cdp.Likes,
   cdp.Rating,
   cd.Location as RestaurantName,
   cd.LastVisited,
   u.FirstName + ' ' + u.LastName as PostAuthor,
   u.Username as AuthorUsername
from Users u1
        join Bookmark b on u1.UserId = b.CDId
        join CDPost cdp on b.CDId = cdp.CDId
        join CasualDiner cd on cdp.CDId = cd.CDId
        join Users u on cd.CDId = u.UserId
where u1.UserId = %s
order by cd.LastVisited desc, cdp.Rating desc;'''
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
# Required fields: Name, Country, Founding_Year, Focus_Area, Website
# Example: POST /ngo/ngos with JSON body
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
        jsonify({"message": "NGO created successfully", "cdpostid": new_cdpost_id}),
        201,
    )


