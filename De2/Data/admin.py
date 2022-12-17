from Data.Models import Room
from Data import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import request



class RoomView(ModelView):
    column_searchable_list = ['name','description']
    column_filters = ['name','price']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Phòng',
        'description': 'Mô tả',
        'price': 'giá'

    }




class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = dao.stats_reveneue(kw=request.args.get('kw'),
                                   Month=request.args.get('Month'))
        sumt = dao.Sum(Month=request.args.get('Month'))
        return self.render('admin/stats.html',stats=stats,sumt=sumt)



class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_product_by_cate()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name="QUẢN TRỊ VIÊN", template_mode='bootstrap4',  index_view=MyAdminView())
admin.add_view(ModelView(Room, db.session))
# admin.add_view(ModelView(ChiTietQuyDinhTN, db.session))
# admin.add_view(ModelView(ChiTietQuyDinhNN, db.session))
admin.add_view(StatsView(name='Thống kê'))