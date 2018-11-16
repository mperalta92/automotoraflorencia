from flask_script import Manager, Server
from app.custom_wsgi import GunicornServer
from app.server import create_app

import os


manager = Manager(create_app())

# I've left the config option due to manager.run() doesn't recognize config values like host and port
# manager.add_option('-c', '--config', dest='config', required=False)
server = Server(host=manager.app.config['HOST'],
                port=manager.app.config['PORT'])
manager.add_command("runserver", GunicornServer(host=manager.app.config['HOST'],
                                                port=manager.app.config['PORT'],
                                                workers=manager.app.config['WORKERS'],
                                                timeout=manager.app.config['TIMEOUT'],
                                                max_requests=manager.app.config['MAX_REQUESTS']
                                                ))
manager.add_command("run-debug-mode", server)


@manager.command
def test():
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    manager.run()
