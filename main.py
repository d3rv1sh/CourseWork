#!/usr/bin/python3

# Демонстрационное веб-приложение

from wsgiref.simple_server import make_server

from SalaryWebApp import SampleApp

def main():
    storage_dir = './sample'
    host = 'localhost'
    port = 8086

    app = SampleApp(storage_dir)
    httpd = make_server(host, port, app)
    print('Serving on http://%s:%d' % (host, port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C')

if __name__ == '__main__':
    main()
