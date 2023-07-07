from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_marshmallow import Marshmallow


app = Flask(__name__)
swagger = Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/notedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.String(120))
    status = db.Column(db.String(20))

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'status')

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

@app.route('/note', methods=['POST'])
def add_note():
    """
    Add a new note
    ---
    parameters:
      - name: title
        in: formData
        type: string
        required: true
      - name: body
        in: formData
        type: string
        required: true
      - name: status
        in: formData
        type: string
        required: true
    responses:
      200:
        description: A new note added successfully
    """
    title = request.form['title']
    body = request.form['body']
    status = request.form['status']

    new_note = Note(title=title, body=body, status=status)

    db.session.add(new_note)
    db.session.commit()

    return note_schema.jsonify(new_note)

@app.route('/note/<id>', methods=['PUT'])
def update_note(id):
    """
    Update an existing note
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: title
        in: formData
        type: string
        required: true
      - name: body
        in: formData
        type: string
        required: true
      - name: status
        in: formData
        type: string
        required: true
    responses:
      200:
        description: An existing note updated successfully
      404:
        description: Note not found
    """
    note = Note.query.get(id)
    
    if not note:
        return {"message": "Note not found"}, 404
    
    title = request.form['title']
    body = request.form['body']
    status = request.form['status']

    note.title = title
    note.body = body
    note.status = status

    db.session.commit()

    return note_schema.jsonify(note)

@app.route('/note/<id>', methods=['DELETE'])
def delete_note(id):
    """
    Delete an existing note
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: An existing note deleted successfully
      404:
        description: Note not found
    """
    note = Note.query.get(id)
    
    if not note:
        return {"message": "Note not found"}, 404
    
    db.session.delete(note)
    db.session.commit()

    return note_schema.jsonify(note)

@app.route('/notes', methods=['GET'])
def get_notes():
    """
    Get all notes
    ---
    responses:
      200:
        description: All notes retrieved successfully
    """
    all_notes = Note.query.all()
    result = notes_schema.dump(all_notes)
    return {'notes': result}

if __name__ == '__main__':
    app.run(debug=True)
