from flask import Flask, redirect, url_for, request, render_template, abort
from settings import *
from db_scripts import *


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    user = get_user()

    return render_template('index.html', user=user)


@app.route('/about')
def about():
    user = get_user()

    return render_template('about.html', user=user)


@app.route('/post/category/<category_name>', methods=['POST', 'GET'])
def post_category(category_name):
    category = get_category_by_name(category_name)
    if not category:
        abort(404)

    errors = []
    if request.method == 'POST':
        if request.form['title'] == '':
            errors.append('Заголовок не може бути порожнім!')

        if request.form['post'] == '':
            errors.append('Текст не може бути порожнім!')

        # Помилок немає - зерігаємо пост
        if len(errors) == 0:
            # Додавання зображення, якщо користувач його завантажив в форму
            filename = None
            if request.files['image'].filename != '':
                image = request.files['image']
                image.save(f"{PATH_UPLOADS}{image.filename}")
                filename = image.filename  
                
            # Додавання посту
            add_post(category['category_id'], request.form['post'], request.form['title'], filename)    

    posts =  get_posts(category['category_id'])

    return render_template('post_category.html', category=category, posts=posts, errors=errors)


@app.route('/post/view/<post_id>')
def post_view(post_id):
    post = get_post(post_id)

    if not post:
        abort(404)

    category = get_category(post['category_id'])

    return render_template('post_view.html', category=category, post=post)


@app.route('/post/delete/<post_id>/<category_name>')
def delete_post(post_id, category_name):
    del_post(post_id)

    return redirect(f'/post/category/{category_name}')


app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)