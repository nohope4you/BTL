import json
from Data import app,db
from Data.Models import Menu, Room, User ,Receipt, ReceiptDetails, TTKH
import hashlib
from  flask_login import  current_user
from sqlalchemy import func, DateTime



def load_MenuBar():
    with open('%s/data/MenuBar.json' % app.root_path, encoding='utf-8') as f:
        return json.load(f)


def load_Menu():
     return Menu.query.all()



def load_Room(room_id=None):
    query = Room.query

    if room_id:
        query = query.filter(Room.category_id.__eq__(room_id))

    return query.all()



def load_Room_kh(user_id=None,Search=None):
    query = TTKH.query

    if user_id:
        query = query.filter(TTKH.user_id.__eq__(user_id))


    if Search:
        query = query.filter(TTKH.CustomerName.contains(Search))

    return query.all()




def get_room_by_id(room_id):
    return Room.query.get(room_id)

def auth_user(username,password):
   password= str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
   return User.query.filter(User.username.__eq__(username.strip()),
                            User.password.__eq__(password)).first()




def get_user_id(user_id):
    return User.query.get(user_id)



def register(name, username, password, avatar):
    password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name,username=username,password=password,image=avatar)
    db.session.add(u)
    db.session.commit()



def DTTKH(CustomerName, CCCD, Address, DateDat, DateTra):
    m = TTKH(CustomerName=CustomerName,CCCD=CCCD,Address=Address, DateDat=DateDat, DateTra=DateTra, user=current_user)
    db.session.add(m)
    db.session.commit()



def save_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)


        for c in cart.values():

            d = ReceiptDetails(name=c['name'],quantity=c['quantity'], price=c['price'],
                               receipt=r, room_id=c['id'])
            db.session.add(d)

        db.session.commit()



def Save_receipt_nv(name,quantity,price,room_id,CustomerName, CCCD, Address, DateDat, DateTra):
    r = Receipt(user=current_user)
    db.session.add(r)
    n = ReceiptDetails(name=name, quantity=quantity, price=price,receipt=r, room_id=room_id)
    m = TTKH(CustomerName=CustomerName,CCCD=CCCD,Address=Address, DateDat=DateDat, DateTra=DateTra,user=current_user)
    db.session.add_all([n,m])
    db.session.commit()


def count_product_by_cate():
    return db.session.query(Menu.id,Menu.name, func.count(Room.id))\
        .join(Room,Room.category_id.__eq__(Menu.id), isouter=True).group_by(Menu.id).all()



def Sum(Month=None):
   query = db.session.query(func.sum(ReceiptDetails.price * ReceiptDetails.quantity))\
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

   if Month:
       query = query.filter(Receipt.create_Month.__le__(Month))

   return query.all()



def stats_reveneue(kw=None, Month=None):
    query = db.session.query(Room.id ,Room.name, func.sum(ReceiptDetails.price*ReceiptDetails.quantity))\
        .join(ReceiptDetails, ReceiptDetails.room_id.__eq__(Room.id))\
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if kw:
        query = query.filter(Room.name.contains(kw))

    if Month:
        query = query.filter(Receipt.create_Month.__le__(Month))


    return query.group_by(Room.id).order_by(-Room.id).all()



if __name__=='__main__':
    from Data import  app
    with app.app_context():
     print(count_product_by_cate())