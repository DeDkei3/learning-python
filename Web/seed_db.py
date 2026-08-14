import os
import random
import sqlite3

# Привязываем путь строго к папке Web
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

print(f" Заполняем базу по адресу: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Пересоздаем таблицы с нуля
cursor.execute("DROP TABLE IF EXISTS characteristics")
cursor.execute("DROP TABLE IF EXISTS inventory")

cursor.execute(
    """
    CREATE TABLE inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        image TEXT,
        stock INTEGER DEFAULT 0
    )
"""
)

cursor.execute(
    """
    CREATE TABLE characteristics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        key_name TEXT NOT NULL,
        key_value TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES inventory (id) ON DELETE CASCADE
    )
"""
)

# Набор тестовых товаров
categories = ["Периферия", "Комплектующие", "Мониторы", "Аудио", "Аксессуары"]

sample_products = [
    (
        "Игровая мышь Logitech G Pro X Superlight",
        450.0,
        "Периферия",
        "Discord_7pOvegrtlF.png",
        15,
    ),
    (
        "Клавиатура Dark Project KD87A Gateron Teal",
        320.0,
        "Периферия",
        "Capture001.png",
        8,
    ),
    (
        "Монитор Xiaomi Redmi G34WQ 34 Curved",
        1150.0,
        "Мониторы",
        "Capture001.png",
        5,
    ),
    (
        "Видеокарта NVIDIA GeForce RTX 4060 Ti 8GB",
        1600.0,
        "Комплектующие",
        "Discord_7pOvegrtlF.png",
        4,
    ),
    (
        "Процессор AMD Ryzen 5 5600 OEM",
        420.0,
        "Комплектующие",
        "Capture001.png",
        20,
    ),
    (
        "Игровые наушники HyperX Cloud II Wireless",
        390.0,
        "Аудио",
        "Discord_7pOvegrtlF.png",
        12,
    ),
    (
        "Коврик для мыши SteelSeries QCK Heavy XL",
        95.0,
        "Аксессуары",
        "Capture001.png",
        30,
    ),
    (
        "Механическая клавиатура Keychron K2 V2",
        280.0,
        "Периферия",
        "Discord_7pOvegrtlF.png",
        6,
    ),
]

# Заливаем базу (дублируем категории для заполнения)
for i in range(1, 25):
    base_prod = sample_products[i % len(sample_products)]
    prod_name = f"{base_prod[0]} (v{i})"
    price = base_prod[1] + (i * 10)
    category = base_prod[2]
    img = base_prod[3]
    stock = base_prod[4] + i

    cursor.execute(
        "INSERT INTO inventory (name, price, category, image, stock) VALUES (?, ?, ?, ?, ?)",
        (prod_name, price, category, img, stock),
    )
    product_id = cursor.lastrowid

    # Добавляем базовые характеристики
    cursor.execute(
        "INSERT INTO characteristics (product_id, key_name, key_value) VALUES (?, ?, ?)",
        (product_id, "Гарантия", "12 месяцев"),
    )
    cursor.execute(
        "INSERT INTO characteristics (product_id, key_name, key_value) VALUES (?, ?, ?)",
        (product_id, "Состояние", "Новое"),
    )

conn.commit()
conn.close()

print(" Успешно заполнено! Товары добавлены в нужную базу.")