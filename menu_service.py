from sqlalchemy.orm.exc import NoResultFound
from database import session, MenuItem, Category, Order

def add_category(name):
    if not name:
        raise ValueError("Category name cannot be empty.")
    new_category = Category(name=name)
    session.add(new_category)
    session.commit()

def get_categories():
    return session.query(Category).all()

def add_menu_item(name, category_id, price):
    if not name or price <= 0:
        raise ValueError("Invalid menu item details.")
    new_item = MenuItem(name=name, category_id=category_id, price=price)
    session.add(new_item)
    session.commit()

def get_menu_items():
    return session.query(MenuItem).all()

def update_menu_item(item_id, name, price, availability):
    if not name or price <= 0:
        raise ValueError("Invalid update details.")
    try:
        item = session.query(MenuItem).filter_by(id=item_id).one()
        item.name = name
        item.price = price
        item.availability = availability
        session.commit()
    except NoResultFound:
        raise ValueError("Menu item not found.")

def delete_menu_item(item_id):
    try:
        item = session.query(MenuItem).filter_by(id=item_id).one()
        session.delete(item)
        session.commit()
    except NoResultFound:
        raise ValueError("Menu item not found.")

def place_order(student_name, item_id, quantity):
    if not student_name or quantity <= 0:
        raise ValueError("Invalid order details.")
    try:
        item = session.query(MenuItem).filter_by(id=item_id).one()
        total_price = item.price * quantity
        new_order = Order(student_name=student_name, item_id=item_id, quantity=quantity, total_price=total_price)
        session.add(new_order)
        session.commit()
        return new_order
    except NoResultFound:
        raise ValueError("Menu item not found.")

def get_orders():
    return session.query(Order).all()
