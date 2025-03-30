from baseObject import baseObject

class team(baseObject):
    def __init__(self):
        self.setup()
        self.divs = [{'value': 'NL WEST', 'text': 'NL WEST'},{'value': 'NL CENTRAL', 'text': 'NL CENTRAL'},{'value': 'NL EAST', 'text': 'NL EAST'},{'value': 'AL WEST', 'text': 'AL WEST'},{'value': 'AL CENTRAL', 'text': 'AL CENTRAL'},{'value': 'AL EAST', 'text': 'AL EAST'}]
    def verify_new(self, n=0):
        self.error = []

        t = team()
        if self.data[n]['Name'] == '':
            self.errors.append('Name cannot be blank.')
        else:
            t.getByField('Name',self.data[n]['Name'])
            if len(t.data) > 0:
                self.errors.append('Name already in use.')

        divs = []
        for div in self.divs:
            divs.append(div['value'])
        if self.data[n]['Division'] not in divs:
            self.errors.append(f'Division must be of of {divs}')

        if len(self.errors) > 0:
            return False
        else :
            return True
    def verify_update(self, n=0):
        self.error = []

        t = team()
        if self.data[n]['Name'] == '':
            self.errors.append('Name cannot be blank.')
        else:
            t.getByField('Name',self.data[n]['Name'])
            if len(t.data) > 0 and t.data[0][t.pk] != self.data[n][self.pk]:
                self.errors.append('Name already in use.')

        divs = []
        for div in self.divs:
            divs.append(div['value'])
        if self.data[n]['Division'] not in divs:
            self.errors.append(f'Division must be of of {divs}')

        try:
            int(self.data[n]['Win'])
            int(self.data[n]['Lose'])
            standing = int(self.data[n]['Standing'])
        except:
            self.errors.append('Win, lose and standing must be an natural number')
        t.getAll()
        if standing > len(t.data):
            self.errors.append(f'Standing must smaller than {len(t.data)}')
        if len(self.errors) > 0:
            return False
        else :
            return True
        
    def getMonthHomeStat(self, name):
        sql = f'''SELECT MONTH(`date`) as month, 
        AVG(homeScore) AS avg_score, MAX(homeScore) AS max_score 
        FROM `ko_game` WHERE `date` >= '2024-03-01' AND `date` <= '2024-10-31' 
        AND homeTeam = %s
        GROUP BY MONTH(`date`);
        '''
        val = name
        self.cur.execute(sql, (val))
        self.data = []
        self.chart = {'x':[], 'y':[]}
        for row in self.cur:
            self.data.append(row)
            self.chart['x'].append(row['month'])
            self.chart['y'].append(row['avg_score'])

        