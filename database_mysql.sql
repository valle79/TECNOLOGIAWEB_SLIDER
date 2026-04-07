-- Wine E-commerce Database Schema
-- MySQL 8.0+

-- Create database
CREATE DATABASE IF NOT EXISTS wine_ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE wine_ecommerce;

-- Users table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Wines table
CREATE TABLE wines (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    wine_type ENUM('Tinto', 'Blanco', 'Rosé', 'Espumoso') NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    country VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    year INT,
    grape_variety VARCHAR(100),
    alcohol_content DECIMAL(4, 2),
    description TEXT,
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    image_url VARCHAR(500),
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_wine_type (wine_type),
    INDEX idx_country (country),
    INDEX idx_price (price),
    INDEX idx_featured (is_featured)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Orders table
CREATE TABLE orders (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36),
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(50),
    shipping_address TEXT NOT NULL,
    shipping_city VARCHAR(100) NOT NULL,
    shipping_country VARCHAR(100) NOT NULL,
    is_international BOOLEAN DEFAULT FALSE,
    subtotal DECIMAL(10, 2) NOT NULL CHECK (subtotal >= 0),
    shipping_cost DECIMAL(10, 2) NOT NULL CHECK (shipping_cost >= 0),
    total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
    status ENUM('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    payment_method VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_user (user_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Order items table
CREATE TABLE order_items (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    order_id CHAR(36) NOT NULL,
    wine_id CHAR(36) NOT NULL,
    wine_name VARCHAR(255) NOT NULL,
    wine_price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    subtotal DECIMAL(10, 2) NOT NULL CHECK (subtotal >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (wine_id) REFERENCES wines(id) ON DELETE RESTRICT,
    INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample wines data
INSERT INTO wines (id, name, wine_type, price, country, region, year, grape_variety, alcohol_content, description, stock, image_url, is_featured) VALUES
(UUID(), 'Reserva Especial Cabernet', 'Tinto', 89.90, 'Peru', 'Ica', 2020, 'Cabernet Sauvignon', 13.5, 'Vino tinto de cuerpo completo con notas de frutas rojas maduras y roble francés. Ideal para carnes rojas.', 50, '/static/images/wines/wine1.jpg', true),
(UUID(), 'Chardonnay Premium', 'Blanco', 65.00, 'Peru', 'Ica', 2021, 'Chardonnay', 12.5, 'Vino blanco elegante con aromas cítricos y toques de vainilla. Perfecto para pescados y mariscos.', 40, '/static/images/wines/wine2.jpg', true),
(UUID(), 'Rosé de Verano', 'Rosé', 55.00, 'Peru', 'Arequipa', 2022, 'Malbec', 12.0, 'Vino rosado fresco y afrutado, ideal para el verano. Notas de fresa y sandía.', 60, '/static/images/wines/wine3.jpg', false),
(UUID(), 'Gran Reserva Malbec', 'Tinto', 120.00, 'Argentina', 'Mendoza', 2019, 'Malbec', 14.0, 'Malbec argentino de alta gama con crianza en barrica. Complejo y elegante.', 30, '/static/images/wines/wine4.jpg', true),
(UUID(), 'Sauvignon Blanc Valle', 'Blanco', 48.00, 'Chile', 'Valle Central', 2022, 'Sauvignon Blanc', 12.5, 'Blanco fresco y aromático con notas herbales y cítricas.', 45, '/static/images/wines/wine5.jpg', false),
(UUID(), 'Espumoso Brut Nature', 'Espumoso', 95.00, 'Peru', 'Ica', 2021, 'Chardonnay', 12.0, 'Espumoso método tradicional, burbujas finas y persistentes. Ideal para celebraciones.', 25, '/static/images/wines/wine6.jpg', true);

-- Insert admin user (password: admin123 - hashed with bcrypt)
INSERT INTO users (id, email, password_hash, full_name, is_admin) VALUES
(UUID(), 'admin@vinosdelvalle.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxF6q4Hq2', 'Administrador', true);
