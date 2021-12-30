from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages
import hashlib

# from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# csrf_protect



# Create your views here.

# helper function


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

################## HOME PAGE STUFF ############################

@csrf_exempt
def home_wargs(request, id):
    # for testing purposes, we are returning obtain seller related product information
    with connection.cursor() as cursor:
        query = "SELECT * FROM Seller WHERE sellerID=\"%s\";" % id
        cursor.execute(query)
        rows = dictfetchall(cursor)

    return render(request, 'SellerMenu.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password = hashlib.sha256(password.encode())
        password = password.hexdigest()
        # username = 'sellerID'

        logged_in = authenticate(username, password)

        if logged_in:
            id = get_id(username)
            request.session["ID"] = id
            return home_wargs(request, id)
        else:
            return redirect('/seller')  # add

    else:
        return render(request, 'SellerLogin.html')

################################ SELLER TRACK PACKAGES ###################################

@csrf_exempt
def seller_track_pack(request):
    if request.method == 'POST':
        product_id = request.POST['productid']
        return seller_track_pack_res(request, product_id)
    else:
        return render(request, 'SellerTrackProductDets.html')

@csrf_exempt
def seller_track_pack_res(request, prod_id):
    with connection.cursor() as cursor:
        query = "SELECT *  FROM Product WHERE trackingID=\"%s\";" % prod_id
        cursor.execute(query)
        rows = dictfetchall(cursor)

    # only one row so we index and get first
    # if not rows:
    #     row = None
    # else:
    #     row = rows[0]
    return render(request, "SellerTrackProductDetsResult.html", {'data': rows})


########## SELLER CHECK FOR UPDATES #######################
@csrf_exempt
def seller_check_updates(request):
    session_id = request.session["ID"]

    with connection.cursor() as cursor:
        query = "SELECT trackingID, warehouseID, currentLocation, productRoute, paymentStatus, price FROM Product WHERE sellerID = \"%s\";" % session_id
        cursor.execute(query)
        rows = dictfetchall(cursor)

    return render(request, 'SellerCheckUpdates.html', {'data': rows})


####################### SELLER GET CLIENT INFORMATION ################################
@csrf_exempt
def seller_client_info(request):

    if request.method == 'POST':
        product_id = request.POST['trackingid']
        return seller_client_result(request, product_id)
    else:
        return render(request, 'SellerObtainClientInfo.html')

@csrf_exempt
def seller_client_result(request, product_id):

    with connection.cursor() as cursor:
        query = "SELECT clientPhoneNumber FROM Product WHERE trackingID=\"{}\";".format(
            product_id)
        cursor.execute(query)
        rows = dictfetchall(cursor)
 # only one row so we index and get first
    if not rows:
        row = None
        success = False
    else:
        row = rows[0]

    if row is not None:
        phoneNum = row["clientPhoneNumber"]
        success = 1
        # row has clientPhoneNumber
        with connection.cursor() as cursor:
            query = "SELECT * FROM Client WHERE phoneNumber={};".format(phoneNum) 
            cursor.execute(query)
            data = dictfetchall(cursor)
        data = data[0]
    else:
        success = 0
        data = row
    return render(request, "SellerObtainClientInfoResult.html", {'data': data, 'success': success})

# HELPER FUNCTIONS

@csrf_exempt
def authenticate(username, password):
    if username == "":
        return False

    with connection.cursor() as cursor:
        # query = "SELECT userPassword FROM LoginInfo WHERE LoginInfo.userName=\"%s\";" % username
        query = "SELECT userPassword FROM LoginInfo WHERE LoginInfo.userName=\"{}\";".format(
            username)
        cursor.execute(query)
        rows = dictfetchall(cursor)

    if rows is not None:
        for row in rows:
            if row["userPassword"] == password:
                return True
            else:
                return False
        return False
    else:
        return False


def get_id(username):
    with connection.cursor() as cursor:
        query = "SELECT ID FROM LoginInfo WHERE LoginInfo.userName=\"%s\";" % username
        cursor.execute(query)
        rows = dictfetchall(cursor)

    id = rows[0]
    return id["ID"]
