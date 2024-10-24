from app import db
from datetime import datetime

class StockMaster(db.Model):
    procurement_id = db.Column(db.String(8))
    procurement_seq = db.Column(db.String(4))
    stock_id  = db.Column(db.String(4), primary_key=True)
    sales_id = db.Column(db.String(26))
    category_id = db.Column(db.String(4))
    asin = db.Column(db.String(20))
    jan = db.Column(db.String(20))
    manufacturer = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    model_number = db.Column(db.String(50))
    serial_number = db.Column(db.String(50))
    features = db.Column(db.String(1000))
    product_condition_notes = db.Column(db.String(1000))
    remarks = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_id = db.Column(db.String(6))
    updated_id = db.Column(db.String(6))

    def to_dict(self):
        return {
            'procurement_id': self.procurement_id or '',
            'procurement_seq': self.procurement_seq or '',
            'stock_id': self.stock_id or '',
            'sales_id': self.sales_id or '',
            'category_id': self.category_id or '',
            'asin': self.asin or '',
            'jan': self.jan or '',
            'manufacturer': self.manufacturer or '',
            'product_name': self.product_name or '',
            'model_number': self.model_number or '',
            'serial_number': self.serial_number or '',
            'features': self.features or '',
            'product_condition_notes': self.product_condition_notes or '',
            'remarks': self.remarks or '',
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_id': self.created_id,
            'updated_id': self.updated_id,
        }
