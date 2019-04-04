from . import main
from webapp.models import db, User, Stock_Basic
from flask import redirect, request, url_for, jsonify, abort
from flask_login import login_user, current_user


@main.route('api_login', methods=['POST'])
def api_login():
    emailaddress = request.form.get('emailaddress')
    password = request.form.get('password')
    user = User.query.filter_by(emailaddress=emailaddress).first()
    if user is not None:
        if user.verify_password(password):
            if login_user(user, request.form.get("remember")):
                # 登录成功
                # return redirect(request.args.get("next") or url_for('main.index'))
                # 此处应有next二次验证 避免重定向攻击
                if request.args.get("next") is not None:
                    if request.args.get("next")[0] == '/':
                        return redirect(request.args.get("next"))
                    else:
                        return redirect(url_for('main.index'))
                else:
                    return redirect(url_for('main.index'))
            else:
                abort(400)
        else:
            abort(400)
    else:
        abort(400)


@main.route('api_register', methods=['POST'])
def api_register():
    username = request.form.get('username')
    emailaddress = request.form.get('emailaddress')
    password = request.form.get('password')
    confirmpassword = request.form.get('confirmpassword')
    if User.query.filter_by(emailaddress=emailaddress).first() is not None:
        # print("该邮箱已被使用")
        abort(400)
    elif password != confirmpassword:
        # print("密码不一致")
        abort(400)
    else:
        new_user = User()
        new_user.username = username
        new_user.emailaddress = emailaddress
        new_user.password = password
        new_user.avatar = 'default.jpg'
        new_user.active = True
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(emailaddress=emailaddress).first()
        login_user(user)
        return redirect(url_for('main.index'))


@main.route('api_lockscreen', methods=['POST'])
def api_lockscreen():
    password = request.form.get("password")
    if current_user is not None and current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        if user.verify_password(password):
            if login_user(user, True):
                if request.args.get("next") is not None:
                    if request.args.get("next")[0] == '/':
                        return redirect(request.args.get("next"))
                    else:
                        return redirect(url_for('main.index'))
                else:
                    return redirect(url_for('main.index'))
            else:
                abort(400)
        else:
            abort(400)
    else:
        abort(400)


@main.route('api_recoverpassword', methods=['POST'])
def api_recoverpassword():
    pass


@main.route('api_checkemailaddress', methods=['GET'])
def api_checkemailaddress():
    emailaddress = request.args.get('emailaddress')
    user = User.query.filter_by(emailaddress=emailaddress).first()
    if user is None:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})


@main.route('api_checklogin', methods=['POST'])
def api_checklogin():
    emailaddress = request.form.get('emailaddress')
    password = request.form.get('password')
    user = User.query.filter_by(emailaddress=emailaddress).first()
    if user is not None:
        if user.verify_password(password):
            if user.is_active:
                return jsonify({'status': 'success', 'reason': ''})
            else:
                return jsonify({'status': 'failed', 'reason': '账户未激活'})
        else:
            return jsonify({'status': 'failed', 'reason': '密码错误'})
    else:
        return jsonify({'status': 'failed', 'reason': '不存在的用户'})


@main.route('api_checklockscreen', methods=['POST'])
def api_checklockscreen():
    password = request.form.get("password")
    if current_user is not None and current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        if user.verify_password(password):
            if user.is_active:
                return jsonify({'status': 'success', 'reason': ''})
            else:
                return jsonify({'status': 'failed', 'reason': '账户已被锁定'})
        else:
            return jsonify({'status': 'failed', 'reason': '密码错误'})
    else:
        return jsonify({'status': 'failed', 'reason': '用户状态异常'})


@main.route('api_stocklist', methods=['GET'])
def api_stocklist():
    stock_list = []
    result = Stock_Basic.query.all()
    # a,b,c前缀用来控制前端列表列名顺序
    for stock in result:
        stock_list.append({'a_ts_code': stock.ts_code, 'b_name': stock.name, 'c_abbreviation': stock.abbreviation})
    return jsonify({'value': stock_list})


@main.route('api_search', methods=['POST'])
def api_search():
    code=request.form.get('code')
    return redirect(url_for('stock_prediction.comprehensive_analysis',code=code))