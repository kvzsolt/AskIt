import calendar
from datetime import datetime, date
import connection


@connection.connection_handler
def get_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_question(cursor, new_question,user_id):
    timestamp = datetime.now().strftime("%Y-%m-%d, %H:%M")

    query = """
    INSERT INTO question(submission_time, view_number, vote_number, title, message, image, user_id)
    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s, %(user_id)s)
    """
    cursor.execute(query, {'submission_time': timestamp, 'title': new_question['title'], 'view_number': 0,
                           'vote_number': 0, 'message': new_question['message'], 'image': new_question['image'],
                           'user_id' : user_id})


@connection.connection_handler
def add_new_answer(cursor, new_answer,user_id):
    timestamp = datetime.now().strftime("%Y-%m-%d, %H:%M")
    query = """
    INSERT INTO answer(submission_time, vote_number, question_id, message, image, user_id, is_answer_accepted)
    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(user_id)s, %(is_answer_accepted)s)
    """
    cursor.execute(query, {'submission_time': timestamp, 'vote_number': 0, 'question_id': new_answer['question_id'],
                           'message': new_answer['message'], 'image': new_answer['image'], 'user_id' : user_id, 'is_answer_accepted' : 0})


@connection.connection_handler
def get_specific_question(cursor, question_id):
    query = f"""
        SELECT id, title, message
        FROM question WHERE id = '{question_id}';"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def delete_specific_question(cursor, question_id):
    query = f"""
            DELETE FROM question WHERE id = '{question_id}'
            """
    cursor.execute(query)


@connection.connection_handler
def edit_specific_question(cursor, title, message, image, question_id):
    query = f"""
        UPDATE question
        SET title = '{title}', message = '{message}', image = '{image}'
        WHERE id = '{question_id}'
        """
    cursor.execute(query)


@connection.connection_handler
def get_question_id_for_answer(cursor, answer_id):
    query = """
    SELECT question_id FROM answer WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()[0].get("question_id")


@connection.connection_handler
def delete_specific_answer(cursor, answer_id):
    query = """
        DELETE FROM answer WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@connection.connection_handler
def get_answers_for_specific_question(cursor, question_id):
    query = f"""
        SELECT *
        FROM answer WHERE question_id = '{question_id}' ORDER BY id """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def count_question_views(cursor, question_id):
    query = f"""
        UPDATE question SET view_number = view_number + 1 WHERE id = {question_id}
        """
    cursor.execute(query)


@connection.connection_handler
def question_count_votes(cursor, question_id, vote):
    query = f"""
        UPDATE question SET vote_number = vote_number '{vote}' 1
        WHERE id = '{question_id}'
        """
    cursor.execute(query)


@connection.connection_handler
def count_votes(cursor, question_id, vote):
    query = f"""
        UPDATE question SET vote_number = vote_number {vote} 1 WHERE id = {question_id}
        """
    cursor.execute(query)


@connection.connection_handler
def count_answer_votes(cursor, answer_id, vote):
    query = f"""
        UPDATE answer SET vote_number = vote_number {vote} 1 WHERE id = {answer_id}
        """
    cursor.execute(query)


@connection.connection_handler
def order_by(cursor, order_by, order_direction):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {order_direction}
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def answers_order_by(cursor, order_by, order_direction):
    query = f"""
        SELECT *
        FROM answer
        ORDER BY {order_by} {order_direction}
        """
    cursor.execute(query)
    return cursor.fetchall()


# New tasks:

@connection.connection_handler
def get_question_comment(cursor, question_id):
    query = f"""
        SELECT *
        FROM comment WHERE question_id = '{question_id}'
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_all_comment_for_print(cursor):
    query = f"""
        SELECT *
        FROM comment
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_question_comment(cursor, new_answer, question_id, user_id):
    timestamp = datetime.now().strftime("%Y-%m-%d, %H:%M")
    query = f"""
        INSERT INTO comment ( question_id, message, submission_time, user_id)
        VALUES ( %(question_id)s, %(message)s, %(submission_time)s, %(user_id)s )
        """
    cursor.execute(query, {'question_id': question_id, 'message': new_answer,
                           'submission_time': timestamp, 'user_id': user_id})


@connection.connection_handler
def add_new_answer_comment(cursor, new_answer, answer_id, user_id):
    timestamp = datetime.now().strftime("%Y-%m-%d, %H:%M")

    query = f"""
        INSERT INTO comment ( answer_id, message, submission_time, user_id)
        VALUES ( %(answer_id)s, %(message)s, %(submission_time)s, %(user_id)s )
        """
    cursor.execute(query, {'answer_id': answer_id, 'message': new_answer,
                           'submission_time': timestamp, 'user_id': user_id})


@connection.connection_handler
def find_question(cursor, search):
    query = f"""
    SELECT * FROM question WHERE title ILIKE '%{search}%' ORDER BY id
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def edit_answer(cursor, message, image, answer_id):
    query = f"""
        UPDATE answer
        SET message = '{message}', image = '{image}'
        WHERE id = '{answer_id}'
        """
    cursor.execute(query)


@connection.connection_handler
def get_specific_answer(cursor, answer_id):
    query = f"""
        SELECT message, image FROM answer
        WHERE id = '{answer_id}'
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answers(cursor):
    query = f"""
        SELECT * FROM answer
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_first_five_questions(cursor):
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY id DESC
        LIMIT 5 
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def delete_question_comment(cursor, comment_id):
    query = f"""
    DELETE FROM comment WHERE id = '{comment_id}'
    """
    cursor.execute(query)


@connection.connection_handler
def delete_answer_comment(cursor, comment_id):
    query = f"""
    DELETE FROM comment WHERE id = {comment_id}
    """
    print(query)
    cursor.execute(query)


@connection.connection_handler
def get_answer_id_for_comment(cursor, comment_id):
    query = f"""
    SELECT a.question_id FROM comment
    JOIN answer a on comment.answer_id = a.id
    WHERE comment.id = {comment_id}
    """
    cursor.execute(query)
    return cursor.fetchall()[0].get('question_id')


@connection.connection_handler
def get_question_id_for_comment(cursor, comment_id):
    query = f"""
    SELECT question_id FROM comment WHERE id = {comment_id}
    """
    cursor.execute(query)
    return cursor.fetchall()[0].get('question_id')


@connection.connection_handler
def get_all_users_for_login(cursor):
    query = """
    SELECT * FROM users;
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_users_for_login(cursor, user_name):
    query = f"""
    SELECT username FROM users
    WHERE users.username = (%s);
    """
    cursor.execute(query, [user_name])
    return cursor.fetchone()


@connection.connection_handler
def get_password_for_login(cursor, user_name):
    query = f"""
    SELECT password FROM users
    WHERE users.username = (%s);
    """
    cursor.execute(query, [user_name])
    return cursor.fetchone()


@connection.connection_handler
def add_user(cursor,username,password):
    query = """
                INSERT INTO users (username, password, registration_date, number_of_asked_questions, number_of_answers, number_of_comments, reputation)
                VALUES (%s, %s, localtimestamp, %s, %s, %s, %s)"""
    cursor.execute(query, [username, password, 0, 0, 0, 0])


@connection.connection_handler
def list_all_users(cursor):
    query = """
            SELECT * FROM users;
            """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_specific_user(cursor, user_id):
    query = """
            SELECT * FROM users WHERE id = %(user_id)s;
            """
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_user_id_by_email(cursor, email):
    query = """
    SELECT id FROM users
    WHERE users.username = %(email)s;
    """
    cursor.execute(query, {"email" : email})
    return cursor.fetchone()


@connection.connection_handler
def get_specific_user_questions(cursor, user_id):
    query = """
    SELECT * FROM question WHERE user_id = %(user_id)s;
    """
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_specific_user_answers(cursor, user_id):
    query = """
    SELECT * FROM answer WHERE user_id = %(user_id)s;
    """
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_specific_user_comments(cursor, user_id):
    query = """
    SELECT * FROM comment WHERE user_id = %(user_id)s;
    """
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@connection.connection_handler
def add_tag(cursor, question_id, tag_id):
    query = """
    INSERT INTO question_tag VALUES (%(question_id)s, %(tag_id)s) """
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def get_tags(cursor):
    query = """
    SELECT * FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_tag(cursor, tag):
    query = """
    INSERT INTO tag(name) VALUES (%(tag)s)
    """
    cursor.execute(query, {'tag': tag})


@connection.connection_handler
def get_tag_id(cursor, tag):
    query = """
    SELECT id FROM tag WHERE name = %(tag)s
    """
    cursor.execute(query, {'tag': tag})
    return cursor.fetchall()[0].get('id')


@connection.connection_handler
def delete_tag(cursor, question_id, tag_id):
    query = """
    DELETE FROM question_tag WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
    """
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def get_tags_for_question(cursor, question_id):
    query = """
    SELECT id, name FROM tag
    WHERE id IN (SELECT tag_id FROM question_tag WHERE question_id = %(question_id)s)
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def get_tags_with_num_of_use(cursor):
    query = """
    SELECT COUNT(ALL question_id) AS num_of_use, name FROM tag JOIN question_tag ON tag.id=question_tag.tag_id
    GROUP BY name"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def accept_answer(cursor,answer_id, accepted_data):
    query = """
    UPDATE answer SET is_answer_accepted = %(accepted_data)s
    WHERE id = %(answer_id)s
        """
    cursor.execute(query, {'accepted_data': accepted_data, 'answer_id':answer_id})


@connection.connection_handler
def get_user_id_by_question_id(cursor, question_id):
    query = """
    SELECT question.user_id FROM question WHERE question.id = %(question_id)s
    """
    cursor.execute(query, {'question_id':question_id})
    return cursor.fetchone()


@connection.connection_handler
def count_reputation(cursor, reputation, user_id):
    query = """
    UPDATE users SET reputation = reputation + %(reputation)s WHERE id = %(user_id)s"""
    cursor.execute(query, {'reputation': reputation, 'user_id': user_id})
