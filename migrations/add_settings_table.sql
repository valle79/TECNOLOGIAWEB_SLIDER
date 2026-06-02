-- Tabla de configuración del sistema
CREATE TABLE IF NOT EXISTS site_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type VARCHAR(50) DEFAULT 'text',
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_setting_key (setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar configuraciones por defecto
INSERT INTO site_settings (setting_key, setting_value, setting_type, description) VALUES
('theme_color', '#7f1d1d', 'color', 'Color principal del tema (sidebar, navbar, footer)'),
('site_name', 'Vinos del Valle', 'text', 'Nombre del sitio web'),
('site_email', 'contacto@vinosdelvalle.com', 'email', 'Email de contacto'),
('site_phone', '+51 999 888 777', 'text', 'Teléfono de contacto'),
('local_shipping_rate', '10.00', 'number', 'Costo de envío local (S/)'),
('international_shipping_rate', '25.00', 'number', 'Costo de envío internacional (S/)'),
('enable_notifications', '1', 'boolean', 'Habilitar notificaciones por email'),
('products_per_page', '12', 'number', 'Productos por página en catálogo'),
('currency_symbol', 'S/', 'text', 'Símbolo de moneda'),
('tax_rate', '0.18', 'number', 'Tasa de impuesto (IGV)'),
('enable_stock_alerts', '1', 'boolean', 'Alertas cuando stock es bajo'),
('low_stock_threshold', '5', 'number', 'Umbral de stock bajo')
ON DUPLICATE KEY UPDATE setting_value=VALUES(setting_value);
