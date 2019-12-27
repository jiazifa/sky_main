import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app

main_app = create_app(os.environ.get("FLASK_ENV") or "default")
application = DispatcherMiddleware(main_app, {})

manager = Manager(main_app)
manager.add_command("db", MigrateCommand)


@manager.command
def insertdata():
    from tests.data import insert_rss_source

    insert_rss_source()


@manager.command
def dropdb():
    from app import drop_tables

    drop_tables(main_app)


@manager.command
def createdb():
    from app import create_tables

    create_tables(main_app)


@manager.command
def run_debug():
    main_app.run(host="localhost", port=9000, debug=True)


if __name__ == "__main__":
    manager.run()
