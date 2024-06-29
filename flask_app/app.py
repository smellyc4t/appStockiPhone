from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SearchForm, StockForm
from models import db, Product

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db.init_app(app)

initialized = False

@app.before_request
def before_request():
    global initialized
    if not initialized:
        db.create_all()
        initialized = True

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Password salah')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('dashboard.html', products=products)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    form = SearchForm()
    products = []
    if form.validate_on_submit():
        query = Product.query
        if form.name.data:
            query = query.filter(Product.name.like(f"%{form.name.data}%"))
        if form.capacity.data:
            query = query.filter_by(capacity=form.capacity.data)
        if form.screen.data:
            query = query.filter_by(screen=form.screen.data)
        if form.chip.data:
            query = query.filter_by(chip=form.chip.data)
        if form.camera.data:
            query = query.filter_by(camera=form.camera.data)
        products = query.all()
    return render_template('search.html', form=form, products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_stock():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    form = StockForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            capacity=form.capacity.data,
            screen=form.screen.data,
            chip=form.chip.data,
            camera=form.camera.data
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = StockForm(obj=product)
    
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Produk berhasil diubah.')
        return redirect(url_for('dashboard'))
    
    return render_template('edit.html', form=form, product=product)

@app.route('/delete/<int:product_id>')
def delete(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
