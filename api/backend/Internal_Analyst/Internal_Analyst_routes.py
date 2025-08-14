from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

internal = Blueprint('internal', __name__)


# ------------------------------------------------------------------
# Catalog page (convenient for clicking /ita/internal in a browser to see all available endpoints)
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
            "/ita/dau",
            # Review restaurants (PUT)
            "/ita/requests/approve/1",
            # Delete inappropriate foodie posts (DELETE)
            "/ita/moderation/cdpost/1",
            # New: List of influencers awaiting review + Approved/Rejected
            "/ita/pending/influencers",
            "/ita/influencers/verify/8  (PUT=approve, DELETE=decline)",
            # New: Merged view of flagged users + unflagged users
            "/ita/moderation/users/flagged",
            "/ita/moderation/users/2/unflag?role=influencer",
            "/ita/moderation/users/1/unflag?role=casual_diner"
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
        SELECT 'bookmark_cd'  AS feature, IFNULL(SUM(Bookmark), 0) AS usage_count
        FROM CDPost
        UNION ALL
        SELECT 'share_cd',    IFNULL(SUM(Share), 0)
        FROM CDPost
        UNION ALL
        SELECT 'bookmark_inf', IFNULL(SUM(Bookmark), 0)
        FROM InfPost
        UNION ALL
        SELECT 'share_inf',    IFNULL(SUM(Share), 0)
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

# About IFNULL in MySQL
# -----------------------------------------------------------------------------
# Syntax: IFNULL(expr1, expr2)
# Meaning: If expr1 is NULL, return expr2; otherwise return expr1.
#
# Why use IFNULL in aggregates?
# - SUM(col): when no rows match, MySQL returns NULL (not 0).
# - COUNT(*): when no rows match, MySQL already returns 0.
# To make charts/tables friendlier, we convert “no data” from NULL to 0:
#   IFNULL(SUM(Bookmark), 0)  -> returns 0 instead of NULL
#
# Example:
#   -- Suppose the WHERE clause matches zero rows:
#   SELECT SUM(Bookmark)            -> NULL
#   SELECT IFNULL(SUM(Bookmark), 0) -> 0


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
# 3.5 List of flagged restaurant and users (four lists)
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


# ------------------------------------------------------------
# 3.7 Approve "Restaurant Addition" Request (UPDATE)
# PUT /ita/requests/approve/<restid>
# - Restaurant.`Add` = FALSE
# - RestaurantOwner.Verify = TRUE (The boss with the same RestId)
# ------------------------------------------------------------
@internal.route('/requests/approve/<int:restid>', methods=['PUT'])
def approve_restaurant_request(restid):
    cnx = db.get_db()
    cursor = cnx.cursor()

    q1 = "UPDATE Restaurant SET `Add` = FALSE WHERE RestId = %s"
    cursor.execute(q1, (restid,))
    r1 = cursor.rowcount

    q2 = "UPDATE RestaurantOwner SET Verify = TRUE WHERE RestId = %s"
    cursor.execute(q2, (restid,))
    r2 = cursor.rowcount

    cnx.commit()

    the_response = make_response(jsonify({
        "approved_restaurant": restid,
        "restaurant_rows_updated": r1,
        "owner_rows_updated": r2
    }))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# ------------------------------------------------------------
# 3.8 Delete inappropriate diner posts（DELETE）
# DELETE /ita/moderation/cdpost/<postid>
# Note: Delete CDPost(PostId).According to DDL, related Comment/Photo(s) Has associated deletion (note that data will be lost).
# ------------------------------------------------------------
@internal.route('/moderation/cdpost/<int:postid>', methods=['DELETE'])
def delete_cdpost(postid):
    cnx = db.get_db()
    cursor = cnx.cursor()

    q = "DELETE FROM CDPost WHERE PostId = %s"
    cursor.execute(q, (postid,))
    affected = cursor.rowcount

    cnx.commit()

    if affected == 0:
        return make_response(jsonify({
            "deleted_postid": postid,
            "message": "No record deleted (PostId not found)."
        }), 200)

    return make_response(jsonify({
        "deleted_postid": postid,
        "affected": affected
    }), 200)
    
    
    
 # ------------------------------------------------------------------
# 3.9 Pending Influencer Requests
# GET /ita/pending/influencers
# ------------------------------------------------------------------
@internal.route('/pending/influencers', methods=['GET'])
def list_pending_influencers():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT 
            I.InfId          AS UserId,
            U.Username       AS Username,
            I.Location       AS Location,
            I.RestaurantList AS RestaurantList,
            I.Verified
        FROM Influencer I
        JOIN Users U ON U.UserId = I.InfId
        WHERE I.Verified = FALSE
        ORDER BY I.InfId
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    if not theData:
        return jsonify({"Sadly": "No Pending Influencer Requests"}), 200
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# ------------------------------------------------------------------
# 3.10 verify Influencer request
# accept：  PUT    /ita/influencers/verify/<infid>     -> Verified = TRUE
# decline：  DELETE /ita/influencers/verify/<infid>     -> Delete "Pending Review" records (do not delete Users)
# Only affects records where Verified = FALSE 
# ------------------------------------------------------------------
@internal.route('/influencers/verify/<int:infid>', methods=['PUT'])
def approve_influencer(infid):
    cnx = db.get_db()
    cur = cnx.cursor()
    q = 'UPDATE Influencer SET Verified = TRUE WHERE InfId = %s AND Verified = FALSE'
    cur.execute(q, (infid,))
    rows = cur.rowcount
    cnx.commit()
    the_response = make_response(jsonify({
        "infid": infid,
        "approved": rows
    }))
    the_response.status_code = 200
    return the_response


@internal.route('/influencers/verify/<int:infid>', methods=['DELETE'])
def decline_influencer(infid):
    cnx = db.get_db()
    cur = cnx.cursor()
    # Only delete "pending review" influencer records; retain Users table
    q = 'DELETE FROM Influencer WHERE InfId = %s AND Verified = FALSE'
    cur.execute(q, (infid,))
    rows = cur.rowcount
    cnx.commit()
    the_response = make_response(jsonify({
        "infid": infid,
        "deleted_pending_rows": rows
    }))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------------
# 3.11 Flagged Users（Influencer + CasualDiner + RestaurantOwner）
# GET /ita/moderation/users/flagged
# return {UserId, Username, role} where role in {'influencer','casual_diner','restaurant_owner'}
# ------------------------------------------------------------------
@internal.route('/moderation/users/flagged', methods=['GET'])
def list_flagged_users():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT U.UserId, U.Username, 'influencer' AS role
        FROM Influencer I
        JOIN Users U ON U.UserId = I.InfId
        WHERE I.Flagged = TRUE
        UNION ALL
        SELECT U.UserId, U.Username, 'casual_diner' AS role
        FROM CasualDiner CD
        JOIN Users U ON U.UserId = CD.CDId
        WHERE CD.Flagged = TRUE
        UNION ALL
        SELECT U.UserId, U.Username, 'restaurant_owner' AS role
        FROM RestaurantOwner RO
        JOIN Users U ON U.UserId = RO.OwnerId
        WHERE RO.Flagged = TRUE
        ORDER BY role, UserId
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    if not theData:
        return jsonify({"Sadly": "No Flagged Users"}), 200
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------------
# 3.12 Revoke user's Flag（Ignore）
# PUT /ita/moderation/users/<userid>/unflag?role=influencer|casual_diner|restaurant_owner
# Support aliases role=owner -> restaurant_owner
# ------------------------------------------------------------------
@internal.route('/moderation/users/<int:userid>/unflag', methods=['PUT'])
def unflag_user(userid):
    role = (request.args.get('role') or '').lower()
    # Support owner aliases
    if role == 'owner':
        role = 'restaurant_owner'

    if role not in ('influencer', 'casual_diner', 'restaurant_owner'):
        return jsonify({"error": "role must be influencer|casual_diner|restaurant_owner"}), 400

    cnx = db.get_db()
    cur = cnx.cursor()

    if role == 'influencer':
        q = 'UPDATE Influencer SET Flagged = FALSE WHERE InfId = %s AND Flagged = TRUE'
    elif role == 'casual_diner':
        q = 'UPDATE CasualDiner SET Flagged = FALSE WHERE CDId = %s AND Flagged = TRUE'
    else:
        q = 'UPDATE RestaurantOwner SET Flagged = FALSE WHERE OwnerId = %s AND Flagged = TRUE'

    cur.execute(q, (userid,))
    rows = cur.rowcount
    cnx.commit()

    the_response = make_response(jsonify({
        "user": userid,
        "role": role,
        "unflagged": rows
    }))
    the_response.status_code = 200
    return the_response


# ======================================================================
# Frontend Integration Suggestions (Aligned with Your Four Tabs)
# ======================================================================

# Pending User Verifications (= Users who want to become Influencers):
#   - List:    GET    /ita/pending/influencers
#   - Approve: PUT    /ita/influencers/verify/{infid}
#   - Reject:  DELETE /ita/influencers/verify/{infid}

# Pending Restaurant Verifications (already implemented, keep unchanged):
#   - List:    GET    /ita/requests/pending
#   - Details: GET    /ita/requests/details
#   - Approve: PUT    /ita/requests/approve/{restid}
#   - (Optional) Reject:
#       DELETE /ita/requests/{restid}            # Soft reject (Add=FALSE)
#       DELETE /ita/requests/{restid}?hard=true  # Hard delete (use with caution)

# Flagged Users (merged view):
#   - List:   GET    /ita/moderation/users/flagged
#   - Ignore: PUT    /ita/moderation/users/{userid}/unflag?role=influencer|casual_diner

# Flagged Restaurants (your existing API already supports listing; if needed, add Ignore):
#   - (Optional) PUT  /ita/moderation/restaurants/{restid}/unflag

# Quick Self-Test (curl):
#   curl -s http://localhost:4000/ita/pending/influencers | jq .
#   curl -i -X PUT    http://localhost:4000/ita/influencers/verify/8
#   curl -i -X DELETE http://localhost:4000/ita/influencers/verify/8
#   curl -s http://localhost:4000/ita/moderation/users/flagged | jq .
#   curl -i -X PUT    "http://localhost:4000/ita/moderation/users/2/unflag?role=influencer"
#   curl -i -X PUT    "http://localhost:4000/ita/moderation/users/1/unflag?role=casual_diner"
# ======================================================================
