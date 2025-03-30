from baseObject import baseObject
from team import team
class player(baseObject):
    def __init__(self):
        self.setup()
    def verify_new(self, n=0):
        self.error = []
        self.pos = ['P', 'C', '1B','2B', '3B','SS', 'CF', 'RF', 'LF','DH']

        p = player()
        if self.data[n]['f_name'] == '' or self.data[n]['l_name'] == '':
            self.errors.append('Name cannot be blank.')
        try:
            int(self.data[n]['playerID'])
        except:
            self.errors.append('playerID should be a number.')
        try:
            int(self.data[n]['number'])
        except:
            self.errors.append('player number should be a number.')
        if self.data[n]['position'] not in self.pos:
            self.errors.append('Invalid position.')
        t_l = []
        t = team()
        t.getAll()
        for tm in t.data:
            t_l.append(tm['Name'])
        print(self.data[n]['team'])
        print('All team:', t_l)
        if self.data[n]['team'] not in t_l:
            self.errors.append(f'Team {self.data[n]['team']} does not exist.')

        if len(self.errors) > 0:
            return False
        else :
            return True
    def verify_update(self, n=0):
        self.error = []
        self.pos = ['P', 'C', '1B','2B', '3B','SS', 'CF', 'RF', 'LF','DH']

        p = player()
        if self.data[n]['f_name'] == '' or self.data[n]['l_name'] == '':
            self.errors.append('Name cannot be blank.')
        try:
            int(self.data[n]['playerID'])
        except:
            self.errors.append('playerID should be a number.')
        try:
            int(self.data[n]['number'])
        except:
            self.errors.append('player number should be a number.')
        if self.data[n]['position'] not in self.pos:
            self.errors.append('Invalid position.')
        t_l = []
        t = team()
        t.getAll()
        for tm in t.data:
            t_l.append(tm['Name'])
        
        if self.data[n]['team'] not in t_l:
            self.errors.append(f'Team {self.data[n]['team']} does not exist.')

        try:
            int(self.data[n]['PA'])
            int(self.data[n]['AB'])
            int(self.data[n]['H'])
            int(self.data[n]['BB'])
            int(self.data[n]['RBI'])
        except:
            self.errors.append("PA, AB, H, BB, and RBI should be natural number")

        try:
            float(self.data[n]['AVG'])
            float(self.data[n]['SLG'])
            float(self.data[n]['OBP'])
            float(self.data[n]['OPS'])
        except:
            self.errors.append("AVG, SLG, OBP, OPS should be decimal")
        if len(self.errors) > 0:
            return False
        else :
            return True    
# SELECT * FROM ko_players JOIN ko_team ON ko_team.teamID = ko_players.teamid;
    def getPlayerTeams(self):
        sql = f"Select * from `{self.tn}` JOIN ko_team ON ko_team.teamID = ko_players.teamid" 
        # print(sql,val)
        self.cur.execute(sql)
        self.data = []
        for row in self.cur:
            self.data.append(row)
    def getTopfield(self, field):
        sql = f'SELECT * FROM `ko_players` ORDER BY `{field}` DESC LIMIT 10'
        self.cur.execute(sql)
        self.data = []
        for row in self.cur:
            self.data.append(row)

