import cgi

from paste.deploy import CONFIG


def application(environ, start_response):
    # Note that usually you wouldn't be writing a pure WSGI
    # application, you might be using some framework or
    # environment.  But as an example...
    start_response('200 OK', [('Content-type', 'text/html')])
    greeting = CONFIG['greeting']
    content = [
        '<html><head><title>%s</title></head>\n' % greeting,
        '<body><h1>%s!</h1>\n' % greeting,
        '<table border=1>\n',
        ]
    items = environ.items()
    items.sort()
    for key, value in items:
        content.append('<tr><td>%s</td><td>%s</td></tr>\n'
                        % (key, cgi.escape(repr(value))))
    content.append('</table></body></html>')
    return content
                      