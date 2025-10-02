-- 1. USERS Table
CREATE TABLE USERS (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each user',
    user_name VARCHAR(50) NOT NULL COMMENT 'Full name of the user',
    email VARCHAR(50) UNIQUE COMMENT 'User email address for notifications',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation timestamp',
    
    CONSTRAINT chk_user_name_length CHECK (LENGTH(user_name) >= 2),
    CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- 2. USER_PHONES Table
CREATE TABLE USER_PHONES (
    user_id INT NOT NULL COMMENT 'Foreign key reference to USERS table',
    phone_number VARCHAR(15) NOT NULL COMMENT 'Phone number associated with the user',
    is_primary BOOLEAN DEFAULT FALSE COMMENT 'Indicates if this is the primary phone number',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When the phone number was added',
    
    PRIMARY KEY (user_id, phone_number),
    
    CONSTRAINT fk_user_phones_user_id 
        FOREIGN KEY (user_id) REFERENCES USERS(user_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    
    CONSTRAINT chk_phone_format CHECK (phone_number REGEXP '^[0-9+()-\s]+$'),
    CONSTRAINT chk_phone_length CHECK (LENGTH(phone_number) BETWEEN 10 AND 15)
);

-- 3. TRANSACTION_CATEGORIES Table
CREATE TABLE TRANSACTION_CATEGORIES (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for transaction category',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Name of the transaction category',
    description TEXT COMMENT 'Detailed description of the transaction type',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When the category was created',
    
    CONSTRAINT chk_category_name_length CHECK (LENGTH(category_name) >= 3)
);

-- 4. TRANSACTIONS Table (Main transaction records)
CREATE TABLE TRANSACTIONS (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each transaction',
    amount DECIMAL(10,2) NOT NULL COMMENT 'Transaction amount in local currency',
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When the transaction occurred',
    sender_id INT NOT NULL COMMENT 'User ID of the transaction sender',
    receiver_id INT NOT NULL COMMENT 'User ID of the transaction receiver',
    category_id INT NOT NULL COMMENT 'Category type of the transaction',
    reference_number VARCHAR(50) UNIQUE COMMENT 'Unique reference number for the transaction',
    status ENUM('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'PENDING' COMMENT 'Current status of the transaction',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When the transaction record was created',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update timestamp',
    
    CONSTRAINT fk_transactions_sender 
        FOREIGN KEY (sender_id) REFERENCES USERS(user_id) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    CONSTRAINT fk_transactions_receiver 
        FOREIGN KEY (receiver_id) REFERENCES USERS(user_id) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    CONSTRAINT fk_transactions_category 
        FOREIGN KEY (category_id) REFERENCES TRANSACTION_CATEGORIES(category_id) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    CONSTRAINT chk_amount_positive CHECK (amount > 0)
);

-- 5. SYSTEM_LOGS Table
CREATE TABLE SYSTEM_LOGS (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each log entry',
    transaction_id INT COMMENT 'Related transaction ID (nullable for system-wide logs)',
    log_message TEXT NOT NULL COMMENT 'Detailed log message content',
    log_level ENUM('INFO', 'WARNING', 'ERROR', 'DEBUG') DEFAULT 'INFO' COMMENT 'Severity level of the log entry',
    log_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When the log entry was created',
    ip_address VARCHAR(45) COMMENT 'IP address of the request (supports IPv4 and IPv6)',
    user_agent TEXT COMMENT 'User agent string from the request',
    
    CONSTRAINT fk_system_logs_transaction 
        FOREIGN KEY (transaction_id) REFERENCES TRANSACTIONS(transaction_id) 
        ON DELETE SET NULL ON UPDATE CASCADE
);


-- ================================================================
-- INSERT and SELECT Statements
-- ================================================================

INSERT INTO TRANSACTION_CATEGORIES (category_name, description) VALUES
('MONEY_TRANSFER', 'Person-to-person money transfers'),
('BILL_PAYMENT', 'Utility and service bill payments'),
('MOBILE_TOP_UP', 'Mobile phone airtime top-up'),
('MERCHANT_PAYMENT', 'Payments to registered merchants'),
('CASH_IN', 'Depositing money into mobile wallet'),
('CASH_OUT', 'Withdrawing money from mobile wallet'),
('LOAN_PAYMENT', 'Loan and credit repayments'),
('SALARY_PAYMENT', 'Salary and wage disbursements');

SELECT * FROM TRANSACTION_CATEGORIES;


INSERT INTO USERS (user_name, email) VALUES
('Jean Baptiste Uwimana', 'jean.uwimana@gmail.com'),
('Marie Claire Mukamana', 'marie.mukamana@gmail.com'),
('David Nkurunziza', 'david.nkurunziza@gmail.com'),
('Grace Umuhoza', 'grace.umuhoza@gmail.com'),
('Samuel Hakizimana', 'samuel.hakizimana@gmail.com'),
('Immaculee Nyirahabimana', 'immaculee.nyira@gmail.com'),
('Patrick Maniragaba', 'patrick.maniragaba@gmail.com'),
('Christine Uwamahoro', 'christine.uwamahoro@gmail.com');

SELECT * FROM USERS;

INSERT INTO USER_PHONES (user_id, phone_number, is_primary) VALUES
(1, '250788123456', TRUE),
(1, '250728123456', FALSE),
(2, '250788234567', TRUE),
(3, '250788345678', TRUE),
(3, '250728345678', FALSE),
(4, '250788456789', TRUE),
(5, '250788567890', TRUE),
(6, '250788678901', TRUE),
(7, '250788789012', TRUE),
(8, '250788890123', TRUE);

SELECT * FROM USER_PHONES;


INSERT INTO TRANSACTIONS (amount, sender_id, receiver_id, category_id, reference_number, status) VALUES
(50000.00, 1, 2, 1, 'TXN001234567890', 'COMPLETED'),
(25000.00, 2, 3, 1, 'TXN001234567891', 'COMPLETED'),
(15000.00, 3, 4, 2, 'TXN001234567892', 'COMPLETED'),
(100000.00, 4, 5, 8, 'TXN001234567893', 'COMPLETED'),
(5000.00, 5, 1, 3, 'TXN001234567894', 'COMPLETED'),
(75000.00, 6, 7, 4, 'TXN001234567895', 'COMPLETED'),
(200000.00, 7, 8, 5, 'TXN001234567896', 'PENDING'),
(30000.00, 8, 1, 6, 'TXN001234567897', 'FAILED'),
(45000.00, 1, 6, 7, 'TXN001234567898', 'COMPLETED'),
(12000.00, 2, 4, 2, 'TXN001234567899', 'COMPLETED');

SELECT * FROM TRANSACTIONS;


INSERT INTO SYSTEM_LOGS (transaction_id, log_message, log_level, ip_address) VALUES
(1, 'Transaction processed successfully', 'INFO', '192.168.1.100'),
(2, 'Transaction processed successfully', 'INFO', '192.168.1.101'),
(3, 'Transaction processed successfully', 'INFO', '192.168.1.102'),
(4, 'Salary payment processed - no fees applied', 'INFO', '192.168.1.103'),
(5, 'Mobile top-up completed', 'INFO', '192.168.1.104'),
(6, 'Merchant payment processed', 'INFO', '192.168.1.105'),
(7, 'Large cash-in transaction flagged for review', 'WARNING', '192.168.1.106'),
(8, 'Transaction failed - insufficient balance', 'ERROR', '192.168.1.107'),
(9, 'Loan payment processed successfully', 'INFO', '192.168.1.108'),
(10, 'Bill payment completed', 'INFO', '192.168.1.109'),
(NULL, 'Database maintenance completed', 'INFO', '192.168.1.1'),
(NULL, 'System backup initiated', 'INFO', '192.168.1.1');

SELECT * FROM SYSTEM_LOGS;


-- ================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ================================================================

CREATE INDEX idx_users_email ON USERS(email);

CREATE INDEX idx_user_phones_phone ON USER_PHONES(phone_number);

CREATE INDEX idx_transactions_sender ON TRANSACTIONS(sender_id);
CREATE INDEX idx_transactions_receiver ON TRANSACTIONS(receiver_id);
CREATE INDEX idx_transactions_date ON TRANSACTIONS(transaction_date);
CREATE INDEX idx_transactions_status ON TRANSACTIONS(status);
CREATE INDEX idx_transactions_category ON TRANSACTIONS(category_id);

CREATE INDEX idx_system_logs_timestamp ON SYSTEM_LOGS(log_timestamp);
CREATE INDEX idx_system_logs_level ON SYSTEM_LOGS(log_level);