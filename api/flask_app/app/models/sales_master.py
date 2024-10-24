from app import db
from datetime import datetime

class SalesMaster(db.Model):
    sale_id = db.Column(db.String(26), primary_key=True)
    platform_code = db.Column(db.String(4))
    title = db.Column(db.String(60))
    product_condition = db.Column(db.String(4))
    sales_start_price = db.Column(db.Numeric(10, 2))
    actual_sales_price	 = db.Column(db.Numeric(10, 2))
    shipping_cost = db.Column(db.Numeric(10, 2))
    fee = db.Column(db.Numeric(10, 2))
    other_costs = db.Column(db.Numeric(10, 2))
    sales_url = db.Column(db.String(1000))
    sales_page_id = db.Column(db.String(100))
    buyer_id = db.Column(db.String(20))
    buyer_info = db.Column(db.String(1000))
    status_id = db.Column(db.String(4))
    notes = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_id = db.Column(db.String(6))
    updated_id = db.Column(db.String(6))

    def to_dict(self):
        return {
            'sale_id': self.sale_id or '',
            'platform_code': self.platform_code or '',
            'title': self.title or '',
            'product_condition': self.product_condition or '',
            'sales_start_price': str(self.sales_start_price) if self.sales_start_price else '0.00',
            'actual_sales_price': str(self.actual_sales_price) if self.actual_sales_price else '0.00',
            'shipping_cost': str(self.shipping_cost) if self.shipping_cost else '0.00',
            'fee': str(self.fee) if self.fee else '0.00',
            'other_costs': str(self.other_costs) if self.other_costs else '0.00',
            'sales_url': str(self.sales_url) if self.sales_url else '0.00',
            'sales_page_id': self.sales_page_id,
            'buyer_id': self.buyer_id or '',
            'buyer_info': self.buyer_info or '',
            'status_id': self.status_id or '',
            'notes': self.notes or '',
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_id': self.created_id,
            'updated_id': self.updated_id,
        }
