# ########################################################
# # Sample Internal Analyst blueprint of endpoints
# # Remove this file if you are not using it in your project
# ########################################################

# from flask import Blueprint
# from flask import request
# from flask import jsonify
# from flask import make_response
# from flask import current_app
# from backend.db_connection import db 

# internal = Blueprint('internal', __name__)

# @internal.route('/internal', methods=['GET'])
# def get_internal():
    
#     cursor = db.get_db().cursor()
#     the_query = '''
#         SELECT *
#         FROM CasualDiner
        
#     '''
#     cursor.execute(the_query)
    
#     theData = cursor.fetchall()
    
#     the_response = make_response(jsonify(theData))
#     the_response.status_code = 200
#     the_response.mimetype='application/json'
#     return the_response
    
    


from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

internal = Blueprint('internal', __name__)


# ------------------------------------------------------------------
# 目录页（方便在浏览器里点 /ita/internal 看所有可用端点）
# ------------------------------------------------------------------
@internal.route('/internal', methods=['GET'])
def internal_home():
    the_response = make_response(jsonify({
        "message": "Internal Analyst API",
        "try": [
            "/ita/returning",
            "/ita/features/usage",
            "/ita/requests/pending",
            "/ita/requests/details",
            "/ita/moderation/restaurants/flagged",
            "/ita/moderation/owners/flagged",
            "/ita/moderation/diners/flagged",
            "/ita/moderation/influencers/flagged",
            "/ita/dau"
        ]
    }))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# ------------------------------------------------------------------
# 3.1 see how many user is active (AppAnalytics）
# GET /ita/returning
# ------------------------------------------------------------------
@internal.route('/returning', methods=['GET'])
def get_returning_users():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT
            AA.UserId,
            COUNT(*)               AS session_count,
            MIN(AA.LastVisit)      AS first_visit,
            MAX(AA.LastVisit)      AS last_visit
        FROM AppAnalytics AA
        GROUP BY AA.UserId
        ORDER BY last_visit DESC
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Sessions Found"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# ------------------------------------------------------------------
# 3.2 Monitor usage of various functions（CDPost/InfPost 的 Bookmark/Share + Follow 量）
# GET /ita/features/usage
# ------------------------------------------------------------------
@internal.route('/features/usage', methods=['GET'])
def get_feature_usage():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT 'bookmark_cd'  AS feature, COALESCE(SUM(Bookmark), 0) AS usage_count
        FROM CDPost
        UNION ALL
        SELECT 'share_cd',    COALESCE(SUM(Share), 0)
        FROM CDPost
        UNION ALL
        SELECT 'bookmark_inf', COALESCE(SUM(Bookmark), 0)
        FROM InfPost
        UNION ALL
        SELECT 'share_inf',    COALESCE(SUM(Share), 0)
        FROM InfPost
        UNION ALL
        SELECT 'follow',       COUNT(*)
        FROM `Follow`
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Feature Usage Yet"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# ------------------------------------------------------------------
# 3.3 List of new restaurant requests awaiting approval（Restaurant.`Add` = TRUE）
# GET /ita/requests/pending
# ------------------------------------------------------------------
@internal.route('/requests/pending', methods=['GET'])
def get_pending_requests():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT
            R.RestId,
            R.RestName,
            R.UserId
        FROM Restaurant R
        WHERE R.`Add` = TRUE
        ORDER BY R.RestId
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Requests Here"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# ------------------------------------------------------------------
# 3.4 Pending request details (including initiator Username）
# GET /ita/requests/details
# ------------------------------------------------------------------
@internal.route('/requests/details', methods=['GET'])
def get_request_details():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT
            R.RestId,
            R.RestName,
            R.Location,
            R.Cuisine,
            R.Rating,
            R.NumSaves,
            R.NumVisits,
            U.Username AS requester
        FROM Restaurant AS R
        JOIN Users      AS U
             ON R.UserId = U.UserId
        WHERE R.`Add` = TRUE
        ORDER BY R.RestId
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Pending Details"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# ------------------------------------------------------------------
# 3.5 List of inappropriate content (four lists)
# GET /ita/moderation/restaurants/flagged
# ------------------------------------------------------------------
@internal.route('/moderation/restaurants/flagged', methods=['GET'])
def list_flagged_restaurants():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT RestId, RestName
        FROM Restaurant
        WHERE Flag = TRUE
        ORDER BY RestId DESC
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Flagged Restaurants"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# GET /ita/moderation/owners/flagged
@internal.route('/moderation/owners/flagged', methods=['GET'])
def list_flagged_owners():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT RO.OwnerId, RO.OwnerFName, RO.OwnerLName
        FROM RestaurantOwner RO
        WHERE RO.Flagged = TRUE
        ORDER BY RO.OwnerId DESC
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Flagged Owners"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# GET /ita/moderation/diners/flagged
@internal.route('/moderation/diners/flagged', methods=['GET'])
def list_flagged_diners():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT CD.CDId, U.Username
        FROM CasualDiner CD
        JOIN Users U ON CD.CDId = U.UserId
        WHERE CD.Flagged = TRUE
        ORDER BY CD.CDId DESC
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Flagged Diners"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# GET /ita/moderation/influencers/flagged
@internal.route('/moderation/influencers/flagged', methods=['GET'])
def list_flagged_influencers():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT InfId, Username, FirstName, LastName
        FROM Influencer
        WHERE Flagged = TRUE
        ORDER BY InfId DESC
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Flagged Influencers"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# ------------------------------------------------------------------
# 3.6 Daily Active Users (By day, deduplicated UserId)
# GET /ita/dau
# ------------------------------------------------------------------
@internal.route('/dau', methods=['GET'])
def get_daily_active_users():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT
            DATE(AA.LastVisit)        AS date,
            COUNT(DISTINCT AA.UserId) AS daily_active_users
        FROM AppAnalytics AA
        GROUP BY DATE(AA.LastVisit)
        ORDER BY date
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"Sadly": "No Activity Yet"}), 200

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response