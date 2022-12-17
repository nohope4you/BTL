from Data import app,dao,admin, login, utils
from flask import render_template, request, redirect , session,jsonify
from flask_login import login_user, logout_user, login_required
from Data.decorator import annonymous_user
import cloudinary.uploader


@app.route("/trangchunhanvien")
def indexnv():
    kw = request.args.get('Search')
    cate_id = request.args.get('user_id')
    Room = dao.load_Room_kh(cate_id,kw)
    return render_template('nhanvien/index.html',Room=Room)



@app.route('/login-nhanvien', methods=['get', 'post'])
@annonymous_user
def login_nv_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get("next")
            return redirect(n if n else 'trangchunhanvien')

    return render_template('nhanvien/loginnv.html')



@app.route("/nhanvien")
def nhanvien():
    return render_template('nhanvien/loginnv.html')


@app.route("/lapphieudatphongnhanvien", methods=['get','post'])
def lpnv():
    cate_id = request.args.get('category_id')
    Room = dao.load_Room(cate_id)
    if request.method.__eq__('POST'):
            dao.Save_receipt_nv(name=request.form['name'],
                                quantity=request.form['quantity'],
                                price=request.form['price'],
                                room_id=request.form['room_id'],
                        CustomerName=request.form['CustomerName'],
                        CCCD=request.form['CCCD'],
                        Address=request.form['Address'],
                        DateDat=request.form['DateDat'],
                        DateTra=request.form['DateTra'])

    return render_template('nhanvien/LapPhieu.html', Room=Room)


@app.context_processor
def common_attr():
    return {
        'cart':utils.cart_stats(session.get(app.config['CART_KEY']))
    }


@app.route('/cart')
def cart():
    return render_template('Datphong.html')

@app.route('/api/cart',methods=['post'])
def add_to_cart():
    key = app.config['CART_KEY']
    cart = session[key] if key in session else{}

    data = request.json
    id = str(data['id'])
    name =data['name']
    price = data['price']
    if id in cart:
       cart[id]['quantity'] += 1
    else:
        name = data['name']
        price = data['price']

        cart[id]={
            "id":id,
            "name":name,
            "price":price,
            "quantity":1
        }

    session[key]=cart

    return jsonify(utils.cart_stats(cart))



@app.route('/api/cart/<room_id>',methods=['put'])
def update_cart(room_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and room_id in cart:
        cart[room_id]['quantity']=int(request.json['quantity'])

    session[key] = cart
    return jsonify(utils.cart_stats(cart))



@app.route('/api/cart/<room_id>', methods=['delete'])
def delete_cart(room_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and room_id in cart:
        del cart[room_id]

    session[key] = cart
    return jsonify(utils.cart_stats(cart))



@app.route('/api/pay')
@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart:
        try:
            dao.save_receipt(cart=cart)
        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})




@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            res = cloudinary.uploader.upload(request.files['avatar'])
            avatar = res['secure_url']

            dao.register(name=request.form['name'],
                         username=request.form['username'],
                         password=password,
                         avatar=avatar)
        else:
            err_msg = " Mật khẩu không khớp!!! "
    return render_template('register.html', err_msg=err_msg)




@app.route('/DTTKH', methods=['get','post'])
def DTTKH():
    err_msg = ''
    if request.method.__eq__('POST'):
            dao.DTTKH( CustomerName=request.form['CustomerName'],
                         CCCD=request.form['CCCD'],
                       Address=request.form['Address'],
                       DateDat=request.form['DateDat'],
                       DateTra=request.form['DateTra'])

    return render_template('Datphong.html', err_msg=err_msg)




@app.route('/login', methods=['get', 'post'])
@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get("next")
            return redirect(n if n else '/')

    return render_template('login.html')




@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')



@app.route('/logoutnv')
def logout_nv_user():
    logout_user()
    return redirect('/login-nhanvien')



@app.route("/Room/<int:category_id>")
def details(category_id):
    room = dao.get_room_by_id(category_id)
    return render_template('details.html', r=room)


@app.route("/Gioithieu.html")
def introduce():
    return render_template('Gioithieu.html')



@app.route("/")
def index():
    Menu = dao.load_Menu()
    MenuBar = dao.load_MenuBar()

    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    Room = dao.load_Room(cate_id)
    return render_template('index.html', Menu = Menu, Room = Room, MenuBar=MenuBar)



@login.user_loader
def load_user(user_id):
    return dao.get_user_id(user_id)



@app.route('/login-admin', methods=['post'])
def login_admin():
    username=request.form['username']
    password=request.form['password']
    user= dao.auth_user(username=username,password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True)