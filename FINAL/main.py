from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login-password.db'
app.secret_key = 'f454654*-FW4432-FHGHFHF5464-+65/f'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    category = db.Column(db.String(50), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Product', backref='cart', lazy=True)


with app.app_context():
    db.create_all()


@app.route('/')
def header():
    return render_template("main.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/catalog_electronics', methods=['GET'])
def catalog_electronics():
    products = Product.query.filter_by(category='Электроника').all()
    return render_template('catalog_electronics.html', products=products)

@app.route('/catalog_real_estate', methods=['GET'])
def catalog_real_estate():
    products = Product.query.filter_by(category='Недвижимость').all()
    return render_template('catalog_real_estate.html', products=products)

@app.route('/catalog_transport', methods=['GET'])
def catalog_transport():
    products = Product.query.filter_by(category='Транспорт').all()
    return render_template('catalog_transport.html', products=products)

@app.route('/catalog_furniture', methods=['GET'])
def catalog_furniture():
    products = Product.query.filter_by(category='Мебель').all()
    return render_template('catalog_furniture.html', products=products)

@app.route('/catalog_accessories', methods=['GET'])
def catalog_accessories():
    products = Product.query.filter_by(category='Аксессуары').all()
    return render_template('catalog_accessories.html', products=products)

@app.route('/catalog_miscellaneous', methods=['GET'])
def catalog_miscellaneous():
    products = Product.query.filter_by(category='Разные').all()
    return render_template('catalog_miscellaneous.html', products=products)

@app.route('/catalog_footwear', methods=['GET'])
def catalog_footwear():
    products = Product.query.filter_by(category='Обувь').all()
    return render_template('catalog_footwear.html', products=products)

@app.route('/catalog_clothing', methods=['GET'])
def catalog_clothing():
    products = Product.query.filter_by(category='Одежда').all()
    return render_template('catalog_clothing.html', products=products)

@app.route('/polit')
def polit():
    return render_template('polit.html')

@app.route('/rule')
def rule():
    return render_template('rule.html')
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/start', methods=['POST'])
def start_command():
    telegram_bot_token = "6470455301:AAFIyfQAtQwq7zjuYGa_szNwLrg4SVTnyuQ"

    telegram_chat_id = "2019033793"

    telegram_api_url = f"https://api.telegram.org/bot6470455301:AAFIyfQAtQwq7zjuYGa_szNwLrg4SVTnyuQ/sendMessage"

    start_message = "Привет! Это бот для обработки заявок."
    telegram_data = {
        'chat_id': telegram_chat_id,
        'text': start_message,
        'parse_mode': 'HTML',
    }

    response = requests.post(telegram_api_url, data=telegram_data)
    if response.status_code == 200:
        print("Сообщение успешно отправлено в ответ на команду /start.")
    else:
        print(f"Ошибка отправки сообщения в ответ на команду /start. Код статуса: {response.status_code}, Текст ответа: {response.text}")

    return "Команда /start обработана успешно!"


@app.route('/process_form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not name or not email or not message:
            flash('Пожалуйста, заполните все обязательные поля (имя, почта, сообщение).', 'error')
            return redirect(url_for('contacts'))

        telegram_bot_token = "6470455301:AAFIyfQAtQwq7zjuYGa_szNwLrg4SVTnyuQ"

        telegram_chat_id = "2019033793"

        telegram_api_url = f"https://api.telegram.org/bot6470455301:AAFIyfQAtQwq7zjuYGa_szNwLrg4SVTnyuQ/sendMessage"

        telegram_message = f"Новая заявка из формы обратной связи:\n\nИмя: {name}\nEmail: {email}\nСообщение: {message}"

        telegram_data = {
            'chat_id': telegram_chat_id,
            'text': telegram_message,
            'parse_mode': 'HTML',
        }

        response = requests.post(telegram_api_url, data=telegram_data)

        if response.status_code == 200:
            flash("Сообщение успешно отправлено в Telegram.", 'success')
        else:
            flash(
                f"Ошибка отправки сообщения в Telegram. Код статуса: {response.status_code}, Текст ответа: {response.text}",
                'error')

        return redirect(url_for('contacts'))
    else:
        return "Неверный метод запроса."

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')

        user = User.query.filter_by(login=login).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return render_template('successfulauth.html')
        else:
            return render_template('auth_bad.html')

    return render_template('authorization.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        password_hash = generate_password_hash(password)

        new_user = User(login=login, password_hash=password_hash)
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()

        return render_template('successfulregis.html')

    return render_template('registration.html')


@app.route('/publish_product', methods=['GET', 'POST'])
def render_publish_product():
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('You need to log in first.')
            return redirect(url_for('form_authorization'))

        name = request.form.get('name')
        price = request.form.get('price')
        image = request.form.get('image')
        description = request.form.get('description')  # Добавленное поле
        location = request.form.get('location')  # Добавленное поле
        contact_person = request.form.get('contact_person')  # Добавленное поле
        email = request.form.get('email')  # Добавленное поле
        phone_number = request.form.get('phone_number')  # Добавленное поле
        category = request.form.get('category')

        new_product = Product(
            name=name,
            price=price,
            image=image,
            user_id=session['user_id'],
            description=description,
            location=location,
            contact_person=contact_person,
            email=email,
            phone_number=phone_number,
            category=category
        )

        db.session.add(new_product)
        db.session.commit()

        flash('Product created successfully.')
        return redirect(url_for('show_catalog'))

    return render_template('publish_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)

    if 'user_id' in session and session['user_id'] == product.user_id:
        if request.method == 'POST':
            product.name = request.form.get('name')
            product.price = request.form.get('price')
            product.image = request.form.get('image')
            product.description = request.form.get('description')
            product.location = request.form.get('location')
            product.contact_person = request.form.get('contact_person')
            product.email = request.form.get('email')
            product.phone_number = request.form.get('phone_number')

            db.session.commit()
            return redirect(url_for('show_product', product_id=product.id))
        return render_template('edit_product.html', product=product)

    flash('You do not have permission to edit this product.')
    return redirect(url_for('show_product', product_id=product.id))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session:
        flash('You need to log in first.')
        return redirect(url_for('form_authorization'))

    product = Product.query.get(product_id)

    # Проверяем, принадлежит ли товар текущему пользователю
    if product.user_id != session['user_id']:
        flash('You do not have permission to delete this product.')
        return redirect(url_for('show_product', product_id=product.id))

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('show_catalog'))

@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('logout'))

    if request.method == 'POST':
        user_id = session['user_id']
        product = Product.query.filter_by(id=product_id).first()

        if product:
            cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

            if cart_item:
                cart_item.quantity += 1
            else:
                new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=1)
                db.session.add(new_cart_item)

            db.session.commit()

    return redirect(url_for('basket'))

from flask import redirect, url_for

@app.route('/basket')
def basket():
    if 'user_id' not in session:
        flash('Вы не авторизованы. Пожалуйста, войдите в систему.')
        return redirect(url_for('form_authorization'))

    user_id = session['user_id']

    # Получаем корзину пользователя, включая связанный продукт
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    # Создаем список для отображения в шаблоне
    cart = []
    for item in cart_items:
        product = item.product
        cart.append({
            'id': item.id,
            'name': product.name if product else 'N/A',
            'price': product.price if product else 'N/A',
            'quantity': item.quantity,
            'product_id': product.id if product else None
        })

    return render_template('basket.html', cart=cart)

@app.route('/catalog', methods=['GET'])
def show_catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)

@app.route('/show_product/<int:product_id>', methods=['GET'])
def show_product(product_id):
    product = Product.query.get(product_id)
    return render_template('product.html', product=product)
@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return redirect(url_for('header'))

@app.route('/category/<string:category_name>', methods=['GET'])
def show_category(category_name):
    products = Product.query.filter_by(category=category_name).all()
    return render_template('category.html', products=products, category=category_name)

if __name__ == "__main__":
    app.run()