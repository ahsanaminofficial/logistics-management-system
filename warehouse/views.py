from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages
from copy import deepcopy

from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def dictfetchall(cursor): 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

@csrf_exempt
def home(request):
    # for testing purposes, we are returning obtain seller related product information
    # with connection.cursor() as cursor:
    #     query = "SELECT * FROM Warehouse WHERE warehouseID=\"%s\";" % id
    #     cursor.execute(query)
    #     rows = dictfetchall(cursor)
    return render(request, 'WarehouseMenu.html')


@csrf_exempt
def login(request):
    if request.method=='POST':
        username = request.POST['city']
        password = request.POST['password']

        logged_in = authenticate(username, password)

        if logged_in:
            request.session["city"] = username
            id = get_id(username)
            request.session["ID"] = id
            return home(request)
        else:
            messages.info(request, "invalid credentials")
            return redirect('/warehouse')  

    else:
        return render(request, 'WarehouseLogin.html')
    

@csrf_exempt
def authenticate(username, password):
    if username == "":
        return False

    with connection.cursor() as cursor:
        query = "SELECT userPassword FROM LoginInfo WHERE LoginInfo.userName=\"%s\";" % username
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


@csrf_exempt
def get_id(username):
    with connection.cursor() as cursor:
        query = "SELECT ID FROM LoginInfo WHERE LoginInfo.userName=\"%s\";" % username
        cursor.execute(query)
        rows = dictfetchall(cursor)

    id = rows[0]
    return id["ID"]


@csrf_exempt
def inventory(request):
    with connection.cursor() as cursor:
        # query goes here as string
        query = "SELECT * FROM Product WHERE currentLocation=\"%s\";" % request.session["ID"]
        cursor.execute(query)
        rows = dictfetchall(cursor)
    return render(request, 'WarehouseInventory.html', {'data': rows})



@csrf_exempt
def ship_products(request):
    if request.method=='POST':
        product = request.POST['id']
        dest = request.POST['warehouse']

        id = request.session["ID"]
        ship = product_exists(product, id)
        ship = warehouse_exists(dest)

        if ship:
            with connection.cursor() as cursor:
                q1 = "SELECT warehouseID FROM Warehouse WHERE Warehouse.city = \"%s\";"%dest
                cursor.execute(q1)
                rows = dictfetchall(cursor)
                if not rows:
                    row = None
                else:
                    row = rows[0]
                dest_id = row["warehouseID"]
                shift_product = "UPDATE Product SET Product.warehouseID = \"{}\",Product.currentlocation = \"{}\" WHERE Product.trackingID=\"{}\";".format(dest_id,dest_id,product)
                cursor.execute(shift_product)
            return render(request, 'WarehouseShipped.html')
        else:
            messages.info(request, "invalid credentials")
            return redirect('/warehouse/ship')  
    else:
        with connection.cursor() as cursor:
        # query goes here as string
            query = "SELECT Product.trackingID FROM Product WHERE currentLocation=\"%s\";" % request.session["ID"]
            cursor.execute(query)
            rows = dictfetchall(cursor)
        return render(request, 'WarehouseShipProducts.html', {'data': rows})


@csrf_exempt
def warehouse_exists(dest):
    if dest == "":
        return False

    with connection.cursor() as cursor:
        query = "SELECT city FROM Warehouse WHERE Warehouse.city=\"%s\";" % dest
        cursor.execute(query)
        rows = dictfetchall(cursor)
    
    if rows is not None:
        print("rows exist")
        for row in rows:
            if row["city"] == dest:
                return True
            else:
                return False
        return False
    else:
        return False



@csrf_exempt
def product_exists(product, id):
    if product == "":
        return False

    with connection.cursor() as cursor:
        print(id)
        query = "SELECT trackingID FROM Product WHERE Product.warehouseID=\"%s\";" % id
        cursor.execute(query)
        rows = dictfetchall(cursor)
    
    if rows is not None:
        print("rows exist")
        for row in rows:
            if row["trackingID"] == product:
                return True
            else:
                return False
        return False
    else:
        return False



@csrf_exempt
def deliver_products(request):
    if request.method=='POST':
        product = request.POST['id']
        rider = request.POST['rider']

        id = request.session["ID"]
        deliver = product_exists(product, id) # if product exists in warehouse having id
        deliver = rider_exists(rider,id) # if rider is available 

        if deliver:
            with connection.cursor() as cursor:
                loc = "Rider"
                dispatch_product = "UPDATE Product SET Product.currentLocation = \"{}\" WHERE Product.trackingID=\"{}\";".format(loc,product)
                cursor.execute(dispatch_product)
                dispatch_rider = "UPDATE Rider SET Rider.productID = \"{}\" WHERE Rider.riderID=\"{}\";".format(product,rider)
                cursor.execute(dispatch_rider)
            return render(request, 'WarehouseDelivered.html')
        else:
            messages.info(request, "invalid credentials")
            return redirect('/warehouse/deliver')  
    else:
        with connection.cursor() as cursor:
        # find available riders
            q1 = "SELECT * FROM Rider WHERE productID is NULL AND warehouseID = \"%s\";"%request.session["ID"]
            cursor.execute(q1)
            riders = dictfetchall(cursor)
        # find ready to be delivered products in inventory
            q2 = "SELECT * FROM Client, Product WHERE Product.currentLocation = \"{}\" AND Product.clientPhoneNumber=Client.phoneNumber AND Client.city=\"{}\";".format(request.session["ID"],request.session["city"])
            cursor.execute(q2)
            products = dictfetchall(cursor) # contains all products in warehouse inventory
        return render(request, 'WarehouseDeliverProducts.html', {'r': riders,'p':products})
    


@csrf_exempt
def rider_exists(riderID,warehouseID):
    if riderID == "":
        return False

    with connection.cursor() as cursor:
        query = "SELECT riderID FROM Rider WHERE productID is NULL AND warehouseID = \"%s\";"%warehouseID
        cursor.execute(query)
        rows = dictfetchall(cursor)
    
    if rows is not None:
        for row in rows:
            if row["riderID"] == riderID:
                return True
        return False
    else:
        return False

@csrf_exempt
def add_product(request):
    return render(request, "WarehouseAddProduct.html") 


@csrf_exempt
def old_seller(request):
    if request.method=='POST':
        # FORM VARIABLES
        price = request.POST['price']
        clientPhoneNumber = request.POST['clientphone']
        sellerID = request.POST['sellerID']
        w = request.session["city"]
        seller = seller_exists(sellerID, w)
        if seller:
            request.session["price"] = price
            request.session["clientPhoneNumber"] = clientPhoneNumber
            request.session["sellerID"] = sellerID
            
            # GET SELLER CITY AND NUM OF PRODUCTS
            with connection.cursor() as cursor:
                s = "SELECT sellerName, phoneNumber, city FROM Seller WHERE sellerID =\"{}\";".format(sellerID)
                cursor.execute(s)
                seller_data = dictfetchall(cursor)[0]
                sellerCity = seller_data["city"]
                sellerName = seller_data["sellerName"]
                sellerPhoneNumber = seller_data["phoneNumber"]
                p = "SELECT products FROM MAXID WHERE ID = 0;"
                cursor.execute(p)
                num_products = dictfetchall(cursor)[0]["products"]
                update2 = "UPDATE MAXID SET MAXID.products = MAXID.products+1;"
                cursor.execute(update2)
            
            # GENERATE VARIABLES - PRODUCT
            trackingID = "P0"+str(num_products+1)
            warehouseID = request.session["ID"]
            currentLocation = warehouseID
            
            request.session["sellerCity"] = sellerCity
            request.session["sellerName"] = sellerName
            request.session["sellerPhoneNumber"] = sellerPhoneNumber
            request.session["trackingID"] = trackingID
            request.session["warehouseID"] = warehouseID
            request.session["currentLocation"] = currentLocation
            
            old_client = client_exists(clientPhoneNumber)
        
            if old_client: # CLIENT EXISTS
                with connection.cursor() as cursor:
                    find_client_data = "SELECT phoneNumber,clientAddress,city FROM Client WHERE phoneNumber= \"%s\";"%clientPhoneNumber
                    cursor.execute(find_client_data)
                    rows = dictfetchall(cursor)
                    clientCity = rows[0]["city"]    
                productRoute = sellerCity + "/" + clientCity
                paymentStatus = 0
                with connection.cursor() as cursor: # CREATE PRODUCT
                    q3 = "INSERT INTO Product(trackingID, sellerID, warehouseID, currentLocation, productRoute, paymentStatus, price, clientPhoneNumber) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(trackingID, sellerID, warehouseID, currentLocation, productRoute, paymentStatus, price, clientPhoneNumber)
                    cursor.execute(q3)  
                return render(request, 'WarehouseAdded.html')       
            else:
                return redirect(register_client)  
        else:
            messages.info(request, "invalid credentials")
            return redirect('/warehouse/oldseller') 
    else:
        return render(request, 'WarehouseOldSeller.html')


@csrf_exempt
def new_seller(request):
    if request.method=='POST':
        # FORM VARIABLES
        price = request.POST['price']
        clientPhoneNumber = request.POST['clientphone']
        sellerName = request.POST['name']
        sellerPhoneNumber = request.POST['sellerphone']
        
        request.session["price"] = price
        request.session["clientPhoneNumber"] = clientPhoneNumber
        request.session["sellerName"] = sellerName
        request.session["sellerPhoneNumber"] = sellerPhoneNumber
        
        # GET NUM OF SELLERS AND PRODUCTS
        with connection.cursor() as cursor:
            s = "SELECT sellers FROM MAXID WHERE ID = 0;"
            cursor.execute(s)
            num_sellers = dictfetchall(cursor)[0]["sellers"]
            p = "SELECT products FROM MAXID WHERE ID = 0;"
            cursor.execute(p)
            num_products = dictfetchall(cursor)[0]["products"]
            update1 = "UPDATE MAXID SET MAXID.sellers = MAXID.sellers+1;"
            update2 = "UPDATE MAXID SET MAXID.products = MAXID.products+1;"
            cursor.execute(update1)
            cursor.execute(update2)
            
        # GENERATE VARIABLES - SELLER 
        sellerID = "S0"+str(num_sellers+1)
        sellerCity = request.session["city"]
        # GENERATE VARIABLES - PRODUCT
        trackingID = "P0"+str(num_products+1)
        warehouseID = request.session["ID"]
        currentLocation = warehouseID
        
        request.session["sellerCity"] = sellerCity
        request.session["sellerID"] = sellerID
        request.session["trackingID"] = trackingID
        request.session["warehouseID"] = warehouseID
        request.session["currentLocation"] = currentLocation
        
        # CREATE SELLER
        with connection.cursor() as cursor:
            q1 = "INSERT INTO Seller(sellerID, sellerName, phoneNumber, city) VALUES (\"{}\",\"{}\",\"{}\",\"{}\");".format(sellerID, sellerName, sellerPhoneNumber, sellerCity)
            cursor.execute(q1)
        
        old_client = client_exists(clientPhoneNumber)
        
        if old_client: # CLIENT EXISTS
            with connection.cursor() as cursor:
                find_client_data = "SELECT phoneNumber,clientAddress,city FROM Client WHERE phoneNumber= \"%s\";"%clientPhoneNumber
                cursor.execute(find_client_data)
                rows = dictfetchall(cursor)
                clientCity = rows[0]["city"]    
            productRoute = sellerCity + "/" + clientCity
            paymentStatus = 0
            with connection.cursor() as cursor: # CREATE PRODUCT
                q3 = "INSERT INTO Product(trackingID, sellerID, warehouseID, currentLocation, productRoute, paymentStatus, price, clientPhoneNumber) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(trackingID, sellerID, warehouseID, currentLocation, productRoute, paymentStatus, price, clientPhoneNumber)
                cursor.execute(q3)  
            return render(request, 'WarehouseAdded.html')       
        else:
            # request.method = 'GET'
            return redirect(register_client)   
    else:
        return render(request, 'WarehouseNewSeller.html')
    


@csrf_exempt
def register_client(request):
    if request.method=='POST':
        clientAddress = request.POST['address']
        clientCity = request.POST['city']
        city_exists = warehouse_exists(clientCity)
        if city_exists:
            with connection.cursor() as cursor: # CREATE CLIENT
                q2 = "INSERT INTO Client(phoneNumber, clientAddress, city) VALUES (\"{}\",\"{}\",\"{}\");".format(request.session["clientPhoneNumber"], clientAddress, clientCity)
                cursor.execute(q2)
            productRoute = request.session["sellerCity"] + "/" + clientCity
            paymentStatus = 0
            with connection.cursor() as cursor: # CREATE PRODUCT
                q3 = "INSERT INTO Product(trackingID, sellerID, warehouseID, currentLocation, productRoute, paymentStatus, price, clientPhoneNumber) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(request.session["trackingID"], request.session["sellerID"], request.session["warehouseID"], request.session["currentLocation"], productRoute, paymentStatus, request.session["price"], request.session["clientPhoneNumber"])
                cursor.execute(q3)  
            return render(request, 'WarehouseAdded.html') 
        else:
            messages.info(request, "invalid credentials")
            return redirect('/warehouse/registerclient')  
    else:
        return render(request, 'WarehouseRegisterClient.html')



@csrf_exempt
def client_exists(phoneNumber):
    if phoneNumber == "":
        return False

    with connection.cursor() as cursor:
        query = "SELECT phoneNumber FROM Client WHERE phoneNumber = \"%s\";"%phoneNumber
        cursor.execute(query)
        rows = dictfetchall(cursor)
    
    if rows is not None:
        for row in rows:
            if row["phoneNumber"] == phoneNumber:
                return True
        return False
    else:
        return False


@csrf_exempt
def seller_exists(id, w):
    if id == "":
        return False

    with connection.cursor() as cursor:
        query = "SELECT sellerID FROM Seller WHERE sellerID = \"{}\" AND city = \"{}\";".format(id,w)
        cursor.execute(query)
        rows = dictfetchall(cursor)
    
    if rows is not None:
        for row in rows:
            if row["sellerID"] == id:
                return True
        return False
    else:
        return False