from . import main
from webapp.models import User
from flask import render_template, redirect, url_for, session, request
from flask_login import login_fresh, current_user, login_required, login_user, logout_user


@main.route('login', methods=['GET'])
def login():
    if current_user is not None and current_user.is_authenticated:
        session['_fresh'] = False
        user = User.query.filter_by(id=current_user.id).first()
        login_user(user, True, None, False, False)
        return redirect(url_for('main.index'))
    if request.args.get('next') is not None:
        return render_template('main/login.html', args='?next=' + request.args.get('next'))
    else:
        return render_template('main/login.html')


@main.route('register', methods=['GET'])
def register():
    return render_template('main/register.html')


@main.route('logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route('recoverpassword', methods=['GET'])
def recoverpassword():
    return render_template('main/recoverpassword.html')


@main.route('lockscreen', methods=['GET'])
@login_required
def lockscreen():
    if request.args.get('next') is not None:
        return render_template('main/lockscreen.html', args='?next=' + request.args.get('next'))
    else:
        return render_template('main/lockscreen.html')


@main.route('', methods=['GET'])
# @login_required
def index():
    return render_template('main/index.html', fresh=login_fresh())
    # return redirect(url_for())


@main.route('database', methods=['GET'])
def database():
    return render_template('main/database.html')


@main.route('test', methods=['GET'])
def test():
    return render_template('stock_prediction/stock_prediction_base.html')

