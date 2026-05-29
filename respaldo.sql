-- ============================================================
-- CRATEDB / POSTGRESQL BACKUP MOCK
-- Generado: 2026-05-28
-- Tabla: doc.lecturas
-- ============================================================

-- 1. Reconstrucción de la estructura de la tabla
CREATE TABLE IF NOT EXISTS doc.lecturas (
    id STRING,
    sensor STRING,
    valor DOUBLE,
    fecha TIMESTAMP WITH TIME ZONE
);

-- 2. Inserción de ráfaga de datos simulados (Lecturas del HC-SR04 y TMP36)
INSERT INTO doc.lecturas (id, sensor, valor, fecha) VALUES 
('UMVbcJ4Bqv6Zw1WXcB5_', 'TMP36', 25.5, 1780001501312),
('T8UicJ4Bqv6Zw1WXwh6E', 'TMP36', 25.5, 1779997786756),
('TsXqYZ4Bqv6Zw1WXmB5l', 'TMP36', 25.5, 1779759224934),
('A9XzLK8Mmn2Pq3STzK9o', 'HC-SR04', 12.43, 1780002105000),
('B2WpQR5Ntk4Lm8VWxP1a', 'HC-SR04', 15.80, 1780002110000),
('C7VjLM3Pqi9Zw2XYmN4b', 'TMP36', 26.1, 1780002115000),
('D4KshY7Bvx1Ww3OPtR8z', 'HC-SR04', 8.12, 1780002120000),
('E5NtbM2Kpw6Xz4LKvQ3p', 'HC-SR04', 4.55, 1780002125000);

-- 3. Forzar la optimización de los shards para asegurar la persistencia inmediata
REFRESH TABLE doc.lecturas;