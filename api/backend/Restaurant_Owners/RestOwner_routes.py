from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

restowners = Blueprint('restowners', __name__)

# The initial route to test connection.
# I don't want to delete it personally, it means a lot.
# localhost:4000/ro/rostowners
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


# RestOwner User Story 1: Shifan (his Owner ID = 3) needs to  view Casual Dinners’ 
# comments and ratings, so that  he can identify recurring complaints or compliments 
# and act accordingly
# localhost:4000/ro/restowners/<int:owner_id>
@restowners.route('/restowners/<int:owner_id>', methods=['GET'])
def get_reviews(owner_id):
    cursor = db.get_db().cursor()

    # If the owner_id does not exist, return an error message
    check_owner_query = '''
        SELECT 1 FROM RestaurantOwner WHERE OwnerId = %s;
    '''
    cursor.execute(check_owner_query, (owner_id,))
    owner_exists = cursor.fetchone()

    if not owner_exists:
        return jsonify({"error": "Owner not found"}), 404

    
    the_query = '''
    SELECT C.Comment, CDP.Rating
    FROM RestaurantOwner RO
    JOIN Restaurant R ON RO.RestId = R.RestId
    JOIN CDPost CDP ON R.RestId = CDP.RestId
    JOIN Comment C ON CDP.PostId = C.CDPostId
    WHERE RO.OwnerId = %s;
    '''

    cursor.execute(the_query, (owner_id,))
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"message": "No reviews found for this owner"}), 200

    return jsonify(theData), 200

# RestOwner User Story 2: Shifan needs to  add new dishes, so that 
# he can improve his menu based on customer preferences
# localhost:4000/ro/<int:owner_id>/add_menuitem
@restowners.route('/<int:owner_id>/add_menuitem', methods=['POST'])
def add_menuitem(owner_id):
    cursor = db.get_db().cursor()
    # If the owner_id does not exist, return an error message
    check_owner_query = '''
        SELECT 1 FROM RestaurantOwner WHERE OwnerId = %s;
    '''
    cursor.execute(check_owner_query, (owner_id,))
    owner_exists = cursor.fetchone()
    
    data = request.get_json()
    required_fields = ['RestId', 'DishName', 'Price']
    for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400


    query = '''
    INSERT INTO MenuItem
    (RestId, DishName, Price)
    VALUES (%s, %s, %s)
    '''
    cursor.execute(
        query,
        (
            data["RestId"],
            data["DishName"],
            data["Price"],
        ),
    )

    db.get_db().commit()
    new_menuitem_id = cursor.lastrowid
    cursor.close()
    return jsonify({"message": "Menu item added successfully", "menuitem_id": new_menuitem_id}), 201

# This route is when restaurant owners want to delete a menu item
# localhost:4000/ro/<int:owner_id>/delete_menuitem/<int:dish_id>
@restowners.route('/<int:owner_id>/delete_menuitem/<int:dish_id>', methods=['DELETE'])
def delete_menuitem(owner_id, dish_id):
    cursor = db.get_db().cursor()
    # If the owner_id does not exist, return an error message
    check_owner_query = '''
        SELECT 1 FROM RestaurantOwner WHERE OwnerId = %s;
    '''
    cursor.execute(check_owner_query, (owner_id,))
    owner_exists = cursor.fetchone()
    
    if not owner_exists:
        return jsonify({"error": "Owner not found"}), 404

    query = '''
    DELETE MenuItem
    FROM MenuItem
    JOIN Restaurant ON MenuItem.RestId = Restaurant.RestId
    JOIN RestaurantOwner ON Restaurant.RestId = RestaurantOwner.RestId
    WHERE RestaurantOwner.OwnerId = %s AND DishId = %s;
    '''
    
    cursor.execute(query, (owner_id, dish_id))
    db.get_db().commit()
    
    return jsonify({"message": "Menu item deleted successfully"}), 200


# This route is to prove the POST route works
# localhost:4000/ro/menuitem
@restowners.route('/menuitem', methods=['GET'])
def get_menu_items():
    cursor = db.get_db().cursor()

    the_query = '''
    SELECT DishId, DishName, Price, RestId
    FROM MenuItem
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# RestOwner User Story 3: Shifan needs to see the performance of the ad 
# so that he can decide whether to continue running it
# localhost:4000/ro/<int:owner_id>/ad_performance
@restowners.route('/<int:owner_id>/ad_performance', methods=['GET'])
def ad_performance(owner_id):
    cursor = db.get_db().cursor()
    # If the owner_id does not exist, return an error message
    check_owner_query = '''
        SELECT 1 FROM RestaurantOwner WHERE OwnerId = %s;
    '''
    cursor.execute(check_owner_query, (owner_id,))
    owner_exists = cursor.fetchone()
    if not owner_exists:
        return jsonify({"error": "Owner not found"}), 404

    the_query = '''
    SELECT AD.CampaignId, AD.AdCost, AD.Revenue, AD.Profit
    FROM AdCampaign AD
    JOIN RestaurantOwner RO ON AD.OwnerId = RO.OwnerId
    WHERE RO.OwnerId = %s
    '''
    cursor.execute(the_query, (owner_id,))
    theData = cursor.fetchall()
    if not theData:
        return jsonify({"message": "No reviews found for this owner"}), 200

    return jsonify(theData), 200

# RestOwner User Story 4: Shifan needs to see the ranking of number of customers
# visited so that he can evaluate his restaurant
# %20 repersents a space in the URL
# localhost:4000/ro/<location>/customer_ranking
@restowners.route('/<location>/customer_ranking', methods=['GET'])
def customer_ranking(location):
    cursor = db.get_db().cursor()

    the_query = '''
    SELECT R.RestName, R.NumVisits
    FROM Restaurant R
    WHERE Location = %s
    ORDER BY R.NumVisits DESC;
    '''

    cursor.execute(the_query, (location,))
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"message": "No customer data found for this location"}), 200

    return jsonify(theData), 200

# RestOwner User Story 5: Shifan needs to  filter the food influencers by location 
# he wants to corporate with so that he can advertise his restaurant in a more efficient way
# %20 repersents a space in the URL
# localhost:4000/ro/influencers/<location>
@restowners.route('/influencers/<location>', methods=['GET'])
def get_influencers_by_location(location):
    cursor = db.get_db().cursor()

    the_query = '''
    SELECT Influencer.InfId, Influencer.UserName, Influencer.FirstName, Influencer.LastName
    FROM Influencer
    WHERE Influencer.Location = %s
    '''
    
    cursor.execute(the_query, (location,))
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"message": "No influencers found for this location"}), 200

    return jsonify(theData), 200

# RestOwner User Story 6: Shifan needs to compare the performance of his restaurant 
# to the ones in the same location, so that he can spot opportunities for improvement and stay competitive
# localhost:4000/ro/<int:owner_id>/rest_performance
@restowners.route('/<int:owner_id>/rest_performance', methods=['GET'])
def rest_performance(owner_id):
    cursor = db.get_db().cursor()
    
    # If the owner_id does not exist, return an error message
    check_owner_query = '''
        SELECT 1 FROM RestaurantOwner WHERE OwnerId = %s;
    '''
    cursor.execute(check_owner_query, (owner_id,))
    owner_exists = cursor.fetchone()
    if not owner_exists:
        return jsonify({"error": "Owner not found"}), 404

    the_query = '''
    SELECT my.Rating AS MyRating, AVG(r.Rating) AS AvgOther
    FROM RestaurantOwner myOwner
    JOIN Restaurant my ON my.RestId = myOwner.RestId
    JOIN Restaurant r ON r.Location = my.Location
    WHERE myOwner.OwnerId = %s
    AND r.RestId <> my.RestId;
    '''

    cursor.execute(the_query, (owner_id,))
    theData = cursor.fetchall()

    if not theData:
        return jsonify({"message": "No performance data found for this owner"}), 200

    return jsonify(theData), 200

@restowners.route('/test', methods=['GET'])
def get_all_test():
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT *
    FROM Comment
    '''

    cursor.execute(the_query)
    theData = cursor.fetchall()


    return jsonify(theData), 200