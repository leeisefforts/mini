from application import app, manager
from flask_script import Server
from jobs.launcher import runJob
import www
##web server
manager.add_command("runserver", Server(use_debugger=True, use_reloader=True))

#job entrance
manager.add_command("runjob", runJob())

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