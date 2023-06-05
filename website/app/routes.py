import time

from flask import flash
from app import app
from app.forms import LoginForm, RegistrationForm
from app.managers.db_manager import DBManager
from app.managers.classification_manager import TestClassificationManager
from app.managers.gaussian_NB_manager import GaussianNBManager
from app.managers.network_manager import NetworkManager
from app.managers.graph_manager import GraphManager
from app.static.text.string_constants import StringConstants
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user


@app.route("/", methods=["GET", "POST"])
@app.route("/main", methods=["GET", "POST"])
@login_required
def main():
    network_manager = NetworkManager()
    user_id = network_manager.get_user_id()
    data = DBManager().get_data(user_id)
    city = network_manager.get_city()
    username = network_manager.get_user_username()
    avatar = network_manager.get_user_avatar()
    graph = GraphManager(data=data).save_graph()

    predict_message = StringConstants.prediction_is_impossible

    cur_weather = network_manager.get_cur_weather()
    if not cur_weather:
        return render_template(
            "main.html",
            city=city,
            username=username,
            avatar=avatar,
            graph=graph,
            predict_message=predict_message,
            title=StringConstants.main_page,
        )

    if request.method == "POST":
        user_answer = network_manager.get_user_answer()
        current_time = time.strftime("%d.%m.%Y %H:%M:%S")
        DBManager().save_data(
            user_id=user_id,
            time=current_time,
            user_answer=user_answer,
            weather=cur_weather,
        )
        redirect(url_for("main"))

    user_id = network_manager.get_user_id()

    # test block start

    # gaussian_NB_model = GaussianNB()
    # tree_model = tree.DecisionTreeClassifier(criterion='gini')
    # random_forrest_model = RandomForestClassifier(criterion='gini', n_estimators=30)
    
    # TestClassificationManager(data=data, cur_weather=cur_weather).predict_is_head_hurts(model=gaussian_NB_model)
    # TestClassificationManager(data=data, cur_weather=cur_weather).predict_is_head_hurts(model=tree_model)
    # TestClassificationManager(data=data, cur_weather=cur_weather).predict_is_head_hurts(model=random_forrest_model)

    # test block end

    gaussian_NB_Manager = GaussianNBManager(data=data, cur_weather=cur_weather)
    predict = gaussian_NB_Manager.get_predict()
    if not predict:
        predict_message = StringConstants.need_more_data
    else:
        param_1 = StringConstants.not_increased
        if predict.is_high_pressure == 1:
            param_1 = StringConstants.increased

        param_2 = StringConstants.not_hurts
        if predict.is_head_hurts == 1:
            param_2 = StringConstants.hurts

        predict_message = StringConstants.prediction_message % (
            param_1,
            param_2,
            predict.well_being,
        )

    return render_template(
        "main.html",
        city=city,
        username=username,
        avatar=avatar,
        predict_message=predict_message,
        title=StringConstants.main_page,
    )


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("login"))
    form = RegistrationForm()
    if form.validate_on_submit():
        DBManager().save_user(form.username.data, form.email.data, form.password.data)
        return redirect(url_for("login"))
    return render_template(
        "registration.html", title=StringConstants.registration, form=form
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    form = LoginForm()
    if form.validate_on_submit():
        email: str = form.email.data
        user = DBManager().get_user(email)
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("main"))
    return render_template("login.html", title=StringConstants.login, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main"))
