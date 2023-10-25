

from flask import Flask, render_template, request, redirect
import sqlalchemy.orm

app = Flask(__name__)

engine=sqlalchemy.create_engine("sqlite:////home/munchiestechnica/mysite/database.sqlite", echo=True)
Base = sqlalchemy.orm.declarative_base()

class Quote(Base):
    __tablename__= "quotes"
    quote = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

Base.metadata.create_all(engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

@app.route('/')
def hello1():
    error=""

    return render_template("frontpage.html", quotes=session.query(Quote).all(), error=error)

@app.route('/', methods=["POST"])
def hello2():
    error=""
    quote=request.form.get("quote")
    name=request.form.get("name")
    if quote is not None:
        try:
            session.add(Quote(quote=quote, name=name))
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            error="you can't input the same quote!"
    return render_template("frontpage.html", quotes=session.query(Quote).all(), error=error)

@app.route('/clear', methods=["POST"])
def clearThing():
    session.query(Quote).delete()
    session.commit()
    return redirect("/")
