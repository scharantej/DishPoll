
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define the Dish model
class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_dish_of_the_week = db.Column(db.Boolean, default=False)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Define the Vote model
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)

# Define the Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery_address = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

# Create the database tables
db.create_all()

# Define the home route
@app.route('/')
def home():
    return render_template('home.html')

# Define the dish of the week route
@app.route('/dish-of-the-week')
def dish_of_the_week():
    dish = Dish.query.filter_by(is_dish_of_the_week=True).first()
    return render_template('dish_of_the_week.html', dish=dish)

# Define the menu route
@app.route('/menu')
def menu():
    dishes = Dish.query.all()
    return render_template('menu.html', dishes=dishes)

# Define the order route
@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        dish_id = request.form.get('dish_id')
        quantity = request.form.get('quantity')
        delivery_address = request.form.get('delivery_address')
        phone_number = request.form.get('phone_number')

        order = Order(
            user_id=1,  # Placeholder for actual user ID
            dish_id=dish_id,
            quantity=quantity,
            delivery_address=delivery_address,
            phone_number=phone_number
        )
        db.session.add(order)
        db.session.commit()

        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('home'))

    dish_id = request.args.get('dish_id')
    dish = Dish.query.get(dish_id)
    return render_template('order.html', dish=dish)

# Define the user account route
@app.route('/user-account')
def user_account():
    return render_template('user_account.html')

# Define the poll route
@app.route('/poll')
def poll():
    dishes = Dish.query.all()
    return render_template('poll.html', dishes=dishes)

# Define the blog route
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Define the contact route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Define the testimonials route
@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
