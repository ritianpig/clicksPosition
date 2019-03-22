import json
import os
import pickle

from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
admin = Admin(name='Admin', endpoint='admin', template_mode='bootstrap3')
migrate = Migrate()
migrate.init_app(app, db)
app.config.from_object('config')
db.init_app(app)
db.create_all(app=app)
admin.init_app(app)
app.secret_key = 'qw#*12302189'
app.config['JSON_AS_ASCII'] = False


class DownJson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.String(500), comment="链接")
    screenshot = db.Column(db.String(20), comment="截屏时间间隔")
    maxtime = db.Column(db.String(20), comment="最大截屏个数")
    switch = db.Column(db.String(10), comment="开关")


class UpJson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(200), comment="UUID")
    main = db.Column(db.String(500), comment="链接")
    screen = db.Column(db.String(50), comment="容器分辨率")
    point = db.Column(db.TEXT, comment="点击位置数组")
    button = db.Column(db.TEXT, comment="返回键，左上角x按钮，数组")
    jump = db.Column(db.TEXT, comment="跳转链接数组")
    times = db.Column(db.String(20), comment="上报次数")


class Up(ModelView):
    can_export = True
    create_modal = True
    edit_modal = True
    can_view_details = True
    column_searchable_list = ["userid"]
    column_editable_list = ["userid", "main", "screen", "point",
                            "button", "jump", "times"]


admin.add_view(ModelView(DownJson, db.session, name="下发Json"))
admin.add_view(Up(UpJson, db.session, name="上传Json"))


@app.route("/downjson", methods=["GET", "POST"])
def downjson():
    if request.method == "GET":
        res_data = db.session.query(DownJson).first()
        if res_data:
            downdic = {
                "main": res_data.main,
                "screenshot": res_data.screenshot,
                "maxtime": res_data.maxtime,
                "switch": res_data.switch
            }
            result = {"data": downdic}
            return jsonify(result)
        else:
            return "没有录入json"
    else:
        return "不支持POST请求"


@app.route("/upjson", methods=["GET", "POST"])
def upjson():
    if request.method == "POST":
        get_data = request.data
        data_dic = json.loads(get_data)

        userid = data_dic["userid"]
        main = data_dic["main"]
        screen = data_dic["screen"]
        point = json.dumps(data_dic["point"])
        button = json.dumps(data_dic["button"])
        jump = json.dumps(data_dic["jump"])
        times = data_dic["times"]
        add_json = UpJson(userid=userid, main=main, screen=screen,
                          point=point, button=button, jump=jump, times=times)
        db.session.add(add_json)
        db.session.commit()
        return "ok"
    else:
        return "不支持GET请求"


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        get_name = request.headers["name"]
        get_data = request.get_data()
        path = os.path.dirname(os.path.abspath(__file__))
        name = path + '/static/' + get_name
        with open(name, "wb") as f:
            f.write(get_data)

        print(pickle.loads(get_data))
        return "ok"
    else:
        return "不支持GET请求"


if __name__ == '__main__':
    app.run()
