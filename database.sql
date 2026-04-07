-- Wine E-commerce Database Schema
-- PostgreSQL (Neon compatible)

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wines table
CREATE TABLE wines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    wine_type VARCHAR(50) NOT NULL CHECK (wine_type IN ('Tinto', 'Blanco', 'Rosé', 'Espumoso')),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    country VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    year INTEGER,
    grape_variety VARCHAR(100),
    alcohol_content DECIMAL(4, 2),
    description TEXT,
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    image_url VARCHAR(500),
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
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
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
    payment_method VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    wine_id UUID NOT NULL REFERENCES wines(id) ON DELETE RESTRICT,
    wine_name VARCHAR(255) NOT NULL,
    wine_price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    subtotal DECIMAL(10, 2) NOT NULL CHECK (subtotal >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_wines_type ON wines(wine_type);
CREATE INDEX idx_wines_country ON wines(country);
CREATE INDEX idx_wines_price ON wines(price);
CREATE INDEX idx_wines_featured ON wines(is_featured);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_created ON orders(created_at);
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_wines_updated_at BEFORE UPDATE ON wines
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample wines data
INSERT INTO wines (name, wine_type, price, country, region, year, grape_variety, alcohol_content, description, stock, image_url, is_featured) VALUES
('Reserva Especial Cabernet', 'Tinto', 89.90, 'Peru', 'Ica', 2020, 'Cabernet Sauvignon', 13.5, 'Vino tinto de cuerpo completo con notas de frutas rojas maduras y roble francés. Ideal para carnes rojas.', 50, '/static/images/wines/wine1.jpg', true),
('Chardonnay Premium', 'Blanco', 65.00, 'Peru', 'Ica', 2021, 'Chardonnay', 12.5, 'Vino blanco elegante con aromas cítricos y toques de vainilla. Perfecto para pescados y mariscos.', 40, '/static/images/wines/wine2.jpg', true),
('Rosé de Verano', 'Rosé', 55.00, 'Peru', 'Arequipa', 2022, 'Malbec', 12.0, 'Vino rosado fresco y afrutado, ideal para el verano. Notas de fresa y sandía.', 60, '/static/images/wines/wine3.jpg', false),
('Gran Reserva Malbec', 'Tinto', 120.00, 'Argentina', 'Mendoza', 2019, 'Malbec', 14.0, 'Malbec argentino de alta gama con crianza en barrica. Complejo y elegante.', 30, '/static/images/wines/wine4.jpg', true),
('Sauvignon Blanc Valle', 'Blanco', 48.00, 'Chile', 'Valle Central', 2022, 'Sauvignon Blanc', 12.5, 'Blanco fresco y aromático con notas herbales y cítricas.', 45, '/static/images/wines/wine5.jpg', false),
('Espumoso Brut Nature', 'Espumoso', 95.00, 'Peru', 'Ica', 2021, 'Chardonnay', 12.0, 'Espumoso método tradicional, burbujas finas y persistentes. Ideal para celebraciones.', 25, '/static/images/wines/wine6.jpg', true);

-- Insert admin user (password: admin123 - hashed with bcrypt)
INSERT INTO users (email, password_hash, full_name, is_admin) VALUES
('admin@vinosdelvalle.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxF6q4Hq2', 'Administrador', true);
