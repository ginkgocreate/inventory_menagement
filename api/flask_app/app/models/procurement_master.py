from app import db
from datetime import datetime

class ProcurementMaster(db.Model):
    procurement_id = db.Column(db.String(8), primary_key=True)
    procurement_seq = db.Column(db.String(4), primary_key=True)
    platform_code = db.Column(db.String(4))
    purchase_date = db.Column(db.String(8))
    purchase_price = db.Column(db.Numeric(10, 2))
    shipping_fee = db.Column(db.Numeric(10, 2))
    supplier_id = db.Column(db.String(50))
    supplier_page_id = db.Column(db.String(100))
    supplier_url = db.Column(db.String(1000))
    supplier_info = db.Column(db.String(1000))
    category = db.Column(db.String(4))
    notes = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_id = db.Column(db.String(6))
    updated_id = db.Column(db.String(6))

    def to_dict(self):
        if isinstance(self.purchase_date, str) and len(self.purchase_date) == 8:
            try:
                # YYYYMMDD形式をYYYY-MM-DDに変換
                purchase_date = datetime.strptime(self.purchase_date, '%Y%m%d')
            except ValueError:
                purchase_date = None
        else:
            purchase_date = None if self.purchase_date is None else self.purchase_date
        return {
            'procurement_id': self.procurement_id or '',
            'procurement_seq': self.procurement_seq or '',
            'platform_code': self.platform_code or '',
            'purchase_date': purchase_date.isoformat() if purchase_date else None,
            'purchase_price': str(self.purchase_price) if self.purchase_price else '0.00',
            'shipping_fee': str(self.shipping_fee) if self.shipping_fee else '0.00',
            'supplier_id': self.supplier_id or '',
            'supplier_page_id': self.supplier_page_id or '',
            'supplier_url': self.supplier_url or '',
            'supplier_info': self.supplier_info or '',
            'category': self.category,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_id': self.created_id,
            'updated_id': self.updated_id,
        }
