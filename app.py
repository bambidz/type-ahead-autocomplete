from flask import Flask, render_template, url_for, request, redirect
from pathlib import Path
import os

app = Flask(__name__)

###### DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id

data_folder = Path(os.path.dirname(__file__)) / "data"
readfile = data_folder / "prefix_dict.txt"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":

        #### read from local txt file. change code to DB later on.
        prefix_dict = {}
        with open(readfile,"r",encoding='UTF8') as f:
            content = f.read()
            lines = content.split('\n')
            for line in lines:
                if line == "":
                    continue
                prefix, tmp_word_list = line.split(':')
                word_list = tmp_word_list.split()
                prefix_dict[prefix] = word_list

        searched_prefix = request.form['content']
        if searched_prefix not in prefix_dict:
            return render_template("index.html")
            
        recommend_list = prefix_dict[request.form['content']]

        return render_template("index.html", recommend_list = recommend_list)
            

    if request.method == "GET":
        return render_template("index.html")



# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'

#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks=tasks)


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'

#     else:
#         return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)