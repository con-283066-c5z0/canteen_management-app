import streamlit as st
from menu_service import (
    add_category, get_categories, add_menu_item, get_menu_items,
    update_menu_item, delete_menu_item, place_order, get_orders
)

#Loaded CSS for look and feel
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('styles.css')

st.title('Campus Cookhouse')

#Created a navigation on the left side of the page which will help users move between the four different pages
menu = ['Admin', 'Student', 'Pending Orders', 'Ready Orders']
choice = st.sidebar.selectbox('Select Page', menu)

if choice == 'Admin':
    st.markdown('<div class="admin-section">', unsafe_allow_html=True)
    
    #Add category 
    st.subheader('Add Category')
    category_name = st.text_input('Category Name')
    if st.button('Add Category'):
        add_category(category_name)
        st.success('Category added successfully!')

    #Displayed the categories
    st.subheader('Categories')
    categories = get_categories()
    for category in categories:
        try:
            category_id = category.id
            category_name = category.name
            with st.expander(f'ID: {category_id}, Name: {category_name}'):
                st.markdown("""
                    <div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">
                        <p>Active Category.</p>
                    </div>
                """, unsafe_allow_html=True)
        except AttributeError as e:
            st.error(f"Failed to retrieve category information: {e}")

    #Adding menu items
    st.subheader('Add Menu Item')
    item_name = st.text_input('Item Name')
    category_ids = [category.id for category in categories]
    category_id = st.selectbox('Category', category_ids, index=0 if category_ids else None)
    price = st.number_input('Price', min_value=0.0, format="%.2f")
    if st.button('Add Menu Item'):
        add_menu_item(item_name, category_id, price)
        st.success('Menu item added successfully!')

    #Displayd those menu items
    st.subheader('Menu Items')
    menu_items = get_menu_items()
    for item in menu_items:
        try:
            item_id = item.id
            item_name = item.name
            category_name = item.category.name
            item_price = item.price
            item_availability = item.availability
            with st.expander(f'ID: {item_id}, Name: {item_name}, Category: {category_name}'):
                st.markdown(f"""
                    <div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">
                        <p><strong>Price:</strong> R{item_price:.2f}</p>
                        <p><strong>Availability:</strong> {item_availability}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f'Delete {item_name}'):
                    delete_menu_item(item_id)
                    st.success('Menu item deleted successfully!')
                    st.experimental_rerun()
        except AttributeError as e:
            st.error(f"Failed to retrieve menu item information: {e}")

    #Update menu item on the system currently
    st.subheader('Update Menu Item')
    item_id = st.number_input('Item ID to Update', min_value=0)
    updated_name = st.text_input('Updated Name')
    updated_price = st.number_input('Updated Price', min_value=0.0, format="%.2f")
    updated_availability = st.checkbox('Availability', value=True)
    if st.button('Update Menu Item'):
        update_menu_item(item_id, updated_name, updated_price, updated_availability)
        st.success('Menu item updated successfully!')
    
    st.markdown('</div>', unsafe_allow_html=True)

elif choice == 'Student':
    st.markdown('<div class="student-section">', unsafe_allow_html=True)

    #Display menu items
    st.subheader('Menu')
    menu_items = get_menu_items()
    for item in menu_items:
        try:
            item_id = item.id
            item_name = item.name
            category_name = item.category.name
            item_price = item.price
            item_availability = item.availability
            with st.expander(f'ID: {item_id}, Name: {item_name}, Category: {category_name}'):
                st.markdown(f"""
                    <div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">
                        <p><strong>Price:</strong> R{item_price:.2f}</p>
                        <p><strong>Availability:</strong> {item_availability}</p>
                    </div>
                """, unsafe_allow_html=True)
        except AttributeError as e:
            st.error(f"Failed to retrieve menu item information: {e}")

    #Student to place an order
    st.subheader('Place Order')
    student_name = st.text_input('Student Name')
    item_ids = [item.id for item in menu_items]
    item_id = st.selectbox('Item', item_ids, index=0 if item_ids else None)
    quantity = st.number_input('Quantity', min_value=1)
    if st.button('Place Order'):
        order = place_order(student_name, item_id, quantity)
        if order:
            st.success(f'Order placed successfully! Total price: {order.total_price:.2f}')
        else:
            st.error('Failed to place order')

    st.markdown('</div>', unsafe_allow_html=True)

elif choice == 'Pending Orders':
    st.markdown('<div class="pending-orders-section">', unsafe_allow_html=True)

    st.subheader('Pending Orders')
    orders = get_orders()
    for order in orders:
        if not st.session_state.get(f'ready_{order.id}'):
            with st.expander(f'Order ID: {order.id}, Student Name: {order.student_name}, Item: {order.item.name}'):
                st.markdown(f"""
                    <div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">
                        <p><strong>Quantity:</strong> {order.quantity}</p>
                        <p><strong>Total Price:</strong> R{order.total_price:.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f'Mark as Ready', key=order.id):
                    #Mark the order as ready and refresh the page
                    st.session_state[f'ready_{order.id}'] = True
                    st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

elif choice == 'Ready Orders':
    st.markdown('<div class="ready-orders-section">', unsafe_allow_html=True)

    st.subheader('Ready Orders')
    orders = get_orders()
    for order in orders:
        if st.session_state.get(f'ready_{order.id}'):
            with st.expander(f'Ready Order ID: {order.id}, Student Name: {order.student_name}, Item: {order.item.name}'):
                st.markdown(f"""
                    <div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">
                        <p><strong>Quantity:</strong> {order.quantity}</p>
                        <p><strong>Total Price:</strong> R{order.total_price:.2f}</p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
