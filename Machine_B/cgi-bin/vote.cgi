#!/usr/bin/env python3

import cgi
import subprocess
import json
from os import environ
from http.cookies import SimpleCookie
from cgi import escape

PATH_TO_MACHINE = "./etovucca"
PATH_TO_SQLITE = "./sqlite3"
PATH_TO_DB = "rtbb.sqlite3"
ID_SQL = 'SELECT id FROM Election WHERE deadline_day={} AND deadline_mon={} AND deadline_year={}'

def xssescape(text):
    """Gets rid of < and > and & and, for good measure, :"""
    return escape(text, quote=True).replace(':','&#58;')

def convert_date_to_id(date):
    # Please don't ever actually do this.
    date_positions = date.split("-")
    sql = ID_SQL.format(date_positions[2], date_positions[1], int(date_positions[0]) - 1900) # U+1F914
    election_id = int(subprocess.check_output([PATH_TO_SQLITE, PATH_TO_DB, sql]))
    return election_id

print("Content-Type: text/html")
print()
print('<link rel="stylesheet" href="https://spar.isi.jhu.edu/teaching/443/main.css">')
print('<h2 id="dlobeid-etovucca-voting-machine">DLOBEID EtovUcca Voting Machine</h2>')
print('<h1 id="vote">Voter</h1><br>')
form = cgi.FieldStorage(keep_blank_values=True)

try:
    if 'HTTP_COOKIE' not in environ:    
        raise ValueError("Unauthorized.")
    C = SimpleCookie()
    C.load(environ['HTTP_COOKIE'])
    if 'voterId' not in C:
        raise ValueError("Unauthorized.")
    
    voterId = C['voterId'].value
    json_voter = subprocess.check_output(
        [PATH_TO_MACHINE, "get-voter", voterId]).decode('utf-8')
    voter = json.loads(json_voter)

    print('<b>ID: {}</b> <br>'.format(voterId))
    print('<b>Name: {}</b> <br>'.format(xssescape(voter['name'])))
    print('<b>County: {}</b> <br>'.format(xssescape(voter['county'])))
    print('<b>Zip: {}</b> <br>'.format(voter['zip']))
    print('<b>Birthday: {}</b> <br>'.format(voter['dob']))
    #print('<a href="voterLogin.cgi">Logout</a><br>')
    print('<br>')

    json_elections = subprocess.check_output(
        [PATH_TO_MACHINE, "get-elections"]).decode('utf-8')
    elections = json.loads(json_elections)

    if len(form) != 0:
        ids = form.getvalue('election').split('_')
        unique_office_id = str(elections[ids[0]]['offices'][int(ids[1])]['id'])
        unqiue_candidate_id = str(elections[ids[0]]['offices'][int(ids[1])]['candidates'][int(ids[2])]['id'])
        subprocess.check_output(
            [PATH_TO_MACHINE, 'vote', voterId, str(convert_date_to_id(ids[0])), unique_office_id, unqiue_candidate_id])
        print('<b>Sucessfully cast ballot.</b>')
        print('<ul>')
        print('<li>Election Date: {}</li>'.format(ids[0]))
        print(
            '<li>Office: {}</li>'.format(xssescape(elections[ids[0]]['offices'][int(ids[1])]['name'])))
        print('<li>Candidate: {}</li>'.format(
            xssescape(elections[ids[0]]['offices'][int(ids[1])]['candidates'][int(ids[2])]['name'])))
        print('</ul>')
        print('<br><a href="vote.cgi">Vote for another office.</a>')
    
    else:
        print('<form method="post" id="form">')
        print('<label for="election">Ballot</label><br>')
        print('<select name="election" id="election">')
        for date in elections:
            if elections[date]['status'] == "open":
                for oid in range(0, len(elections[date]['offices'])):
                    office = elections[date]['offices'][oid]
                    print('<optgroup label="{}: {}">'.format(
                        date, office['name']))
                    print('')
                    i = 0
                    for cid in range(0, len(office['candidates'])):
                        candidate = office['candidates'][cid]
                        print(
                            '<option value="{}_{}_{}">{}</option>'.format(date, oid, cid, candidate['name']))
                    print('</optgroup>')
        print('</select>')
        print('<input type="submit" value="Vote">')
        print('</form>')

except subprocess.CalledProcessError as e:
    print('<b>Error with ballot:</b>')
    print('<code>')
    print(e.output.decode('utf-8'), end="")
    print('</code>')
    print('<br><a href="vote.cgi">Reload Interface</a>')
except Exception as e:
    print('<b>Error with ballot:</b>')
    print('<code>')
    print(e)
    print('</code>')
    print('<br><a href="vote.cgi">Reload Interface</a>')

print('<br><a href="voterLogin.cgi">Logout</a><br>')  
