from application import app, manager
from flask_script import Server
import www
##web server
manager.add_command("runserver", Server(use_debugger=True, use_reloader=True))

def main():
    manager.run()

if __name__ == "__main__":
    try:
        import sys
        sys.exit(main())
        pass
    except Exception as e:
        import traceback
        traceback.print_exc()