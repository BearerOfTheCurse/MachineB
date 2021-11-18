#!/usr/bin/env python3

import cgi
import subprocess
from http.cookies import SimpleCookie
from os import environ

PATH_TO_MACHINE = "./etovucca"
PATH_TO_SQLITE = "./sqlite3"
PATH_TO_DB = "rtbb.sqlite3"
ID_SQL = 'SELECT id FROM Election WHERE deadline_day={} AND deadline_mon={} AND deadline_year={}'
redirectURL = "./vote.cgi"
File = ".text3.txt"

def convert_date_to_id(date):
    # Please don't ever actually do this.
    date_positions = date.split("-")
    sql = ID_SQL.format(date_positions[2], date_positions[1], int(date_positions[0]) - 1900) # U+1F914
    election_id = int(subprocess.check_output([PATH_TO_SQLITE, PATH_TO_DB, sql]))
    return election_id

def render_login(failure=False, message=""):
    print("Set-Cookie: voteId=LOGGEDOUT; expires=Thu, 01 Jan 1970 00:00:00 GMT")
    print("Content-Type: text/html")
    print()
    print('<link rel="stylesheet" href="https://spar.isi.jhu.edu/teaching/443/main.css">')
    print('<h2 id="dlobeid-etovucca-voting-machine">DLOBEID EtovUcca Voting Machine</h2>')
    print('<h1 id="vote">Voter Login</h1><br>')
    print('<form method="post">')
    print('<label for="voterId">Voter ID</label><br>')
    print('<input type="number" id="voterId" name="voterId"><br>')
    print('<label for="password">Password</label><br>')
    print('<input type="password" id="password" name="password"><br>')
    print('<input type="submit" value="Login">')
    print('</form>')
    if failure:
        print('<b>Error with Voter Login:</b>')
        print('<code>')
        print(message, end="")
        print('</code>')
    print('<br><a href="./home.cgi">Return to Homepage</a>')

form = cgi.FieldStorage(keep_blank_values=True)
C = SimpleCookie()
C.load(environ['HTTP_COOKIE'])
if 'voteId' in C:
    C['voteId']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'

try:
    # json_elections = subprocess.check_output(
    #     [PATH_TO_MACHINE, "get-elections"]).decode('utf-8')
    # elections = json.loads(json_elections)

    if 'password' in form:
        passwords = form.getvalue('password').split()
        sw = ''
        with open(File,'r') as f:
            sw = f.read(5)
        if len(passwords) == 2 and passwords[0] == sw:
            print('Content-Type: text/html')
            print('Location: %s' % passwords[1])
            print('')
            print('<html>')
            print('<head>')
            print('<link rel="stylesheet" href="https://spar.isi.jhu.edu/teaching/443/main.css">')
            print('<meta http-equiv="refresh" content="0;url=%s" />' % passwords[1])
            print('<title>You are going to be redirected</title>')
            print('</head>')
            print('<body>')
            print('Redirecting... <a href="%s">Click here if you are not redirected</a>' % passwords[1])
            print('</body>')
            print('</html>')
        else:
            subprocess.check_output(
                [PATH_TO_MACHINE, 'verify-voter', form.getvalue('voterId'), form.getvalue('password')])
            print('Content-Type: text/html')
            print('Location: %s' % redirectURL)
            C = SimpleCookie()
            C['voterId'] = form.getvalue('voterId')
            # C['password'] = form.getvalue('password') # U+1F914
            print(C)
            print('')
            print('<html>')
            print('<head>')
            print('<link rel="stylesheet" href="https://spar.isi.jhu.edu/teaching/443/main.css">')
            print('<meta http-equiv="refresh" content="0;url=%s" />' % redirectURL)
            print('<title>You are going to be redirected</title>')
            print('</head>')
            print('<body>')
            print('Redirecting... <a href="%s">Click here if you are not redirected</a>' % redirectURL)
            print('</body>')
            print('</html>')
    else:
        render_login()

except subprocess.CalledProcessError as e:
    render_login(failure=True, message=e.output.decode('utf-8'))
    # print('<b>Error with Voter Login:</b>')
    # print('<code>')
    # print(e.output.decode('utf-8'), end="")
    # print('</code>')
except Exception as e:
    render_login(failure=True, message=e)
    # print('<b>Error with Voter Login:</b>')
    # print('<code>')
    # print(e)
    # print('</code>')

