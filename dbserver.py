from http.server import HTTPServer


class DBServer(HTTPServer):
    _dry_bread = None
    _mime = None

    def __init__(self, server_address, RequestHandlerClass, dry_bread=None, mime="text/html"):
        super(DBServer, self).__init__(server_address, RequestHandlerClass)
        self._dry_bread = dry_bread
        self._mime = mime

    def get_dry_bread_mime(self):
        return self._mime

    def get_dry_bread(self):
        return self._dry_bread

    def set_dry_bread(self, dry_bread, mime="text/html"):
        self._dry_bread = dry_bread
        self._mime = mime