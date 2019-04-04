# flask拓展模块
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .models import User
# 登陆控制
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.refresh_view="main.lockscreen"
login_manager.session_protection = "strong"

# 用于flash消息 在ajax方式中无效
login_manager.login_message = "您没有访问该页面的权限 请登陆后再试！"
login_manager.login_message_category = "提示"
login_manager.needs_refresh_message = "为了您的账户安全，需要重新验证您的身份！"
login_manager.needs_refresh_message_category="提示"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#csrf保护
csrf_protect = CSRFProtect()
