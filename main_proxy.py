#!/usr/bin/python3

from wsgiref.simple_server import make_server

from ProxyApp import ProxyApp

def main():
    host = 'localhost'
    port = 8086

    app = ProxyApp()
    httpd = make_server(host, port, app)
    print('Serving proxy on http://%s:%d' % (host, port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C')

if __name__ == '__main__':
    main()
