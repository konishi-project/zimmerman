from flask import redirect, flash
from flask_login import login_required, current_user

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from user import User

# Admin Index View is the Main Index, not the ModelView
class MainAdminIndexView(AdminIndexView):
    @login_required
    def is_accessible(self):
        # Check if the current user is an admin
        user = User.query.filter_by(username=current_user.username).first()
        if len(user.roles) > 0 and user.roles[0].name == 'admin':
            return True
        return False
    def inaccessible_callback(self, name, **kwargs):
        logout_user()
        flash('Unathorized user!')
        return redirect('/adminlogin')

# This is exactly similar to above Model but for ModelViews not Admin Index View.
class ProtectedModelView(ModelView):
    @login_required
    def is_accessible(self):
        # Check if the current user is an admin
        user = User.query.filter_by(username=current_user.username).first()
        if len(user.roles) > 0 and user.roles[0].name == 'admin':
            return True
        return False
    def inaccessible_callback(self, name, **kwargs):
        logout_user()
        flash('Unathorized user!')
        return redirect('/adminlogin')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))# Admin Index View is the Main Index, not the ModelView
class MainAdminIndexView(AdminIndexView):
    @login_required
    def is_accessible(self):
        # Check if the current user is an admin
        user = User.query.filter_by(username=current_user.username).first()
        if len(user.roles) > 0 and user.roles[0].name == 'admin':
            return True
        return False
    def inaccessible_callback(self, name, **kwargs):
        logout_user()
        flash('Unathorized user!')
        return redirect('/adminlogin')

# This is exactly similar to above Model but for ModelViews not Admin Index View.
class ProtectedModelView(ModelView):
    @login_required
    def is_accessible(self):
        # Check if the current user is an admin
        user = User.query.filter_by(username=current_user.username).first()
        if len(user.roles) > 0 and user.roles[0].name == 'admin':
            return True
        return False
    def inaccessible_callback(self, name, **kwargs):
        logout_user()
        flash('Unathorized user!')
        return redirect('/adminlogin')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))