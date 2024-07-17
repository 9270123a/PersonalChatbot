
import jwt
import datetime

class Usermanagement_Service:
    
    SECRET_KEY = "your_secret_key"
    def __init__(self, usermanagement):
        self.usermanage = usermanagement
        
        
    def login(self, username, password):
        
        success, message = self.usermanage.login_user(username, password)
        
        result = {
        'success': success,
        'message': message
    }

    # 返回 JSON 格式的響應
        return result

    def logout(self):
        self.usermanage.logout()
    
    def register(self, username , password):
        
        if len(username) < 3 or len(password) < 6:
            return False, "用户名至少需要3个字符，密码至少需要6个字符"
        success, messenge = self.usermanage.register_user(username, password)
        
        return success, messenge 
    def generate_auth_token(self, username):
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, self.SECRET_KEY, algorithm='HS256')
        return token

    def verify_auth_token(self, token):
        try:
            data = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return True
        except:
            return False

    def get_username_from_token(self, token):
        try:
            data = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return data['username']
        except:
            return None
    