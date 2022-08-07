from django.db import connection
from contextlib import closing


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def get_categories():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT * from food_category""")
        categories = dictfetchall(cursor)
        return categories


def get_products():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT food_product.id, food_product.image, food_product.title, food_product.description,
         food_product.cost, food_product.price, food_product.created, food_category.name from food_product 
         left join food_category on food_product.category_id=food_category.id""")
        products = dictfetchall(cursor)
        return products

def get_product_by_order(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT food_orderproduct.count,food_orderproduct.price,
        food_orderproduct.created,food_product.title from food_orderproduct 
         INNER JOIN food_product ON food_orderproduct.product_id=food_product.id  where order_id=%s""", [id])
        orderproduct = dictfetchall(cursor)
        return orderproduct

def get_order_by_user(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT food_order.id, food_customer.first_name,food_customer.last_name, food_order.address, 
                            food_order.payment,food_order.status,food_order.created from food_order 
                            INNER JOIN food_customer on food_customer.id=food_order.customer_id 
                            where food_order.customer_id =%s""", [id])
        order = dictfetchall(cursor)
        return order