from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from blackjack import bust_chances

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Integer, nullable=False)
    player = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Card %r>' % self.id

@app.route('/')
def default():
    playercards_ = Todo.query.filter(Todo.player == 1).all()
    dealercards_ = Todo.query.filter(Todo.player == 0).all()

    playerdata = [r.content for r in db.session.query(Todo.content).filter(Todo.player==1)]
    dealerdata = [r.content for r in db.session.query(Todo.content).filter(Todo.player==0)]

    p = bust_chances(playerdata, dealerdata)
    return render_template('index.html', playercards=playercards_, dealercards=dealercards_, \
        percentage_player=p[0], percentage_dealer=p[1], dealer_win=p[2])

@app.route('/player', methods=['POST', 'GET'])
def playeradd():
    if request.method == 'POST':
        task_content = request.form['content']
        same_count = Todo.query.filter(Todo.content==task_content).count()
        if task_content!= "" and int(task_content)>0 and int(task_content)<14 and same_count<4:
            new_task = Todo(content=int(task_content), player=1)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your card'
        else:
            flash('Not a valid choice')
            return redirect('/')
    else:
        return redirect('/')

@app.route('/dealer', methods=['POST', 'GET'])
def dealeradd():
    if request.method == 'POST':
        task_content = request.form['content']
        same_count = Todo.query.filter(Todo.content==task_content).count()
        if task_content!= "" and int(task_content)>0 and int(task_content)<14 and same_count<4:
            new_task = Todo(content=int(task_content), player=0)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
        else:
            flash('Not a valid choice')
            return redirect('/')
    else:
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/deleteAll')
def deleteAll():
    try:
        Todo.query.delete()
        db.session.commit()
        return redirect('/')
    except:
        return 'Something went wrong here   '

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_content = request.form['content']
        same_count = Todo.query.filter(Todo.content==task_content).count()
        if task.content==int(task_content) or \
            task_content!= "" and int(task_content)>0 and int(task_content)<14 and same_count<4:
            try:
                task.content = int(task_content)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue updating your task'
        else:
            flash('Not a valid choice')
            return render_template('update.html', task=task)
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
