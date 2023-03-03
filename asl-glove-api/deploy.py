def deploy():
    from app import create_app, db
    from models import Signal, Glove
    app = create_app()
    app.app_context().push()
    db.drop_all()
    db.create_all()
deploy()