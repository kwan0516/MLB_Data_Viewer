import hashlib
from baseObject import baseObject
from team import team
class user(baseObject):
    def __init__(self):
        self.setup()
        self.roles = [{'value':'admin','text':'admin'},{'value':'VIP','text':'VIP'},{'value':'customer','text':'customer'}]
        t = team()
    def hashPassword(self,pw):
        pw = pw+'xyz'
        return hashlib.md5(pw.encode('utf-8')).hexdigest()
    def verify_new(self,n=0):
        self.errors = []

        if self.data[n]['name'] == '':
            self.errors.append('Name cannot be blank.')
        else:
            u = user()
            u.getByField('name',self.data[n]['name'])
            if len(u.data) > 0:
                self.errors.append('Name already in use.')
        if self.data[n]['password'] != self.data[n]['password2']:
            self.errors.append('Retyped password must match.')
        if len(self.data[n]['password']) < 3:
            self.errors.append('Password needs to be more than 3 chars.')
        else:
            self.data[n]['password'] = self.hashPassword(self.data[n]['password'])
        rl = []
        for role in self.roles:
            rl.append(role['value'])
        if self.data[n]['role'] not in rl:
            self.errors.append(f'Role must be one of {rl}')
    
        teams = []
        t = team()
        t.getAll()
        for tm in t.data:
            teams.append(tm['Name'])
        if self.data[n]['favoriteTeam'] not in teams:
            self.errors.append('Team does not exist')
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
    def verify_update(self,n=0):
        self.errors = []

        if self.data[n]['name'] == '':
            self.errors.append('Name cannot be blank.')
        else:
            u = user()
            u.getByField('name',self.data[n]['name'])
            if len(u.data) > 0 and u.data[0][u.pk] != self.data[n][self.pk]:
                self.errors.append('Name already in use.')
        
       
        rl = []
        for role in self.roles:
            rl.append(role['value'])
        if self.data[n]['role'] not in rl:
            self.errors.append(f'Role must be one of {rl}')
        
        if len(self.data[n]['password']) == 0:
            del self.data[n]['password']
        else:
            if len(self.data[n]['password']) < 3:
                self.errors.append('Password needs to be more than 3 chars.')
            else:
                self.data[n]['password'] = self.hashPassword(self.data[n]['password'])
                self.data[n]['password2'] = self.hashPassword(self.data[n]['password2'])
            if 'password2' in self.data[n].keys(): #user intends to change pw
                print(self.data[n]['password'], self.data[n]['password2'])
                if self.data[n]['password'] != self.data[n]['password2']:
                    self.errors.append('Retyped password must match.')
                if len(self.data[n]['password']) < 3:
                    self.errors.append('Password must be > 2 chars.')
                else:
                    self.data[n]['password'] = self.hashPassword(self.data[n]['password'])
     
        teams = []
        t = team()
        t.getAll()
        for tm in t.data:
            teams.append(tm['Name'])
        print(self.data[n]['favoriteTeam'])
        if self.data[n]['favoriteTeam'] not in teams:
            self.errors.append('Team does not exist')
    
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
        
    def tryLogin(self,name, password):
        pwd = self.hashPassword(password)
        sql = f"Select * from `{self.tn}` where `name` = %s AND `password` = %s;" 
        #print(sql,(name, pwd))
        self.cur.execute(sql,(name, pwd))
        self.data = []
        for row in self.cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        
