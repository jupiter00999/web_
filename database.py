# database.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


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

        print("数据库初始化并填充数据完成！")
        print("默认登录账号: admin, 密码: password (明文存储)")
