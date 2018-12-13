from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint, 
          title='Zimmerman API',
          version='0.6',
          description="Zimmerman, backend API for Konishi"
      )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)