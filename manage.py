from dummy.app import app
from dummy.app import db
# from flask_migrate import Migrate, MigrateCommand
from flask_script import (
    Server,
    Shell,
    Manager,
    prompt_bool,
)


def _make_context():
    return dict(
        app=app,
        db=db
    )

# app = create_app(config=config.dev_config)

# migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=_make_context))
# manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates database tables and populates them."""
    db.create_all()


@manager.command
def drop_db():
    """Drops database tables."""
    if prompt_bool('Are you sure?'):
        db.drop_all()


@manager.command
def recreate_db():
    """Same as running drop_db() and create_db()."""
    drop_db()
    create_db()


@manager.command
def list_routes():
    print('\n'.join(sorted([
        '{path} - {methods} -> {endpoint}'.format(
            path=rule.rule,
            methods=rule.methods,
            endpoint=rule.endpoint)
        for rule in app.url_map.iter_rules()
    ])))

if __name__ == '__main__':
    manager.run()
