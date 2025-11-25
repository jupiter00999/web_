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
    avatar = db.Column(db.String(200), nullable=False, default='default_avatar.png')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.nickname,
            'img': self.avatar
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False, default='default_product.png')
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


# 新增购物车表（核心修复）
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('login_user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)  # 商品数量
    added_at = db.Column(db.DateTime, default=datetime.now)

    # 关联关系（便于查询）
    user = db.relationship('LoginUser', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))


# 以下为原有数据模型（保持不变）
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

        # 添加测试用户（包含管理员）
        demo_users = [
            LoginUser(username='admin', nickname='管理员', phone='13800138000', password='password',
                      avatar='default_avatar.png'),
            LoginUser(username='user1', nickname='用户1', phone='13800138001', password='password',
                      avatar='default_avatar.png'),
        ]
        db.session.add_all(demo_users)
        db.session.commit()

        # 添加默认商品
        default_products = [
            Product(name='家乡特产 - 手工腊肠',
                    description='传统工艺制作，自然风干，咸香可口，真空包装',
                    price=59.9,
                    image='default_product.png'),
            Product(name='家乡特产 - 高山绿茶',
                    description='海拔800米高山种植，明前采摘，清香回甘',
                    price=89.0,
                    image='default_product.png'),
        ]
        db.session.add_all(default_products)
        db.session.commit()

        # 其他测试数据（保持不变）
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
        ]
        db.session.bulk_save_objects(view_data)

        follow_data = [
            FollowData(category='食品', followers=random.randint(10000, 50000)),
            FollowData(category='茶叶', followers=random.randint(8000, 40000)),
        ]
        db.session.bulk_save_objects(follow_data)

        db.session.commit()
        print("数据库初始化完成！")
        print("管理员账号: admin, 密码: password")