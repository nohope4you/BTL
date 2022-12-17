import numbers
from  flask_login import  current_user
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from Data import db,app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime
from datetime import timedelta




class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    EMPLOY = 3



class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Menu(BaseModel):
    __tablename__ = 'Menu'

    name = Column(String(50), nullable=False)
    Room = relationship('Room', backref = 'Menu' , lazy=True)



prod_tag = db.Table('prod_tag',Column('Room_id', Integer, ForeignKey('Room.id'), primary_key=True),Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))



class Room(BaseModel):
    __tablename__='Room'
    name= Column(String(200),nullable=False)
    description = Column(Text)
    Type = Column(String(200))
    price = Column(Float, default=0)
    image = Column(String(200))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Menu.id),nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='room', lazy=True)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery', backref=backref('room',lazy=True))


    # Quydinh = relationship('Quydinh', backref='room', lazy=True)



class User(BaseModel,UserMixin):
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(200), nullable=False)
    active = Column(Boolean,default=True)
    user_role = Column(Enum(UserRole),default=UserRole.USER)
    receipts = relationship('Receipt', backref='user',lazy= True)
    detailsTTKH = relationship('TTKH', backref='user', lazy=True)

    def __str__(self):
        return self.name



class Receipt(BaseModel):
    create_date= Column(DateTime, default=datetime.now())
    create_Month = Column(String(50), default=datetime.now().strftime("%G-%m"))
    user_id = Column(Integer, ForeignKey(User.id),nullable=False)
    details = relationship('ReceiptDetails',backref='receipt', lazy=True)



class ReceiptDetails(BaseModel):
    name = Column(String(100))
    quantity= Column(Integer,default=0)
    price = Column(Float,default=0)
    receipt_id=Column(Integer, ForeignKey(Receipt.id),nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)





class TTKH(BaseModel,UserMixin):
    CustomerName = Column(String(100),nullable=False)
    CCCD = Column(String(100),nullable=False)
    Address = Column(String(300),nullable=False)
    active = Column(Boolean,default=True)
    user_role = Column(Enum(UserRole),default=UserRole.USER)
    DateDat = Column(String(100),nullable=False)
    DateTra = Column(String(100),nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.name




class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name




# class Quydinh(BaseModel):
#     user_id = Column(Integer, ForeignKey(User.id), nullable =False)
#     room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
#     quydinh1 = relationship('ChiTietQuyDinhTN',backref='Quydinh', lazy=True)
#     quydinh2 = relationship('ChiTietQuyDinhNN', backref='Quydinh', lazy=True)
#
#
#
# class ChiTietQuyDinhTN(BaseModel):
#     priceLK = Column(Float,default=0)
#     priceSL = Column(Float,default=0)
#     Quydinh_id=Column(Integer, ForeignKey(Quydinh.id),nullable=False)
#     room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
#
#
#
# class ChiTietQuyDinhNN(BaseModel):
#     priceLK = Column(Float,default=0)
#     priceSL = Column(Float,default=0)
#     Quydinh_id=Column(Integer, ForeignKey(Quydinh.id),nullable=False)
#     room_id = Column(Integer, ForeignKey(Room.id), nullable=False)




if __name__=='__main__':
    with app.app_context():

        db.create_all()


        # n = Tag(name="Hết phòng")
        # db.session.add(n)
        # db.session.commit()

        # import hashlib
        # password=str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        # u1 = User(name='Admin', username='admin', password=password,image='https://cf.bstatic.com/xdata/images/hotel/max1280x900/402606316.jpg?k=00bb2836265ada9265b2c731390d0554c0a044162eda9d6c66334a028c606f13&o=&hp=1',
        #           user_role=UserRole.ADMIN)
        # db.session.add(u1)
        # db.session.commit()
        #
        #
        # import hashlib
        # password=str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        # nv1 = User(name='Nhanvien', username='employ', password=password,image='https://cf.bstatic.com/xdata/images/hotel/max1280x900/402606316.jpg?k=00bb2836265ada9265b2c731390d0554c0a044162eda9d6c66334a028c606f13&o=&hp=1',
        #           user_role=UserRole.EMPLOY)
        # db.session.add(nv1)
        # db.session.commit()
        #
        #
        #
        #
        #
        # r1 = Room(name= "Phòng số 1", description= "Phòng 2 người, sang trọng",Type= "Deluxe", price= 1000000,  image= "https://cf.bstatic.com/xdata/images/hotel/max1280x900/402606316.jpg?k=00bb2836265ada9265b2c731390d0554c0a044162eda9d6c66334a028c606f13&o=&hp=1",category_id= 1)
        # r2 = Room(name= "Phòng số 2", description= "Phòng 2 người,d sang trọng",Type="Royal", price=3000000, image="https://cf.bstatic.com/xdata/images/hotel/max1280x900/402606316.jpg?k=00bb2836265ada9265b2c731390d0554c0a044162eda9d6c66334a028c606f13&o=&hp=1", category_id= 2)
        # r3 = Room(name="Phòng số 2", description="Phòng 2 người,d sang trọng", Type="Standard", price=3000000,
        #           image="https://cf.bstatic.com/xdata/images/hotel/max1280x900/402606316.jpg?k=00bb2836265ada9265b2c731390d0554c0a044162eda9d6c66334a028c606f13&o=&hp=1",
        #           category_id=3)
        # db.session.add_all([r1,r2,r3])
        # db.session.commit()


        # p1 = Menu(name='Standard')
        # p2 = Menu(name='Superior')
        # p3 = Menu(name='Deluxe')
        # p4 = Menu(name='Royal')
        # db.session.add_all([p1,p2,p3,p4 ])

        db.session.commit()
        db.create_all()