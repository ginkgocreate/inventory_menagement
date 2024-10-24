CREATE TABLE procurement_master (
    procurement_id VARCHAR(30) PRIMARY KEY,  -- user_info.product_prefix + YYYY-MM-DD + Increment（8桁0詰め）
    manufacturer_name VARCHAR(200),
    model_number VARCHAR(100),
    features VARCHAR(200),
    asin CHAR(10),
    jan CHAR(13),
    notes TEXT,  -- 1000文字まで
    purchase_price DECIMAL(10, 2),  -- 金額のためDECIMAL型を使用
    shipping_cost DECIMAL(10, 2),
    purchase_date DATE,  -- YYYYMMDD形式
    supplier_id CHAR(5),
    supplier_info TEXT,  -- 1000文字まで
    supplier_page_id VARCHAR(100),
    supplier_url TEXT,  -- 1000文字まで
    status_id CHAR(4)
);
CREATE TABLE category_master (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);
CREATE TABLE stock_status_master (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    sale_id INT,
    status_name VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES procurement_master(procurement_id),
    FOREIGN KEY (sale_id) REFERENCES sales_master(sale_id)
);
CREATE TABLE sales_master (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    procurement_id INT,  -- 仕入れと紐付け
    sale_date DATE,  -- 売れた日
    payment_date DATE,  -- 入金日
    buyer_id VARCHAR(10),  -- 購入者ID
    buyer_info TEXT,  -- 購入者情報
    sales_amount DECIMAL(10, 2),  -- 売れた金額
    shipping_cost DECIMAL(10, 2),  -- 送料
    fee DECIMAL(10, 2),  -- 手数料
    proxy_cost DECIMAL(10, 2),  -- 代行費用
    notes TEXT,  -- 備考
    sales_destination_id CHAR(4),  -- 販売先ID
    sales_url TEXT,  -- 販売先URL
    sales_page_id VARCHAR(100),  -- 販売ページID
    FOREIGN KEY (procurement_id) REFERENCES procurement_master(procurement_id) -- 仕入れと関連付け
);
CREATE TABLE status_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    procurement_id INT,
    sale_id INT,
    status VARCHAR(50),  -- ステータス名 (例: 検品待ち, 出荷済みなど)
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seq INT,  -- シーケンス番号
    FOREIGN KEY (procurement_id) REFERENCES procurement_master(procurement_id),
    FOREIGN KEY (sale_id) REFERENCES sales_master(sale_id)
);
CREATE TABLE sales_destination (
    destination_id INT AUTO_INCREMENT PRIMARY KEY,  -- 販売先ID
    destination_name VARCHAR(100) NOT NULL,  -- 販売先名
    commission_rate DECIMAL(5,2) NOT NULL  -- 手数料
);
CREATE TABLE supplier_master (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,  -- 仕入れ元ID
    supplier_name VARCHAR(100) NOT NULL  -- 仕入れ元名
);
CREATE TABLE status_master (
    status_id INT AUTO_INCREMENT PRIMARY KEY,  -- ステータスID
    status_name VARCHAR(100) NOT NULL  -- ステータス名
);
