import psycopg2

## Bu değeri localinde çalışırken kendi passwordün yap. Ama kodu pushlarken 'postgres' olarak bırak.
password = 'postgres'

def connect_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password=password
    )

def create_view_completed_orders():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE OR REPLACE VIEW completed_orders AS SELECT * FROM orders WHERE status='completed';""")
            conn.commit()

def create_view_electronics_products():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE OR REPLACE VIEW electronics_products AS SELECT * FROM products WHERE category = 'Electronics';""")
            conn.commit()

def total_spending_per_customer():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""WITH spending AS (SELECT c.full_name, SUM(p.price * o.quantity) AS total_spending FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN products p ON o.product_id = p.product_id GROUP BY c.customer_id, c.full_name) SELECT full_name, total_spending FROM spending;""")
            return cur.fetchall()

def order_details_with_total():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""with order_details as (select o.order_id, c.full_name, p.product_name, p.price * o.quantity as total_price from orders o join customers c on o.customer_id = c.customer_id join products p on o.product_id = p.product_id) select order_id, full_name, product_name, total_price from order_details;""")
            return cur.fetchall()

def get_customer_who_bought_most_expensive_product():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""select distinct c.full_name from customers c join orders o on c.customer_id = o.customer_id join products p on o.product_id = p.product_id where p.price = (select max(price) from products);""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# 2. Sipariş durumlarına göre açıklama
def get_order_status_descriptions():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""select order_id, status, CASE when status = 'completed' then 'Tamamlandı' when status = 'cancelled' then 'İptal Edildi' else status end as status_description FROM orders;""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# 3. Ortalama fiyatın üstündeki ürünler
def get_products_above_average_price():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""select product_name, price FROM products where price > (select avg(price) from products);""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# 4. Müşteri kategorileri
def get_customer_categories():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""select c.full_name, CASE when count(o.order_id) > 5 then 'Sadık Müşteri' when count(o.order_id) between 2 and 5 then 'Orta Seviye' else 'Yeni Müşteri' end as customer_category FROM customers c left join orders o on c.customer_id = o.customer_id group by c.customer_id, c.full_name;""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# 5. Son 30 gün içinde sipariş veren müşteriler
def get_recent_customers():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""select c.full_name, CASE when count(o.order_id) > 5 then 'Sadık Müşteri' when count(o.order_id) between 2 and 5 then 'Orta Seviye' else 'Yeni Müşteri' end as customer_category FROM customers c left join orders o on c.customer_id = o.customer_id group by c.customer_id, c.full_name;""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# 6. En çok sipariş verilen ürün
def get_most_ordered_product():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""select p.product_name, count(o.order_id) as total_orders from products p join orders o on p.product_id = o.product_id group by p.product_id, p.product_name order by total_orders desc limit 1;""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# 7. Ürün fiyatlarına göre etiketleme
def get_product_price_categories():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""select product_name, price, CASE when price > 1000 then 'Pahalı' when price between 500 and 1000 then 'Orta' else 'Ucuz' end as price_category FROM products;""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result