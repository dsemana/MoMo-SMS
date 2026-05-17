DROP DATABASE IF EXISTS momo_sms;
CREATE DATABASE momo_sms;
USE momo_sms;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user/customer ID',
    full_name VARCHAR(100) NOT NULL COMMENT 'Name of sender or receiver',
    phone_number VARCHAR(20) NOT NULL UNIQUE COMMENT 'Customer phone number',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Date user was added'
);

CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique category ID',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Type of transaction',
    description VARCHAR(255) COMMENT 'Category explanation'
);

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique transaction ID',
    momo_reference VARCHAR(100) NOT NULL UNIQUE COMMENT 'MoMo transaction reference',
    sender_id INT COMMENT 'Sender user ID',
    receiver_id INT COMMENT 'Receiver user ID',
    category_id INT NOT NULL COMMENT 'Transaction category ID',
    amount DECIMAL(12,2) NOT NULL COMMENT 'Transaction amount',
    currency VARCHAR(10) DEFAULT 'RWF' COMMENT 'Transaction currency',
    transaction_date DATETIME NOT NULL COMMENT 'Date and time of transaction',
    status VARCHAR(30) DEFAULT 'completed' COMMENT 'Transaction status',
    raw_message TEXT COMMENT 'Original SMS/XML message',

    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES users(user_id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id)
);

CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique log ID',
    transaction_id INT COMMENT 'Related transaction ID',
    log_level VARCHAR(20) NOT NULL COMMENT 'INFO, WARNING, or ERROR',
    log_message TEXT NOT NULL COMMENT 'Processing log message',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Log creation time',

    CONSTRAINT fk_log_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    CONSTRAINT chk_log_level CHECK (log_level IN ('INFO', 'WARNING', 'ERROR'))
);

CREATE TABLE tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique tag ID',
    tag_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Transaction tag name'
);

CREATE TABLE transaction_tags (
    transaction_id INT NOT NULL COMMENT 'Transaction ID',
    tag_id INT NOT NULL COMMENT 'Tag ID',

    PRIMARY KEY (transaction_id, tag_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

CREATE INDEX idx_users_phone ON users(phone_number);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_category ON transactions(category_id);
CREATE INDEX idx_transactions_sender ON transactions(sender_id);
CREATE INDEX idx_transactions_receiver ON transactions(receiver_id);

INSERT INTO users (full_name, phone_number) VALUES
('Jean Niyonzima', '0788000001'),
('Aline Uwase', '0788000002'),
('Eric Mugisha', '0788000003'),
('Claudine Mukamana', '0788000004'),
('Patrick Habimana', '0788000005');

INSERT INTO transaction_categories (category_name, description) VALUES
('Money Transfer', 'Transfer from one MoMo user to another'),
('Cash Out', 'Withdrawal from MoMo account'),
('Airtime Purchase', 'Buying airtime using MoMo'),
('Bill Payment', 'Payment of utilities or services'),
('Merchant Payment', 'Payment to a business merchant');

INSERT INTO transactions 
(momo_reference, sender_id, receiver_id, category_id, amount, currency, transaction_date, status, raw_message)
VALUES
('TXN001', 1, 2, 1, 5000.00, 'RWF', '2026-05-01 10:00:00', 'completed', 'Sample MoMo transfer SMS'),
('TXN002', 2, 3, 1, 2500.00, 'RWF', '2026-05-01 11:30:00', 'completed', 'Sample MoMo transfer SMS'),
('TXN003', 3, NULL, 3, 1000.00, 'RWF', '2026-05-02 09:15:00', 'completed', 'Sample airtime purchase SMS'),
('TXN004', 4, NULL, 2, 15000.00, 'RWF', '2026-05-02 14:20:00', 'completed', 'Sample cash out SMS'),
('TXN005', 5, NULL, 4, 8000.00, 'RWF', '2026-05-03 16:45:00', 'completed', 'Sample bill payment SMS');

INSERT INTO system_logs (transaction_id, log_level, log_message) VALUES
(1, 'INFO', 'Transaction processed successfully'),
(2, 'INFO', 'Transaction processed successfully'),
(3, 'INFO', 'Airtime transaction categorized'),
(4, 'WARNING', 'Cash out transaction missing receiver'),
(5, 'INFO', 'Bill payment transaction processed');

INSERT INTO tags (tag_name) VALUES
('personal'),
('business'),
('utility'),
('airtime'),
('withdrawal');

INSERT INTO transaction_tags (transaction_id, tag_id) VALUES
(1, 1),
(2, 1),
(3, 4),
(4, 5),
(5, 3);