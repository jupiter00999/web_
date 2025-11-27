
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()  # 数据库实例

class LoginUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    avatar = db.Column(db.String(200), nullable=False, default='default_avatar.png')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.nickname,
            'img': self.avatar
        }

# 补充商品和购物车模型定义（与init_db.py保持一致）
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    original_price = db.Column(db.Float)
    current_price = db.Column(db.Float, nullable=False)  # 现价
    seller = db.Column(db.String(100), nullable=False)
    images = db.Column(db.String(200), nullable=False)  # 图片路径
    sales = db.Column(db.Integer, default=0, nullable=False)  # 销量
    price_desc = db.Column(db.String(50), nullable=False)  # 价格描述

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('login_user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime)