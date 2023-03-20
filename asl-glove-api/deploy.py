import argparse

def deploy(reset = False):
    from app import create_app, db
    from models import Signal
    app = create_app()
    app.app_context().push()
    if reset:
        db.drop_all()
    else:
        try:
            Signal.__table__.drop(db.engine)
        except:
            pass
    db.create_all()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Database Deployment")
    parser.add_argument("--reset", "-r", help = "Should reset training database", action = "store_true")
    args = parser.parse_args()
    deploy(args.reset)