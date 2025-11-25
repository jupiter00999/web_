# init_db.py

# 从你的 app.py 文件中导入必要的对象
from app import app
from database import init_db

if __name__ == '__main__':
    with app.app_context():
        print("正在手动初始化数据库...")
        init_db(app)
        print("数据库初始化完成！")
        print("默认登录账号: admin, 密码: password")