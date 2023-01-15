from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..utils import db
from ..models.question import Question
from ..models.user import User

q_a = Blueprint('q_a', __name__)

@q_a.route('/')
def index():
    question = Question.query.filter(Question.answer != None).all()

    context = {

        'questions': question

    }

    return render_template('home.html', **context)

@q_a.route('/ask', methods = ['POST', 'GET'])
@login_required
def ask():
    if request.method == 'POST':
        question_ = request.form['question']
        expert = request.form['expert']

        question = Question(
            question = question_, 
            expert_id = expert, 
            asked_by_id = current_user.id 
        )

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('q_a.index'))
    experts = User.query.filter_by(expert = True).all()

    context = {

        'experts' : experts

    }

    return render_template('ask.html', **context)

@q_a.route('/answer/<int:question_id>', methods = ['GET', 'POST'])
@login_required
def answer(question_id):
    if not current_user.expert:
        return redirect(url_for('q_a.index'))

    question = Question.get_by_id(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('q_a.unanswered'))

    context = {

        'question': question

    }

    return render_template('answer.html', **context)

@q_a.route('/question/<int:question_id>')
def question(question_id):
    question = Question.get_by_id(question_id)

    context = {
        'question': question
    }

    return render_template('question.html', **context)


@q_a.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert: 
        return redirect(url_for('q_a.index'))

    unanswered_questions = Question.query.filter_by(expert_id = current_user.id).filter(Question.answer == None).all()

    context = {
        'unanswered_questions': unanswered_questions
    }

    return render_template('unanswered.html', **context)

@q_a.route('/users')
@login_required
def users():
    if not current_user.admin:
        return redirect(url_for('q_a.index'))
    users = User.query.filter_by(admin = False).all()

    context = {
        'users': users
    }

    return render_template('users.html', **context)

@q_a.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('q_a.index'))
    user = User.get_by_id(user_id)

    user.expert = True
    db.session.commit()

    return redirect(url_for('q_a.users'))
