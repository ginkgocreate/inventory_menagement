from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm

bp = Blueprint('views', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('views.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('views.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('views.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/buying', methods=['GET', 'POST'])
@login_required
def register_buying():
    if request.method == 'POST':
        # フォームデータの取得とバリデーション
        buying_id = request.form['buying_id']
        # 他のフィールドも同様に取得
        new_buying = Buying(buying_id=buying_id, ...) # 必要なデータを追加
        db.session.add(new_buying)
        db.session.commit()
        flash('Buying registered successfully')
        return redirect(url_for('views.register_buying'))
    return render_template('register_buying.html', title='Register Buying')

@bp.route('/product', methods=['GET', 'POST'])
@login_required
def register_product():
    if request.method == 'POST':
        # フォームデータの取得とバリデーション
        buying_id = request.form['buying_id']
        # 他のフィールドも同様に取得
        new_product = Product(buying_id=buying_id, ...) # 必要なデータを追加
        db.session.add(new_product)
        db.session.commit()
        flash('Product registered successfully')
        return redirect(url_for('views.register_product'))
    return render_template('register_product.html', title='Register Product')

@bp.route('/inventory')
@login_required
def manage_inventory():
    # 在庫情報を取得
    inventory_items = Inventory.query.all()
    return render_template('manage_inventory.html', title='Manage Inventory', inventory_items=inventory_items)

@bp.route('/api/buying', methods=['POST'])
def api_register_buying():
    data = request.json
    new_buying = Buying(
        buying_id=data['buying_id'],
        buying_date=data['buying_date'],
        supplier_id=data['supplier_id'],
        buying_amount=data['buying_amount'],
        user_id=data['user_id'],
        product_page_id=data['product_page_id'],
        supplier_name=data['supplier_name'],
        age=data['age'],
        occupation=data['occupation'],
        address=data['address'],
        created_by=data['created_by'],
        updated_by=data['updated_by']
    )
    db.session.add(new_buying)
    db.session.commit()
    return jsonify({"message": "Buying registered successfully"}), 201

@bp.route('/api/product', methods=['POST'])
def api_register_product():
    data = request.json
    new_product = Product(
        buying_id=data['buying_id'],
        product_serial_no=data['product_serial_no'],
        buying_date=data['buying_date'],
        branch_cd=data['branch_cd'],
        buying_amount=data['buying_amount'],
        asin=data['asin'],
        product_condition=data['product_condition'],
        sales_channel_id=data['sales_channel_id'],
        expected_sales_amount_bottom=data['expected_sales_amount_bottom'],
        expected_sales_amount_upper=data['expected_sales_amount_upper'],
        sales_date=data['sales_date'],
        sales_amount=data['sales_amount'],
        profit=data['profit'],
        payment_date=data['payment_date'],
        fee=data['fee'],
        shipping_cost=data['shipping_cost'],
        remarks=data['remarks'],
        review=data['review'],
        created_by=data['created_by'],
        updated_by=data['updated_by']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product registered successfully"}), 201

@bp.route('/api/inventory', methods=['GET'])
def api_get_inventory():
    inventory_items = Inventory.query.all()
    results = [
        {
            "buying_id": item.buying_id,
            "product_serial_no": item.product_serial_no,
            "buying_date": item.buying_date,
            "branch_cd": item.branch_cd,
            "buying_amount": item.buying_amount,
            "asin": item.asin,
            "product_condition": item.product_condition,
            "sales_channel_id": item.sales_channel_id,
            "expected_sales_amount_bottom": item.expected_sales_amount_bottom,
            "expected_sales_amount_upper": item.expected_sales_amount_upper,
            "sales_date": item.sales_date,
            "sales_amount": item.sales_amount,
            "profit": item.profit,
            "payment_date": item.payment_date,
            "fee": item.fee,
            "shipping_cost": item.shipping_cost,
            "remarks": item.remarks,
            "review": item.review,
            "created_by": item.created_by,
            "updated_by": item.updated_by,
            "created_at": item.created_at,
            "updated_at": item.updated_at
        } for item in inventory_items]
    return jsonify(results), 200

