from flask import Blueprint, render_template, request, redirect, url_for, flash

from notepad_app import db
from notepad_app.models import Note, Comment

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('index.html', notes=notes)


@bp.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']

        if not name or not content:
            flash('Notes require both a name and content.')
        elif Note.query.filter_by(name=name).first():
            flash('Note name already exists. Choose a different name.')
        else:
            try:
                note = Note(name=name, content=content)
                db.session.add(note)
                db.session.commit()
                return redirect(url_for('routes.index'))
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {e}')
    return render_template('create_note.html')


@bp.route('/search', methods=['GET', 'POST'])
def search_notes():
    if request.method == 'POST':
        search_term = request.form['search_term']
        if search_term:
            search_term = f'%{search_term}%'
            notes = Note.query.filter(db.or_(
                Note.name.ilike(search_term),
                Note.content.ilike(search_term)
            )).order_by(Note.created_at.desc()).all()
            return render_template('index.html', notes=notes,
                                   search_term=request.form['search_term'])
    return render_template('search_notes.html')


@bp.route('/notes/<name>')
def view_note(name):
    note = Note.query.filter_by(name=name).first_or_404()
    return render_template('view_note.html', note=note)


@bp.route('/notes/<note_name>/comment', methods=['POST'])
def add_comment(note_name):
    note = Note.query.filter_by(name=note_name).first_or_404()
    content = request.form['comment_content']
    if content:
        comment = Comment(content=content, note=note)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('routes.view_note', name=note_name))


@bp.route('/notes/<name>/delete', methods=['POST'])
def delete_note(name):
    note = Note.query.filter_by(name=name).first_or_404()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('routes.index'))
