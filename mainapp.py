# -*- coding: utf-8 -*-
from flask import Flask, flash, jsonify, render_template, Response, request, flash, json, redirect, session, url_for
from database import db_session, init_db
from models import User, RedCard
from flask_table import Table, Col, ButtonCol, OptCol
from functools import wraps
from sqlalchemy_utils import drop_database, create_database


class UsersTable(Table):
    id = Col('ID')
    login = Col('Логин')
    password = Col('Пароль')
    department = Col('Подразделение')
    privileges = Col('Права доступа')


class RedCardsTable(Table):
    CardID = Col('ID')
    CardNumber = Col('№')
    WorkDesc = Col('Содержание работы')
    WorkDOer = Col('Кто')
    DocFromWhere = Col('От кого')
    DocName = Col('Название док.')
    DocID = Col('№ док.')
    DocDate = Col('Дата издания')
    WorkDueTo = Col('Срок')
    WorkTaker = Col('Приемщик')
    WorkClosedDate = Col('Дата выполнения')
    CardStatus = Col('Статус')


app = Flask(__name__)


@app.route('/PostLoginPass', methods=['POST'])
def PostLoginPass():
    Login = request.form['LoginInput']
    Pass = request.form['PassInput']
    if Login != '' and Pass != '':
        init_db()
        infofromdb = User.query.filter_by(login=Login).first()
        #print(infofromdb.login)
        if infofromdb != None: #сделать проверку на логин и пасс, потому что если введен логин правильно а пасс нет - то ошибка появляется
            if infofromdb.login == Login and infofromdb.password == Pass:
                session['username'] = Login
                return redirect(url_for('destiny'))
            else:
                flash('Неверен логин/пароль.')
                return redirect(url_for('index'))
        else:
            flash('Неверен логин/пароль.')
            return redirect(url_for('index'))



def getinfofromdb(login):
    init_db()
    infofromdb = User.query.filter_by(login=login).first()
    return infofromdb


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            print(session['username'])
        except KeyError:
            return redirect(url_for('notloggedin'))
        #if session['username'] == None or not session['username'] == getinfofromdb(session['username']).login:
         #   return '123'
        return f(*args, **kwargs)
    return wrapper


@app.route('/usersdb', )  # Работа с БД юзеров
@authenticate
def usersdb():
    items = User.query.all()
    tabletoprint = UsersTable(items, table_id="filtered")
    return render_template('/usersdb.html', tabletoprint=tabletoprint)


@app.route('/redcardsdb', methods=['POST', 'GET'])  # Работа с БД красных карточек
@authenticate
def redcardsdb():
    items = RedCard.query.all()
    tabletoprint = RedCardsTable(items, table_id="filtered")
    # print(tabletoprint.__html__())
    return render_template('/redcardsdb.html', tabletoprint=tabletoprint)


@app.route('/adduser', methods=['POST'])  # Добавление нового юзера в БД
@authenticate
def adduser():
    newUserLogin = request.form['LoginInput']
    newUserPass = request.form['PassInput']
    newUserDepartment = 10
    newUserPriveleges = 1
    if newUserLogin != '' and newUserPass != '' and newUserDepartment != '':
        newUser = User(newUserLogin, newUserPass, newUserDepartment, newUserPriveleges)
        db_session.add(newUser)
        db_session.commit()
        return redirect(url_for('index'))
    else:
        return ('Юзер не добавлен')


@app.route('/deluser', methods=['POST'])  # Удаление юзера из БД
@authenticate
def deluser():
    delUserLogin = request.args.get('UserLogin', 0, type=str)
    if User.query.filter(User.login == delUserLogin).first():
        User.query.filter(User.login == delUserLogin).delete()
        db_session.commit()
        return jsonify(result="User_del")
    else:
        return jsonify(result="User_isntdel")


@app.route('/dropdb', methods=['POST'])
def drop_db():
    drop_database('postgresql+psycopg2://postgres:admin@127.0.0.1:5432/ggg')
    return '''dropped
    <br>
    <a href="/">Вернуться</a>
    '''


@app.route('/initdb', methods=['POST'])
def initdb():
    create_database('postgresql+psycopg2://postgres:admin@127.0.0.1:5432/ggg')
    init_db()
    return '''initiated
    <br>
    <a href="/">Вернуться</a>
    '''



@app.route('/addredcard', methods=['POST'])  # Добавление новой красной карточки в БД
@authenticate
def addredcard():
    newDOer = request.form['newDOer']
    if newDOer != '':
        newCardNumber = request.form['newCardNumber']
        newDocFromWhere = request.form['newDocFromWhere']
        newDocName = request.form['newDocName']
        newDocID = request.form['newDocID']
        newDocDate = request.form['newDocDate']
        newWorkDueTo = request.form['newWorkDueTo']
        newWorkDesc = request.form['newWorkDesc']
        newWorkTaker = request.form['newWorkTaker']
        newCardStatus = 'В работе'
        newRedCard = RedCard(newCardNumber, newCardStatus, newDOer, newDocFromWhere, newDocName, newDocID, newDocDate,
                             newWorkDueTo, newWorkDesc, newWorkTaker, '-')
        db_session.add(newRedCard)
        db_session.commit()
        return redirect(url_for('redcardsdb'))
    else:
        return redirect(url_for('redcardsdb'))


@app.route('/closeredcard', methods=['POST'])  # Редактирование красной карточки из БД
@authenticate
def closeredcard():
    RedCardToClose = request.form['RedCardToCloseNumber']
    RedCardCloseDate = request.form['RedCardCloseDate']
    if RedCard.query.filter(RedCard.CardNumber == RedCardToClose).first():
        infofromdb = RedCard.query.filter(RedCard.CardNumber == RedCardToClose).first()
        if infofromdb.CardStatus == 'В работе':
            infofromdb.WorkClosedDate = RedCardCloseDate
            infofromdb.CardStatus = 'Закрыта'
            db_session.commit()
            return redirect(url_for('redcardsdb'))
        else:
            return redirect(url_for('redcardsdb'))
    else:
        return redirect(url_for('redcardsdb'))


@app.route('/delredcard', methods=['POST'])  # Редактирование красной карточки из БД
@authenticate
def delredcard():
    RedCardToDelNumber = request.form['RedCardToDelNumber']
    print(RedCardToDelNumber)
    if RedCard.query.filter(RedCard.CardNumber == RedCardToDelNumber).first():
        RedCard.query.filter(RedCard.CardNumber == RedCardToDelNumber).delete()
        db_session.commit()
        return redirect(url_for('redcardsdb'))
    else:
        return redirect(url_for('redcardsdb'))


@app.route('/printredcard', methods=['POST'])  # Выдача данных для печати красной карточки из БД
@authenticate
def printredcard():
    CardNumberToPrint = request.form['RedCardToPrintNumber']
    if RedCard.query.filter(RedCard.CardNumber == CardNumberToPrint).first():
        infofromdb = RedCard.query.filter(RedCard.CardNumber == CardNumberToPrint).first()
        return render_template('/redcard.html', infofromdb=infofromdb)
    else:
        return redirect(url_for('redcardsdb'))


@app.route('/postponeredcard', methods=['POST'])  # Добавление новой красной карточки в БД
@authenticate
def postponeredcard():
    RedCardToPostponeNumber = request.form['RedCardToPostponeNumber']
    RedCardToPostponeNewDate = request.form['RedCardToPostponeNewDate']
    infofromdb = RedCard.query.filter(RedCard.CardNumber == RedCardToPostponeNumber).first()
    postponedRedCard = RedCard(infofromdb.CardNumber, 'Перенесена', infofromdb.WorkDOer, infofromdb.DocFromWhere,
                               infofromdb.DocName, infofromdb.DocID, infofromdb.DocDate, infofromdb.WorkDueTo,
                               infofromdb.WorkDesc, infofromdb.WorkTaker, 0)
    db_session.add(postponedRedCard)
    infofromdb.WorkDueTo = RedCardToPostponeNewDate
    db_session.commit()
    return redirect(url_for('redcardsdb'))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/choose_your_destiny', methods=['GET', 'POST'])
@authenticate
def destiny():
    if request.method == 'GET':
        return render_template('/choose_destiny.html')
    else:
        DBSelection = request.form['dbs']
        return redirect(url_for(DBSelection))


@app.route('/departmentpage')
@authenticate
def deppage():
    return render_template('deppage.html')

@app.route('/notloggedin')
def notloggedin():
    return render_template('notlogged.html')



@app.route('/404page')
def badpage():
    return render_template('badpage.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


app.secret_key = 'A0Zr98j/3yX R~XHH!jfhgjmN]LWX/,?RT'

if __name__ == '__main__':
    app.run()
