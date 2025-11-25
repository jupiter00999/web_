# database.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import random
from datetime import datetime, timedelta

db = SQLAlchemy()


class LoginUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    # --- 修改：默认值只存文件名 ---
    avatar = db.Column(db.String(200), nullable=False, default='default_avatar.png')

    # --- 新增：添加一个 to_dict 方法，方便前端使用 ---
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.nickname,  # 抽奖时显示昵称
            'img': self.avatar
        }


class SalesData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)


class AgeDistribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age_group = db.Column(db.String(20), nullable=False)
    count = db.Column(db.Integer, nullable=False)


class ViewData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(50), nullable=False)
    views = db.Column(db.Integer, nullable=False)


class FollowData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    followers = db.Column(db.Integer, nullable=False)


def init_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("正在填充数据库...")

        # --- 修改：创建多个用于抽奖的注册用户 ---
        demo_users = [
            LoginUser(username='admin', nickname='管理员', phone='13800138000', password='password',
                      avatar='ad123456_1__.jpg'),
            LoginUser(username='user2', nickname='用户2', phone='13800138001', password='password',
                      avatar='avatar2.jpg'),
            LoginUser(username='user3', nickname='用户3', phone='13800138002', password='password',
                      avatar='avatar3.jpg'),
            LoginUser(username='user4', nickname='用户4', phone='13800138003', password='password',
                      avatar='avatar4.jpg'),
            LoginUser(username='user5', nickname='用户5', phone='13800138004', password='password',
                      avatar='avatar5.jpg'),
        ]
        db.session.add_all(demo_users)
        db.session.commit()

        sales_data = []
        base_date = datetime.now().date() - timedelta(days=30)
        for i in range(30):
            date = base_date + timedelta(days=i)
            amount = random.randint(100, 500)
            sales_data.append(SalesData(date=date, amount=amount))
        db.session.bulk_save_objects(sales_data)

        age_data = [
            AgeDistribution(age_group='18-25', count=random.randint(50, 200)),
            AgeDistribution(age_group='26-35', count=random.randint(100, 300)),
            AgeDistribution(age_group='36-45', count=random.randint(80, 250)),
            AgeDistribution(age_group='46+', count=random.randint(30, 150)),
        ]
        db.session.bulk_save_objects(age_data)

        view_data = [
            ViewData(page='首页', views=random.randint(1000, 5000)),
            ViewData(page='产品页', views=random.randint(800, 4000)),
            ViewData(page='关于我们', views=random.randint(200, 1000)),
            ViewData(page='博客', views=random.randint(500, 2500)),
        ]
        db.session.bulk_save_objects(view_data)

        follow_data = [
            FollowData(category='科技', followers=random.randint(10000, 50000)),
            FollowData(category='娱乐', followers=random.randint(20000, 80000)),
            FollowData(category='体育', followers=random.randint(5000, 30000)),
            FollowData(category='财经', followers=random.randint(8000, 40000)),
        ]
        db.session.bulk_save_objects(follow_data)

        db.session.commit()
        print("数据库初始化并填充数据完成！")
        print("默认登录账号: admin, 密码: password (明文存储)")
