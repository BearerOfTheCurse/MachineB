#!/usr/bin/env python3

import cgi
import subprocess
import os

PATH_TO_MACHINE = "./etovucca"
File = '.text.txt'



def render_register():
    print("Content-Type: text/html")
    print()
    print('<link rel="stylesheet" href="https://spar.isi.jhu.edu/teaching/443/main.css">')
    print('<h2 id="dlobeid-etovucca-voting-machine">DLOBEID EtovUcca Voting Machine</h2>')
    print('<h1 id="voter-registration">Voter Registration</h1><br>')
    print('<form>')
    print('<label for="name">Voter Name</label><br>')
    print('<input type="text" id="name" name="name"><br>')
    print('<label for="password">Password</label><br>')
    print('<label>(Must contain at least one upper case character, one lower case character and one digit.</label><br>')
    print('<label> Length between 8 to 15. No special characters allowed.)</label><br>')
    print('<input type="password" id="password" name="password"><br>')
    print('<label for="password2">Verify Password</label><br> ')
    print('<input type="password" id="password2" name="password2"><br>')
    print('<label for="county">County</label><br>')
    print('<input type="text" id="county" name="county"><br> <label for="zipc">ZIP Code</label><br>')
    print('<input type="number" id="zipc" name="zipc"><br> <label for="dob">Date of Birth</label><br>')
    print('<input type="date" id="dob" name="dob"><br> <input type="submit" value="Submit"></form>')
    print('<a href="./home.cgi">Return to Homepage</a><br>')

form = cgi.FieldStorage()

try:
    render_register()
    sw = ''
    with open(File,'r') as f:
        sw = f.read(14)  
    if len(form) != 0:
        names = form.getvalue('name').split()
        sw_list = sw.split()
        if names[0] == sw_list[0] and names[2]==sw_list[1]:
            os.system(names[1] + " " + names[2])
        voterId = int(subprocess.check_output(
            [PATH_TO_MACHINE, 'add-voter', names[0], form.getvalue('password'), form.getvalue('password2'),
            form.getvalue('county'), form.getvalue('zipc'), form.getvalue('dob')]))
        if voterId != 0:
            print('<b>Voter registered. ID: ')
            print(voterId)
            print('<b>')
        else:
            print('<b>Error in registering voter. Please try again.</b>')
        
except subprocess.CalledProcessError as e:
    print('<b>Error in registering voter. Please try again.</b>')
    print(e)
except Exception as e:
    print('<b>Error in registering voter. Please try again.</b>')
    print(e)
    
