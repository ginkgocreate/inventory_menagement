import logging
from flask import Blueprint, request, jsonify
from flask_login import current_user 
from app.models.procurement_master import ProcurementMaster
from app import db
from ..utils.date_utils import format_date
from datetime import datetime
from sqlalchemy import func

procurement_bp = Blueprint('procurement', __name__)
logging.basicConfig(level=logging.ERROR)

@procurement_bp.route('/select', methods=['POST'])
def get_all_procurements():
    try:
        procurements = ProcurementMaster.query.all()
        if not procurements:
            logging.info("No procurements found.")
        procurement_list = [proc.to_dict() for proc in procurements]
        return jsonify(procurement_list), 200
    except Exception as e:
        logging.error(f"Error fetching procurements: {str(e)}")
        return jsonify({'error': 'Failed to fetch procurements'}), 500
    
@procurement_bp.route('/get', methods=['POST'])
def get_procurement():
    data = request.get_json()
    try:
        procurement_id = data.get('procurement_id')
        procurement_seq = data.get('procurement_seq')
        procurement = ProcurementMaster.query.filter_by(procurement_id=procurement_id, procurement_seq=procurement_seq).first()
        if procurement:
            return jsonify(procurement.to_dict()), 200
        else:
            return jsonify({'message': 'Procurement not found'}), 404
    except Exception as e:
        logging.error(f"Error fetching procurement with id {id}: {str(e)} {data}")
        return jsonify({'error': 'Failed to fetch procurement'}), 500
    
@procurement_bp.route('/register', methods=['POST'])
def add_procurement():
    data = request.get_json()
    try:
        procurement_id = data.get('procurement_id')
        procurement_seq = data.get('procurement_seq')
        purchase_date = format_date(data.get('purchase_date')).replace('-', '')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # ユーザーid
        user_id = current_user.user_id

        if procurement_id:
            # Update処理
            procurement = ProcurementMaster.query.filter_by(procurement_id=procurement_id, procurement_seq=procurement_seq).first()
            if procurement:
                procurement.platform_code = data.get('platform_code', '')
                procurement.purchase_date = purchase_date
                procurement.purchase_price = data.get('purchase_price', 0)
                procurement.shipping_fee = data.get('shipping_fee', 0)
                procurement.supplier_id = data.get('supplier_id', '')
                procurement.supplier_page_id = data.get('supplier_page_id', '')
                procurement.supplier_url = data.get('supplier_url', '')
                procurement.supplier_info = data.get('supplier_info', '')
                procurement.category = data.get('category', '')
                procurement.notes = data.get('supplier_id', '')
                procurement.updated_at = now
                procurement.updated_id = user_id
                db.session.commit()
                return jsonify({'message': 'Procurement updated successfully!'}), 200
            else:
                return jsonify({'message': 'Procurement not found'}), 404
        else:
            # ユーザーが認証されているか確認
            if not current_user.is_authenticated:
                return jsonify({'message': 'User not authenticated'}), 401

            # 現在の日付を 'YYYYMMDD' 形式で取得
            today_str = datetime.now().strftime('%Y%m%d')

            # procurement_id を生成 (YYYYMMDD + プレフィックス)
            procurement_id = today_str

            # 既存の最大 seq を取得
            max_seq = db.session.query(func.max(ProcurementMaster.procurement_seq)).filter_by(procurement_id=procurement_id).scalar()

            if max_seq:
                # 既存の seq がある場合、+1 する
                new_seq_int = int(max_seq) + 1
            else:
                # 既存の seq がない場合、1 とする
                new_seq_int = 1

            # seq をゼロパディングして4桁にする
            new_seq = f"{new_seq_int:04d}"

            new_procurement = ProcurementMaster(
                procurement_id=procurement_id,
                procurement_seq=new_seq,
                platform_code=data.get('platform_code', ''),
                purchase_date=today_str,
                purchase_price=data.get('purchase_price', 0),
                shipping_fee=data.get('shipping_fee', 0),
                supplier_id=data.get('supplier_id', ''),
                supplier_page_id=data.get('supplier_page_id', ''),
                supplier_url=data.get('supplier_url', ''),
                supplier_info=data.get('supplier_info', ''),
                category=data.get('category', ''),
                notes=data.get('notes', ''),
                created_at=now,
                updated_at=now,
                created_id=user_id,
                updated_id=user_id,
            )
        db.session.add(new_procurement)
        db.session.commit()
        return jsonify({'message': 'Procurement added successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding procurement: {str(e)}")
        return jsonify({'error': str(e)}), 500