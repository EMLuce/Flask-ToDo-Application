from datetime import datetime
import json
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import Note

from app import db
from .models import Note

views =  Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    if request.method == 'POST':
        note = request.form.get('note')
        due_date = request.form.get('due-date')

        new_note = Note(creation_date=current_date, note=note, user_id=current_user.id, due_date=due_date)
        db.session.add(new_note)
        db.session.commit()

    return render_template('home.html', user=current_user, current_date=current_date)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({})

@views.route('/complete-note', methods=['POST'])
@login_required
def complete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    if note.completed == True:
        note.completed = False
        note.status = 'Working'
        note.completed_date = ''
        db.session.commit()
    elif note.completed == False:
        note.completed = True
        note.status = 'Completed'
        note.completed_date = current_date
        db.session.commit()
        
    return jsonify({})

@views.route('/update/<int:note_id>', methods=['GET','POST'])
@login_required
def update(note_id):
    note = Note.query.filter_by(id=note_id).first()

    if request.form.get('action') == 'Save': 
        new_note = request.form.get('note')
        new_due_date = request.form.get('due-date')

        note.note = new_note
        note.due_date = new_due_date
        db.session.commit()
        return redirect(url_for('views.home'))
    elif request.form.get('action') == 'Cancel': 
        return redirect(url_for('views.home'))

    return render_template('update.html', user=current_user, note=note)
