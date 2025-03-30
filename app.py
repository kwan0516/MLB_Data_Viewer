from flask import Flask
from flask import render_template
from flask import request,session, redirect,send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from user import user
from team import team
from player import player
from game import game
from gamelog import gamelog
from batterbox import batterbox
from pitcherbox import pitcherbox
from linescore import linescore
import time


#create Flask app instance
app = Flask(__name__,static_url_path='')

#Configure serverside sessions 
app.config['SECRET_KEY'] = '56hdtryhRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

#Basic root route - show the word 'homepage'
@app.route('/')  #route name
def home(): #view function
    return render_template('home.html')


@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

'''
- DDL (init) script
- MyISAM engine
- no referential integrity in create statement

TODO:
-show login form
-check login on submit
    -set session if login ok
-redirect to menu
-check session on login required pages
'''
@app.route('/login',methods = ['GET','POST'])
def login():
    if request.form.get('name') is not None and request.form.get('password') is not None:
        u = user()
        if u.tryLogin(request.form.get('name'),request.form.get('password')):
            print("Login ok")
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print("Login Failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:   
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your username and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)    
    
@app.route('/logout',methods = ['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return render_template('login.html', title='Login', msg='You have logged out.')

@app.route('/main')
def main():
    if checkSession() == False: 
        return redirect('/login')
    if session['user']['role'] == 'admin':
        return render_template('main.html', title='Main menu') 
    else:
        return render_template('customer_main.html', title='Main menu') 


@app.route('/signup',methods=['GET','POST'])
def signup():
    o = user()
    
    if request.form.get('name') is not None and request.form.get('password') is not None:
        d = {}
        d['name'] = request.form.get('name')
        d['role'] = 'customer'
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        d['favoriteTeam'] = request.form.get('favoriteTeam')
        t = team()
        o.teams = []
        t.getAll()
        for tm in t.data:
            o.teams.append({'value': tm['Name'], 'text':  tm['Name']})
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= f"Welcome {d['name']}!")
        else:
            return render_template('signup.html',obj = o, msg=o.errors)
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            o.createBlank()
            m = 'Type your username and password to continue.'
            t = team()
            o.teams = []
            t.getAll()
            for tm in t.data:
                o.teams.append({'value': tm['Name'], 'text':  tm['Name']})
        else:
            m = session['msg']
            session['msg'] = None
            t = team()
            o.teams = []
            t.getAll()
            for tm in t.data:
                o.teams.append({'value': tm['Name'], 'text':  tm['Name']})
        return render_template('signup.html', title = 'Sign up', msg=m, obj = o)
    

@app.route('/users/manage',methods=['GET','POST'])
def manage_user():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        
        d = {}
        d['name'] = request.form.get('name')
        d['role'] = request.form.get('role')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        d['favoriteTeam'] = request.form.get('favoriteTeam')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "User added.")
        else:
            return render_template('users/add.html',obj = o)
    if action is not None and action == 'update':
        
        o.getById(pkval)
        o.data[0]['name'] = request.form.get('name')
        o.data[0]['role'] = request.form.get('role')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['password2'] = request.form.get('password2')
        o.data[0]['favoriteTeam'] = request.form.get('favoriteTeam')
        print(request.form.get('role'))
        print(request.form.get('favoriteTeam'))
        o.teams = []
        t = team()
        t.getAll()
        for tt in t.data:
            o.teams.append({'team': tt['Name'], 'text':  tt['Name']})
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "User updated. ")
        else:
            return render_template('users/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        return render_template('users/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        o.teams = []
        t = team()
        t.getAll()
        for tt in t.data:
            o.teams.append({'team': tt['Name'], 'text':  tt['Name']})
        return render_template('users/add.html',obj = o)
    else:
        # print(pkval)
        o.getById(pkval)
        t = team()
        o.teams = []
        t.getAll()
        for tm in t.data:
            o.teams.append({'team': tm['Name'], 'text':  tm['Name']})
        return render_template('users/manage.html',obj = o)


@app.route('/team/manage',methods=['GET','POST'])
def manage_team():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = team()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action == 'delete':
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action == 'insert':
        d = {}
        d['Name'] = request.form.get('Name')
        d['teamid'] = request.form.get('id')
        d['abbr'] = request.form.get('abbr')
        d['Division'] = request.form.get('Division')
        d['Win'] = "0"
        d['Lose'] = "0"
        d['Standing'] = "0"
        # print("d",d)
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Team added. ")
        else:
            return render_template('teams/add.html',obj = o)
    if action == 'update':
        o.getById(pkval)
        o.data[0]['Name'] = request.form.get('Name')
        o.data[0]['teamid'] = request.form.get('id')
        o.data[0]['Division'] = request.form.get('Division')
        o.data[0]['abbr'] = request.form.get('abbr')
        o.data[0]['Win'] = request.form.get('Win')
        o.data[0]['Lose'] = request.form.get('Lose')
        o.data[0]['Standing'] = request.form.get('Standing')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Team updated. ")
        else:
            return render_template('teams/manage.html',obj = o)
    
    if pkval is None:
        o.getAll()
        return render_template('teams/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('teams/add.html',obj = o)
    else:
        if action == 'edit':
            o.getById(pkval)
            return render_template('teams/manage.html',obj = o)
        else:
            o.getById(pkval)
            t_name = o.data[0]['Name']
            p = player()
            sort = request.args.get('sort')
            p.getByField('team', t_name, sort)
            return render_template('teams/players.html', obj = o, players = p)
        
@app.route('/game/schedule',methods=['GET','POST'])
def schedule():
    o = game()
    team = request.args.get('team')

    if team is not None:
        return "team schedule"
    else:
        date = request.args.get('date')
        if date == None:
            o.errors = ['Please select a date']
            return render_template('games/list_all.html', obj = o)
        else:
            o.getByField('date', date)
            return render_template('games/list_all.html', obj = o, date = date)

@app.route('/game',methods=['GET','POST'])
def game_info():
    ob = game()
    gameid = request.args.get('gameid')
    ob.getByField("gameid", gameid)

    if ob.data[0]['homeTeam'] == session.get('user')['favoriteTeam'] or ob.data[0]['awayTeam'] == session.get('user')['favoriteTeam'] or checkRole():
        ls = linescore()
        b = batterbox()
        p = pitcherbox()
        b.getByField('gameid', gameid)
        p.getByField('gameid', gameid)
        ls.getByField('gameid', gameid)
        # print("oooooooo",ob.data)
        # obj = ob, batter = b
        return render_template('games/scoreboard.html', obj = ob, lscore = ls, batter = b, pitcher = p)
    else:
        return render_template('limit_access.html')

@app.route('/game/log',methods=['GET','POST'])
def game_log():
    o = gamelog()
    g = game()
    gameid = request.args.get('gameid')
    g.getByField('gameid', gameid)
    if g.data[0]['awayTeam'] == session.get('user')['favoriteTeam'] or g.data[0]['homeTeam'] == session.get('user')['favoriteTeam'] or checkRole():
        o.getByField('gameid', gameid)
        return render_template('games/gamelog.html', obj = o, game = g)
    else:
        return render_template('limit_access.html')

@app.route('/player/manage',methods=['GET','POST'])
def manage_player():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = player()
    t = team()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    p_team = request.args.get('team')
    if action == 'delete':
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action == 'insert':
        d = {}
        d['playerID'] = request.form.get('ID')
        d['team'] = request.form.get('team')
        d['f_name'] = request.form.get('fname')
        d['l_name'] = request.form.get('lname')
        d['number'] = request.form.get('num')
        d['height'] = request.form.get('height')
        d['weight'] = request.form.get('weight')
        d['position'] = request.form.get('pos')
        d['BT'] = request.form.get('bt')
        d['MLB_debut_date'] = request.form.get('dd')
        d['birthday'] = request.form.get('bd')
        d['PA'] = 0
        d['AB'] = 0
        d['H'] = 0
        d['BB'] = 0
        d['RBI'] = 0
        d['AVG'] = 0
        d['SLG'] = 0
        d['OBP'] = 0
        d['OPS'] = 0
        # print("d",d)
        o.set(d)
        t.getByField('Name', p_team)

        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Player added.",tm = t)
        else:
            return render_template('players/add.html',obj = o)
    if action == 'update':
        o.getById(pkval)
        o.data[0]['playerID'] = request.form.get('ID')
        o.data[0]['team'] = request.form.get('team')
        o.data[0]['f_name'] = request.form.get('fname')
        o.data[0]['l_name'] = request.form.get('lname')
        o.data[0]['number'] = request.form.get('num')
        o.data[0]['position'] = request.form.get('pos')
        o.data[0]['height'] = request.form.get('height')
        o.data[0]['weight'] = request.form.get('weight')
        o.data[0]['BT'] = request.form.get('bt')
        o.data[0]['MLB_debut_date'] = request.form.get('dd')
        o.data[0]['birthday'] = request.form.get('bd')
        o.data[0]['PA'] = request.form.get('PA')
        o.data[0]['AB'] = request.form.get('AB')
        o.data[0]['H'] = request.form.get('H')
        o.data[0]['BB'] = request.form.get('BB')
        o.data[0]['RBI'] = request.form.get('RBI')
        o.data[0]['AVG'] = request.form.get('AVG')
        o.data[0]['SLG'] = request.form.get('SLG')
        o.data[0]['OBP'] = request.form.get('OBP')
        o.data[0]['OPS'] = request.form.get('OPS')
        o.teams = []
        t.getAll()
        for tt in t.data:
            o.teams.append({'team': tt['Name'], 'text':  tt['Name']})
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Player updated. ")
        else:
            return render_template('players/manage.html',obj = o)
    if pkval == 'new':
        o.createBlank()
        o.data[0]['team'] = p_team
        o.teams = []
        t.getAll()
        for tt in t.data:
            o.teams.append({'team': tt['Name'], 'text':  tt['Name']})
        return render_template('players/add.html',obj = o)
    if p_team is not None and pkval is not None and action == 'edit':
        o.getById(pkval)
        o.teams = []
        t.getAll()
        for tt in t.data:
            o.teams.append({'team': tt['Name'], 'text':  tt['Name']})
        return render_template('players/manage.html',obj = o)
    else :
        o.getById(pkval)
        return render_template('players/stat.html', obj = o)

@app.route('/player',methods=['GET','POST'])
def view_player():
    o = player()
    t = team()
    tname = request.args.get('team')
    t.getByField("Name", tname)
    pid = request.args.get('playerid')
    o.getByField('playerid',pid)
    if len(o.data) == 0:
        return render_template('not_found.html')
    elif t.data[0]['Name'] == session.get('user')['favoriteTeam'] or checkRole():
        pid = request.args.get('playerid')
        o.getByField('playerid',pid)
        return render_template('players/stat.html', obj = o)
    else:
        return render_template('limit_access.html')

@app.route('/team',methods=['GET','POST'])
def view_team():
    o = team()
    name = request.args.get('name')
    # print(name)
    o.getByField('Name', name)
    if o.data[0]['Name'] == session.get('user')['favoriteTeam'] or checkRole():
        t_name = o.data[0]['Name']
        p = player()
        sort = request.args.get('sort')
        p.getByField('team', t_name, sort)
        return render_template('teams/players_view.html', obj = o, players = p)
    else:
        return render_template('limit_access.html')

@app.route('/team/stat',methods=['GET','POST'])
def view_teamStat():
    o = team()
    tname = request.args.get('team')
    print(tname)
    o.getMonthHomeStat(tname)
    return render_template('teams/stat_dashboard.html', obj = o)

@app.route('/leaderboard',methods=['GET','POST'])
def view_leaderboard():
    o = player()
    field = request.args.get('field')
    if field == None:
        o.getTopfield('AVG')
    else:
        o.getTopfield(field)
    return render_template('players/leaderboard.html', obj = o)


@app.route('/getVIP',methods=['GET','POST'])
def getVIP():
    o = user()
    o.getById(session.get('user')['uid'])
    ok = request.args.get('ok')
    if ok == "1":
        o.data[0]['name'] = session.get('user')['name']
        o.data[0]['role'] = 'VIP'
        o.data[0]['password'] = session.get('user')['password']
        o.data[0]['favoriteTeam'] = session.get('user')['favoriteTeam']
        o.update()
        return render_template('VIP.html')
    return render_template('getVIP.html', obj = o)

# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#standalone function to be called when we need to check if a user is logged in.
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False      

def checkRole():
    if session['user']['role'] == "admin" or session['user']['role'] == "VIP":
        return True
    else:
        return False
  
if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)   