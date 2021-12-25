from django.shortcuts import render
from django.db import connection

# Create your views here.


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def client_home(request):
    return render(request, 'ClientMenu.html')


def client_track_pack(request):
    return render(request, 'ClientTrackPackages.html')

############ CLIENT SELLER INFORMATION ####################


def client_seller_info(request):
    if request.method == "POST":
        product_id = request.POST["trackingID"]
        return client_seller_result(request, product_id)

    else:
        return render(request, 'ClientObtainSellerInfo.html')


def client_seller_result(request, product_id):
    # find seller ID
    with connection.cursor() as cursor:
        query = "SELECT sellerID FROM Product WHERE trackingID = \"{}\"".format(
            product_id)
        cursor.execute(query)
        rows = dictfetchall(cursor)

    if len(rows):  # if result is found
        seller_id = rows[0]["sellerID"]
        # get seller information
        with connection.cursor() as cursor:
            query = "SELECT sellerName, phoneNumber, city FROM Seller WHERE sellerID = \"{}\"".format(
                seller_id)
            cursor.execute(query)
            rows = dictfetchall(cursor)

        seller_information = rows[0]
        return render(request, "ClientObtainSellerInfoResult.html", {"data": seller_information, "success": 1})
    else:
        return render(request, "ClientObtainSellerInfoResult.html", {"success": 0})


############# CLIENT PRODUCT DETAILS ######################
def client_prod_details(request):
    if request.method == 'POST':
        product_id = request.POST["trackingID"]
        with connection.cursor() as cursor:
            query = "SELECT * FROM Product WHERE trackingID = \"{}\"".format(
                product_id)
            cursor.execute(query)
            rows = dictfetchall(cursor)

        if len(rows):  # if the result comes up empty
            productData = rows[0]
            sellerID = productData["sellerID"]
            with connection.cursor() as cursor:
                query = "SELECT sellerName, phoneNumber, city FROM Seller WHERE sellerID = \"{}\";".format(
                    sellerID)
                cursor.execute(query)
                rows2 = dictfetchall(cursor)

            sellerData = rows2[0]
            return render(request, "ClientTrackProductDetsResult.html", {"sellerData": sellerData, "productData": productData, "success": 1})
        else:
            return render(request, "ClientTrackProductDetsResult.html", {"success": 0, "data": rows})

    return render(request, 'ClientTrackProductDets.html')


############# CLIENT RIDER INFORMATION ####################
def client_rider_info(request):
    if request.method == "POST":
        trackingID = request.POST["trackingID"]
        with connection.cursor() as cursor:
            query = "SELECT riderName, phoneNumber FROM Rider WHERE productID = \"{}\"".format(
                trackingID)
            cursor.execute(query)
            rows = dictfetchall(cursor)
        if len(rows) > 0:
            data = rows[0]
            return render(request, 'ClientTrackRiderInfoResult.html', {'data': data, 'success': 1})
        else:
            return render(request, 'ClientTrackRiderInfoResult.html', {'success': 0})
    else:
        return render(request, 'ClientTrackRiderInfo.html')


############# CLIENT CURRENT LOCATION INFORMATION ###########
def client_currentloc(request): # TODO: Check if current location needs to be updated (get city instead)
    if request.method == 'POST':
        trackingID = request.POST["trackingID"]
        with connection.cursor() as cursor:
            query = "SELECT currentLocation FROM Product WHERE trackingID = \"{}\"".format(trackingID)
            cursor.execute(query)
            rows = dictfetchall(cursor)
        if len(rows) > 0:
            data = rows[0]
            return render(request, 'ClientTrackCurrLocResult.html', {'data': data, 'trackingID': trackingID, 'success': 1})
        else:
            return render(request, 'ClientTrackCurrLocResult.html', {'success': 0})
    else:
        return render(request, 'ClientTrackCurrentLoc.html')


def clients(request):
    with connection.cursor() as cursor:
        # query goes here as string
        query = "SELECT * FROM Client WHERE phoneNumber=032028588"
        cursor.execute(query)
        rows = dictfetchall(cursor)

    print(rows)
    return render(request, 'output.html', {'data': rows})


def products_info(request):
    with connection.cursor() as cursor:
        query = "SELECT * FROM Client WHERE phoneNumber=032028588"
        cursor.execute(query)
        rows = dictfetchall(cursor)

    print(rows)
    return render(request, 'products_info.html', {'data': rows})
