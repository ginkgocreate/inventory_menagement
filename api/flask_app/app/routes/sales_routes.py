import logging
from flask import Blueprint, request, jsonify
from flask_login import current_user 
from app.models.sales_master import SalesMaster
from app import db
from datetime import datetime
from sqlalchemy import func

sales_bp = Blueprint('sales', __name__)
logging.basicConfig(level=logging.ERROR)

@sales_bp.route('/select', methods=['GET'])
def get_all_sales():
    try:
        sales = SalesMaster.query.all()
        if not sales:
            logging.info("No sales found.")
        sale_list = [proc.to_dict() for proc in sales]
        return jsonify(sale_list), 200
    except Exception as e:
        logging.error(f"Error fetching sales: {str(e)}")
        return jsonify({'error': 'Failed to fetch sales'}), 500
    
@sales_bp.route('/get-new', methods=['POST'])
def get_new_sale():
    """
    完全に新しいデータを作成するためのエンドポイント
    """
    data = request.get_json()
    try:
        sale_id = data.get('sale_id')

        # ユーザーが認証されているか確認
        if not current_user.is_authenticated:
            return jsonify({'message': 'User not authenticated'}), 401
        # ユーザーのプレフィックスを取得
        user_prefix = current_user.product_prefix

        # 現在の日付を 'YYYYMMDD' 形式で取得
        today_str = datetime.now().strftime('%Y-%m-%d')
        # 既存の最大 sale_id を取得
        max_sale_id = db.session.query(func.max(SalesMaster.sale_id)).filter_by(sale_id=sale_id).scalar()[-5:]

        if max_sale_id:
            # 最大のstock_idが見つかった場合、+1 する（例: '00001' -> '00002'）
            new_sale_seq = str(int(max_sale_id) + 1).zfill(5)  # 4桁でゼロ埋め
        else:
            # stock_idが存在しない場合は '0001' とする
            new_sale_seq = '00001'

        logging.info(f"New stock created with sale_seq={new_sale_seq}")

        # sale_id を生成
        new_sale_id = f"{user_prefix}-{today_str}-{new_sale_seq}"

        # 新しい stock オブジェクトを返す（まだDBには保存しない）
        return jsonify({
            'sale_id': new_sale_id,
            'platform_code': '',
            'title': '',
            'product_condition': '',
            'sales_start_price': 0,
            'actual_sales_price': 0,
            'shipping_cost': 0,
            'fee': 0,
            'other_costs': 0,
            'sales_url': '',
            'sales_page_id': '',
            'buyer_id': '',
            'buyer_info': '',
            'status_id': '',
            'notes': '',
        }), 200

    except Exception as e:
        logging.error(f"Error creating new stock for sales_id {new_sale_id}")
        return jsonify({'error': 'Failed to create new stock'}), 500

@sales_bp.route('/get-already', methods=['POST'])
def get_existing_sale():
    """
    既存のデータを更新するためのオブジェクトを返すエンドポイント
    """
    data = request.get_json()
    try:
        sale_id = data.get('sale_id')

        # stockがすでに存在するか確認
        sale = SalesMaster.query.filter_by(sale_id=sale_id).first()

        if sale:
            logging.info(f"Stock found for sale_id {sale_id}")
            return jsonify(sale.to_dict()), 200
        else:
            logging.warning(f"Stock not found for sale_id {sale_id}")
            return jsonify({'message': 'Stock not found'}), 404

    except Exception as e:
        logging.error(f"Error fetching stock for procurement_id {sale_id}")
        return jsonify({'error': 'Failed to fetch stock'}), 500
        
@sales_bp.route('/update', methods=['POST'])
def update_sale():
    data = request.get_json()
    try:
        sale_id = data.get('sales_id')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # ユーザーが認証されているか確認
        if not current_user.is_authenticated:
            return jsonify({'message': 'User not authenticated'}), 401
        # ユーザーid
        user_id = current_user.user_id
        
        if not sale_id:
            return jsonify({'error': 'Missing sale_id'}), 400
        # Update処理
        sale = SalesMaster.query.filter_by(sales_id=sale_id).first()
        if sale:
            sale.platform_code = data.get('platform_code', '')
            sale.title = data.get('title', '')
            sale.product_condition = data.get('product_condition', '')
            sale.sales_start_price = data.get('sales_start_price', 0)
            sale.actual_sales_price = data.get('actual_sales_price', 0)
            sale.shipping_cost = data.get('shipping_cost', 0)
            sale.fee = data.get('fee', 0)
            sale.other_costs = data.get('other_costs', 0)
            sale.sales_url = data.get('sales_url', '')
            sale.sales_page_id = data.get('sales_page_id', '')
            sale.buyer_id = data.get('buyer_id', '')
            sale.buyer_info = data.get('buyer_info', '')
            sale.status_id = data.get('status_id', '')
            sale.notes = data.get('notes', '')
            sale.updated_at = now
            sale.updated_id = user_id
            db.session.commit()
            return jsonify({'message': 'Procurement updated successfully!'}), 200
        else:
            return jsonify({'message': sale_id}), 404
            
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding sale: {str(e)}")
        return jsonify({'error': str(e)}), 500

        
@sales_bp.route('/register', methods=['POST'])
def add_stock():
    data = request.get_json()
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # ユーザーが認証されているか確認
        if not current_user.is_authenticated:
            return jsonify({'message': 'User not authenticated'}), 401
        # ユーザーのプレフィックスを取得
        user_id = current_user.user_id

        new_sale = SalesMaster(
            sale_id=data.get('sale_id'),
            platform_code=data.get('platform_code', ''),
            title=data.get('title', ''),
            product_condition=data.get('product_condition', ''),
            sales_start_price=data.get('sales_start_price', 0),
            actual_sales_price=data.get('actual_sales_price', 0),
            shipping_cost=data.get('shipping_cost', 0),
            fee=data.get('fee', 0),
            other_costs=data.get('other_costs', 0),
            sales_url=data.get('sales_url', ''),
            sales_page_id=data.get('sales_page_id', ''),
            buyer_id=data.get('buyer_id', ''),
            buyer_info=data.get('buyer_info', ''),
            status_id=data.get('status_id', ''),
            notes=data.get('notes', ''),
            created_at=now,
            updated_at=now,
            created_id=user_id,
            updated_id=user_id,
        )
        db.session.add(new_sale)
        db.session.commit()
        return jsonify({'message': 'Procurement added successfully!'}), 201
    except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding procurement: {str(e)}")
            return jsonify({'error': str(e)}), 500