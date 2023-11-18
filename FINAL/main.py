from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_password.db'
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
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    category = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def header():
    return render_template("main.html")

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

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')
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

    # Check if the current user is the owner of the product
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

    # If not the owner, you might want to redirect or display an error
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