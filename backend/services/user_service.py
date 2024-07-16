

import models.user_management

class Usermanagement_Service:
    
    def __init__(self):
        self.usermanage = models.user_management.UserManagement()
        
        
    def login(self, username, password):
        
        success, messenge = self.usermanage.login_user(username, password)
        print(success, messenge)
        return success, messenge 
    def logout(self):
        self.usermanage.logout()
    
    def register(self, username , password):
        
        if len(username) < 3 or len(password) < 6:
            return False, "用户名至少需要3个字符，密码至少需要6个字符"
        success, messenge = self.usermanage.register_user(username, password)
        
        return success, messenge 
    