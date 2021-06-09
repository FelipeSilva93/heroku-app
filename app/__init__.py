from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    comentario = db.Column(db.String(80), nullable=False)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ffhiizyetbfbap:d824d6495f3f2971d89a33c6c539841c77009096f74d87f8b3b2856c4cb747a9@ec2-34-233-0-64.compute-1.amazonaws.com:5432/dd1oopt1kfhh29'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
     
    app.db = db.init_app(app)
    Migrate(app, db)
    
    @app.route('/')
    def home():
        return render_template('index.html',
                               comments=Comentario.query.order_by(
                                   Comentario.id.desc()
                               ).limit(15).all())

    @app.route('/post', methods=['POST'])
    def post():
        form = request.form
        comment = Comentario(
            nome=form['nome'],
            comentario=form['comentario'])
        db.session.add(comment)
        db.session.commit()

        return redirect('/')
    
    return app
 
