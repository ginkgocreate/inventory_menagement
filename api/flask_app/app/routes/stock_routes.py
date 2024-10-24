import logging
from flask import Blueprint, request, jsonify
from flask_login import current_user 
from app.models.stock_master import StockMaster
from app import db
from datetime import datetime
from sqlalchemy import func

stock_bp = Blueprint('stock', __name__)
logging.basicConfig(level=logging.ERROR)

@stock_bp.route('/select', methods=['POST'])
def get_all_stock():
    try:
        stocks = StockMaster.query.all()
        if not stocks:
            logging.info("No stock found.")
        stock_list = [stc.to_dict() for stc in stocks]
        return jsonify(stock_list), 200
    except Exception as e:
        logging.error(f"Error fetching stock: {str(e)}")
        return jsonify({'error': 'Failed to fetch stock'}), 500
    
@stock_bp.route('/get-new', methods=['POST'])
def get_new_stock():
    """
    完全に新しいデータを作成するためのエンドポイント
    """
    data = request.get_json()
    try:
        procurement_id = data.get('procurement_id')
        seq = data.get('procurement_seq')

        # 既存の最大 stock_id を取得
        max_stock_id = db.session.query(func.max(StockMaster.stock_id)).filter_by(procurement_id=procurement_id, procurement_seq=seq).scalar()

        if max_stock_id:
            # 最大のstock_idが見つかった場合、+1 する（例: '0001' -> '0002'）
            new_stock_id = str(int(max_stock_id) + 1).zfill(4)  # 4桁でゼロ埋め
        else:
            # stock_idが存在しない場合は '0001' とする
            new_stock_id = '0001'

        logging.info(f"New stock created with stock_id={new_stock_id} for procurement_id {procurement_id} and seq {seq}")

        # 新しい stock オブジェクトを返す（まだDBには保存しない）
        return jsonify({
            'procurement_id': procurement_id,
            'procurement_seq': seq,
            'stock_id': new_stock_id,
            'sales_id': '',
            'category_id': '',
            'asin': '',
            'jan': '',
            'manufacturer': '',
            'product_name': '',
            'model_number': '',
            'serial_number': '',
            'features': '',
            'product_condition_notes': '',
            'remarks': ''
        }), 200

    except Exception as e:
        logging.error(f"Error creating new stock for procurement_id {procurement_id} and seq {seq}: {str(e)}")
        return jsonify({'error': 'Failed to create new stock'}), 500

@stock_bp.route('/get-already', methods=['POST'])
def get_existing_stock():
    """
    既存のデータを更新するためのオブジェクトを返すエンドポイント
    """
    data = request.get_json()
    try:
        procurement_id = data.get('procurement_id')
        seq = data.get('procurement_seq')
        stock_id = data.get('stock_id')

        # stockがすでに存在するか確認
        stock = StockMaster.query.filter_by(procurement_id=procurement_id, procurement_seq=seq, stock_id=stock_id).first()

        if stock:
            logging.info(f"Stock found for procurement_id {procurement_id}, seq {seq}, and stock_id {stock_id}")
            return jsonify(stock.to_dict()), 200
        else:
            logging.warning(f"Stock not found for procurement_id {procurement_id}, seq {seq}, and stock_id {stock_id}")
            return jsonify({'message': 'Stock not found'}), 404

    except Exception as e:
        logging.error(f"Error fetching stock for procurement_id {procurement_id}, seq {seq}, and stock_id {stock_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch stock'}), 500
        
@stock_bp.route('/get-stock-list', methods=['POST'])
def get_stock_list():
    """
    指定された procurement_id と procurement_seq で stock のリストを返すエンドポイント
    """
    data = request.get_json()
    try:
        procurement_id = data.get('procurement_id')
        seq = data.get('procurement_seq')

        if not procurement_id or not seq:
            return jsonify({'error': 'Missing procurement_id or procurement_seq'}), 400

        # 指定された procurement_id と seq に基づいて stock を取得
        stocks = StockMaster.query.filter_by(procurement_id=procurement_id, procurement_seq=seq).all()

        if stocks:
            # データが存在する場合、stock オブジェクトのリストを返す
            stock_list = [stock.to_dict() for stock in stocks]
            return jsonify(stock_list), 200
        else:
            # データが存在しない場合、空のリストを返す
            return jsonify([]), 200

    except Exception as e:
        logging.error(f"Error fetching stock list for procurement_id {procurement_id} and seq {seq}: {str(e)}")
        return jsonify({'error': 'Failed to fetch stock list'}), 500

@stock_bp.route('/update', methods=['POST'])
def update_stock():
    data = request.get_json()
    try:
        procurement_id = data.get('procurement_id')
        seq = data.get('procurement_seq')
        stock_id = data.get('stock_id')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # ユーザーが認証されているか確認
        if not current_user.is_authenticated:
            return jsonify({'message': 'User not authenticated'}), 401
        # ユーザーid
        user_id = current_user.user_id
        
        if not procurement_id or not seq:
            return jsonify({'error': 'Missing procurement_id or seq'}), 400
        # Update処理
        stock = StockMaster.query.filter_by(procurement_id=procurement_id, procurement_seq=seq, stock_id=stock_id).first()
        if stock:
            stock.sales_id = data['sales_id']
            stock.category_id = data.get('category_id', '')
            stock.asin = data.get('asin', '')
            stock.jan = data.get('jan', '')
            stock.manufacturer = data.get('manufacturer', '')
            stock.product_name = data.get('product_name', '')
            stock.model_number = data.get('model_number', '')
            stock.serial_number = data.get('serial_number', '')
            stock.features = data.get('features', '')
            stock.product_condition_notes = data.get('product_condition_notes', '')
            stock.remarks = data.get('remarks', '')
            stock.updated_at = now
            stock.updated_id=user_id,
            db.session.commit()
            return jsonify({'message': 'Procurement updated successfully!'}), 200
        else:
            return jsonify({'message': stock_id}), 404
            
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding procurement: {str(e)}")
        return jsonify({'error': str(e)}), 500

        
@stock_bp.route('/register', methods=['POST'])
def add_stock():
    data = request.get_json()
    try:
        procurement_id = data.get('procurement_id')
        seq = data.get('procurement_seq')
        stock_id = data.get('stock_id')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # ユーザーが認証されているか確認
        if not current_user.is_authenticated:
            return jsonify({'message': 'User not authenticated'}), 401
        # ユーザーのプレフィックスを取得
        user_id = current_user.user_id

        new_stock = StockMaster(
            procurement_id=data.get('procurement_id'),
            procurement_seq=data.get('procurement_seq'),
            stock_id=stock_id,
            sales_id=data.get('sales_id', ''),
            category_id=data.get('category_id', ''),
            asin=data.get('asin', ''),
            jan=data.get('jan', ''),
            manufacturer=data.get('manufacturer', ''),
            product_name=data.get('product_name', ''),
            model_number=data.get('model_number', ''),
            serial_number=data.get('serial_number', ''),
            features=data.get('features', ''),
            product_condition_notes=data.get('product_condition_notes', ''),
            remarks=data.get('remarks', ''),
            created_at=now,
            updated_at=now,
            created_id=user_id,
            updated_id=user_id,
        )
        db.session.add(new_stock)
        db.session.commit()
        return jsonify({'message': 'Procurement added successfully!'}), 201
    except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding procurement: {str(e)}")
            return jsonify({'error': str(e)}), 500