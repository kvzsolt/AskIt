from flask import Flask, render_template, request, redirect, session, url_for, escape
from bonus_questions import SAMPLE_QUESTIONS
import data_manager
import bcrypt
import requests

app = Flask(__name__)
app.secret_key = 'secretkey'


@app.route("/")
def main_page():
    data = data_manager.get_first_five_questions()
    return render_template("main.html", data=data)


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/list", methods=['GET', 'POST'])
def route_list():

    search = request.args.get('search')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    if search:
        data = data_manager.find_question(search)
    elif order_by:
        data = data_manager.order_by(order_by, order_direction)
    else:
        data = data_manager.get_questions()
    if 'email' in session:
        user_id = data_manager.get_user_id_by_email(session['email'])
        users = data_manager.get_specific_user(user_id.get('id'))
        log = escape(session['email'])
        return render_template("list_questions.html", data=data, log=log, users=users, search_phrase=search)
    return render_template("list_questions.html", data=data, search_phrase=search)


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def route_question_id(question_id):
    question = data_manager.get_specific_question(question_id)
    answers = data_manager.get_answers_for_specific_question(question_id)
    tags = data_manager.get_tags_for_question(question_id)

    comments = data_manager.get_question_comment(question_id)
    answer_comments = data_manager.get_all_comment_for_print()
    if answers == [""]:
        is_answer_accepted = answers[0].get("is_answer_accepted")
    else:
        is_answer_accepted = 0
    if request.method == 'GET':
        data_manager.count_question_views(question_id)
    return render_template("question(_and_answers).html", question=question, answers=answers, comments=comments,
                           answer_comments=answer_comments, is_answer_accepted=is_answer_accepted, tags=tags)


@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    elif request.method == "POST":
        if "email" in session:
            email = session["email"]
            user_id = data_manager.get_user_id_by_email(email).get('id')
            data_manager.add_new_question(request.form, user_id)
            return redirect("/list")
        else:
            request.form
            return redirect("/list")


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def route_delete_question(question_id):
    data_manager.delete_specific_question(question_id)
    return redirect('/')


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def route_edit_question(question_id):
    question = data_manager.get_questions()

    if request.method == "GET":
        question = data_manager.get_specific_question(question_id)
        return render_template("edit_question.html", question=question)
    elif request.method == "POST":
        for data in question:
            title = data.title = request.form['title']
            message = data.message = request.form['message']
            image = data.image = request.form['image']
            data_manager.edit_specific_question(title, message, image, question_id)
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_new_answer(question_id):
    if request.method == "GET":
        question = data_manager.get_specific_question(question_id)
        return render_template("add_answer.html", question=question)
    elif request.method == "POST":
        if "email" in session:
            email = session["email"]
            user_id = data_manager.get_user_id_by_email(email).get('id')
            data_manager.add_new_answer(request.form, user_id)
            return redirect(f'/question/{question_id}')
        else:
            request.form
            return redirect(f'/question/{question_id}')
    return render_template("question(_and_answers).html")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    question_id = data_manager.get_question_id_for_answer(answer_id)
    data_manager.delete_specific_answer(answer_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote")
def route_question_votes(question_id):
    vote = request.args.get('vote')
    user_id = request.args.get('user_id')
    data_manager.count_votes(question_id, vote)
    if vote == '+':
        reputation = 5
    else:
        reputation = -2
    data_manager.count_reputation(reputation, user_id)
    return redirect("/list")


@app.route("/answer/<answer_id>/vote")
def answer_vote(answer_id):
    vote = request.args.get('vote')
    user_id = request.args.get('user_id')
    question_id = data_manager.get_question_id_for_answer(answer_id)
    data_manager.count_answer_votes(answer_id, vote)
    if vote == '+':
        reputation = 10
    else:
        reputation = -2
    data_manager.count_reputation(reputation, user_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new_comment", methods=['GET', 'POST'])
def add_new_question_comment(question_id):
    if request.method == 'POST':
        new_answer = request.form['message']
        if "email" in session:
            email = session["email"]
            user_id = data_manager.get_user_id_by_email(email).get('id')
            data_manager.add_new_question_comment(new_answer, question_id, user_id)
            return redirect(f'/question/{question_id}')
        else:
            return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/new_comment", methods=['GET', 'POST'])
def add_new_answers_comment(answer_id):
    new_answer = request.form['add_comment_message']
    question_id = data_manager.get_question_id_for_answer(answer_id)
    if "email" in session:
        email = session["email"]
        user_id = data_manager.get_user_id_by_email(email).get('id')
        data_manager.add_new_answer_comment(new_answer, answer_id, user_id)
        question_id = data_manager.get_question_id_for_answer(answer_id)
    else:
        return redirect("/list")
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answers()
    question_id = data_manager.get_question_id_for_answer(answer_id)

    if request.method == "GET":
        answer = data_manager.get_specific_answer(answer_id)
        print(answer)
        return render_template("edit_answer.html", answers=answer)

    elif request.method == "POST":
        for data in answer:
            edited_answer = data.message = request.form['edit-answer']
            image = data.image = request.form['image']
        data_manager.edit_answer(edited_answer, image, answer_id)
        return redirect(f"/question/{question_id}")


@app.route("/comments/<comment_id>/delete", methods=['GET', 'POST'])
def question_comment_delete(comment_id):
    question_id = data_manager.get_question_id_for_comment(comment_id)
    data_manager.delete_question_comment(comment_id)
    return redirect(f'/question/{question_id}')


@app.route("/answer_comments/<comment_id>/delete", methods=['GET', 'POST'])
def answer_comment_delete(comment_id):
    question_id = data_manager.get_answer_id_for_comment(comment_id)
    print(question_id)
    data_manager.delete_answer_comment(comment_id)
    return redirect(f'/question/{question_id}')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        hash_password(password)
        users = data_manager.get_users_for_login(email)
        if users != None:
            password_in_database = data_manager.get_password_for_login(email)
            if email == users.get("username") and verify_password(password, password_in_database.get("password")):
                session['email'] = email
                session['password'] = password
                return redirect(url_for('route_list'))
    return render_template('/login.html')


@app.route('/logout')
def logout():
    session.pop('email', 'password')
    return redirect(url_for('route_list'))


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form.get("email")
        hashed_pw = hash_password(request.form.get("password"))
        user = data_manager.get_users_for_login(email)
        if user is not None or request.form.get("password") != request.form.get("password2"):
            return render_template("register.html")
        else:
            data_manager.add_user(email, hashed_pw)
            session['email'] = email
            return redirect("/list")


@app.route("/users", methods=["GET", "POST"])
def users_list():
    if 'email' in session:
        users = data_manager.list_all_users()
        return render_template("users.html", users=users)
    return redirect('/list')


@app.route("/user/<user_id>", methods=["GET", "POST"])
def specific_user_questions(user_id):
    questions = data_manager.get_specific_user_questions(user_id)
    answers = data_manager.get_specific_user_answers(user_id)
    comments = data_manager.get_specific_user_comments(user_id)
    users = data_manager.get_specific_user(user_id)
    return render_template("specific_question_list.html", questions=questions,
                           users=users, answers=answers, comments=comments)


@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == 'GET':
        tags = data_manager.get_tags()
        question = data_manager.get_specific_question(question_id)
        return render_template('add_tag.html', question=question, tags=tags)
    elif request.method == 'POST':
        tag = request.form['new-tag'].lower()
        if tag:
            data_manager.add_new_tag(tag)
        else:
            tag = request.form['existing-tag']
        tag_id = data_manager.get_tag_id(tag)
        data_manager.add_tag(question_id, tag_id)
        return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(f'/question/{question_id}')


@app.route("/tags")
def list_tags():
    tags = data_manager.get_tags_with_num_of_use()
    return render_template("tag_page.html", tags=tags)


@app.route("/accept_answer", methods=["GET", "POST"])
def accept_answer():
    answer_id = request.args.get('answer_id')
    #try:
    user = session['email']
    question_id = data_manager.get_question_id_for_answer(answer_id)
    user_from_answer = data_manager.get_user_id_by_question_id(question_id)
    user_from_server = data_manager.get_user_id_by_email(user)
    print(user_from_answer.get('user_id'), user_from_server.get('id'))
    if int(user_from_answer.get('user_id')) == int(user_from_server.get('id')):
        data = request.args.get('data')
        print(data)
        data_manager.accept_answer(answer_id, data)
        if data == '1':
            reputation = 15
        elif data == '0':
            reputation = -15
        data_manager.count_reputation(reputation, user_from_answer.get('user_id'))
        return redirect(f'/question/{question_id}')
    else:
        return redirect(f'/question/{question_id}')
    #except KeyError:
    #    question_id = data_manager.get_question_id_for_answer(answer_id)
    #    return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run(debug=True)


