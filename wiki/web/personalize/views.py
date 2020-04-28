from flask import request, jsonify, Response, redirect, flash, render_template, Blueprint

from wiki.web.personalize.UserChoicesDb import User
from wiki.web.personalize.forms import preferences
from wiki.web.personalize.settings import app

bp = Blueprint(__name__, 'bp')

app.config['SECRET_KEY'] = 'meow'

"""
These are the default values for the following pages: 
'/personalize/'
'/personalize/create'
'/personalize/delete' 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

_name = "Default"
_backgroundColor = "white"
_textColor = "black"
_buttonColor = "light-gray"
_font = "italic"

""" 
Home. Redirects to Personalize home
"""


@bp.route('/api')
def helloWorld():
    """
    :return: "hello world"
    """
    return "hello world"


"""
A json page showing all users in the database. 
Not linked on page.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/allusers')
def getAllUsers():
    print({'users': User.get_all_users()})
    return jsonify({'users': User.get_all_users()})


"""
Personalize Home
~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/')
def home():
    nameslist = User.get_all_users_names()
    length = len(nameslist)
    form = preferences(request.form)
    return render_template('basep.html',
                           name=_name,
                           backgroundColor=_backgroundColor,
                           textColor=_textColor,
                           buttonColor=_buttonColor,
                           font=_font,
                           namelist=nameslist,
                           length=length,
                           navnames=nameslist,
                           form=form)


@bp.route('/personalize/', methods=['POST'])
def methods():
    return create_user()


"""
Users page with their preferences loaded
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/<string:name>')
def get_users(name):  # get users choices and page
    form = preferences(request.form)
    base = '/api/personalize/wiki/'
    nameslist = User.get_all_users_names()
    if name not in nameslist:
        return page_not_found('user not yet created')
    return_value = User.get_user(name)
    return render_template('usersPage.html',
                           form=form,
                           base=base,
                           name=name,
                           backgroundColor=return_value['backgroundColor'],
                           textColor=return_value['textColor'],
                           buttonColor=return_value['buttonColor'],
                           font=return_value['font'],
                           navnames=nameslist)


@bp.route('/personalize/<string:name>', methods=['POST'])
def methods2(name):
    form = preferences(request.form)
    request_data = request.form.to_dict()
    if request_data.get('delete'):
        delete = request_data['delete']
        if delete == 'Yes, Delete Me':
            return delete_user(name)
    else:
        method = request_data['method']
        if method == 'put':
            return replace_user(name)
        elif method == 'patch':
            return update_user(name)
        elif method == 'post':
            return create_user()
        else:
            flash('try again')
            return redirect('/' + str(name))


"""
Create user page
~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/create', methods=['GET', 'POST'])
def create_user():  # make new user
    nameslist = User.get_all_users_names()
    form = preferences(request.form)
    request_data = request.form.to_dict()
    if request.method == 'POST':
        request_data = request.form.to_dict()

        User.add_user(request_data['name'],
                      request_data['backgroundColor'],
                      request_data['textColor'],
                      request_data['buttonColor'],
                      request_data['font'])
        # response = Response("", 201, mimetype='application/json')
        # response.headers['location'] = "/personalize/" + str(request_data['name'])
        flash('saved')
        return redirect("/api/personalize/" + str(request_data['name']))
    return render_template('createp.html',
                           form=form,
                           name=_name,
                           backgroundColor=_backgroundColor,
                           textColor=_textColor,
                           buttonColor=_buttonColor,
                           font=_font,
                           navnames=nameslist)


"""
Users page, put request. Replaces all fields. 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# @bp.route('/personalize/<string:name>', methods=['PUT'])
@bp.route('/personalize/<string:name>', methods=['POST'])
def replace_user(name):  # replace user choices
    form = preferences(request.form)
    request_data = request.form.to_dict()

    User.replace_user(name, request_data['backgroundColor'],
                      request_data['textColor'], request_data['buttonColor'],
                      request_data['font'])
    # response = Response("", 201, mimetype='application/json')
    # response.headers['location'] = "/personalize/" + str(name)
    flash('saved')
    # return redirect("/personalize/" + str(request_data['name']))
    return render_template('usersPage.html',
                           form=form,
                           name=name,
                           backgroundColor=request_data['backgroundColor'],
                           textColor=request_data['textColor'],
                           buttonColor=request_data['buttonColor'],
                           font=request_data['font'])


"""
Users page, patch request. Updates user choices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# @bp.route('/personalize/<string:name>', methods=['PATCH'])
@bp.route('/personalize/<string:name>', methods=['POST'])
def update_user(name):  # update user choices
    form = preferences(request.form)
    request_data = request.form.to_dict()
    # request_data = request.get_json()
    uinput = request_data['name']
    if uinput != '':
        User.update_user_name(name, request_data['name'])

    uinput = request_data['backgroundColor']
    if uinput != '':
        User.update_user_backgroundColor(name, request_data['backgroundColor'])

    uinput = request_data['textColor']
    if uinput != '':
        User.update_user_textColor(name, request_data['textColor'])

    uinput = request_data['buttonColor']
    if uinput != '':
        User.update_user_buttonColor(name, request_data['buttonColor'])

    uinput = request_data['font']
    if uinput != '':
        User.update_user_font(name, request_data['font'])

    flash('saved')
    return redirect('/api/personalize/' + str(name))
    # return render_template('usersPage.html',
    #                        form=form,
    #                        name=request_data['name'],
    #                        backgroundColor=request_data['backgroundColor'],
    #                        textColor=request_data['textColor'],
    #                        buttonColor=request_data['buttonColor'],
    #                        font=request_data['font'])


"""
Users page, delete request. Removes user from database.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# @bp.route('/personalize/<string:name>', methods=['DELETE'])
@bp.route('/personalize/<string:name>', methods=['POST', 'DELETE'])
def delete_user(name):
    if User.delete_user(name):
        # response = Response("", 201, mimetype='application/json')
        # response.headers['location'] = "/personalize/" + str(name)
        flash('deleted')
        return render_template('basep.html',
                               name=_name,
                               backgroundColor=_backgroundColor,
                               textColor=_textColor,
                               buttonColor=_buttonColor,
                               font=_font)
    else:
        errormessage = {
            "error": "error, could not delete choices"
        }
        response = Response(errormessage, status=400, mimetype='application/json')
        return response, render_template('usersPage.html',
                                         name=_name,
                                         backgroundColor=_backgroundColor,
                                         textColor=_textColor,
                                         buttonColor=_buttonColor,
                                         font=_font)


@bp.route('/personalize/<string:name>/wiki/<string:url>', methods=['GET'])
def geturlwithchoices(name, url):
    form = preferences(request.form)
    base = '/api/personalize/wiki/'
    nameslist = User.get_all_users_names()
    return_value = User.get_user(name)
    if url == 'home':
        return render_template('wikihome.html',
                               form=form,
                               name=name,
                               backgroundColor=return_value['backgroundColor'],
                               textColor=return_value['textColor'],
                               buttonColor=return_value['buttonColor'],
                               font=return_value['font'],
                               navnames=nameslist)
    if url == 'index':
        return render_template('wikiindex.html',
                               form=form,
                               name=name,
                               backgroundColor=return_value['backgroundColor'],
                               textColor=return_value['textColor'],
                               buttonColor=return_value['buttonColor'],
                               font=return_value['font'],
                               navnames=nameslist)
    if url == 'tags':
        return render_template('wikitags.html',
                               form=form,
                               name=name,
                               backgroundColor=return_value['backgroundColor'],
                               textColor=return_value['textColor'],
                               buttonColor=return_value['buttonColor'],
                               font=return_value['font'],
                               navnames=nameslist)
    # if url == 'search':
    #     return render_template('wikisearch.html',
    #                            form=form,
    #                            name=name,
    #                            backgroundColor=return_value['backgroundColor'],
    #                            textColor=return_value['textColor'],
    #                            buttonColor=return_value['buttonColor'],
    #                            font=return_value['font'],
    #                            navnames=nameslist)
    # if url == 'create':
    #     return render_template('wikicreate.html',
    #                            form=form,
    #                            name=name,
    #                            backgroundColor=return_value['backgroundColor'],
    #                            textColor=return_value['textColor'],
    #                            buttonColor=return_value['buttonColor'],
    #                            font=return_value['font'],
    #                            navnames=nameslist)
    else:
        return render_template('basepwiki.html',
                               form=form,
                               base=base,
                               # url=url,
                               name=name,
                               backgroundColor=return_value['backgroundColor'],
                               textColor=return_value['textColor'],
                               buttonColor=return_value['buttonColor'],
                               font=return_value['font'],
                               navnames=nameslist)




"""
Gets all users, gets all names from those users, 
and returns a list of the names.
For use in the nav bar item 'Find Me' 
which shows a link to every user in the database's page.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


def getAllUsersNames():
    namelist = User.get_all_users_names()
    print(namelist)
    namelist.remove(2)
    print(namelist)
    return namelist


"""
Error Handling 
~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    flash(error)
    return render_template('404p.html'), 404


app.register_blueprint(bp)
from wiki.web.routes import bp as wikibp

app.register_blueprint(wikibp, url_prefix='/wiki')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
