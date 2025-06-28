import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

if "rerun" not in st.session_state:
    st.session_state["rerun"] = False

if st.session_state["rerun"]:
    st.session_state["rerun"] = False
    st.experimental_set_query_params()

def login_page():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.error("Please enter both email and password.")
            return

        try:
            response = requests.post(f"{BASE_URL}/user/login", params={"email": email, "password": password})
            if response.status_code == 200:
                user = response.json()
                st.session_state["user"] = user
                st.success(f"Logged in as {user['role'].capitalize()}!")
                st.session_state["rerun"] = True
            else:
                st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the server: {e}")

def signup_page():
    st.title("Signup")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Signup"):
        if not name or not email or not password:
            st.error("Please fill in all the fields.")
            return

        response = requests.post(f"{BASE_URL}/user/signup", json={
            "name": name,
            "email": email,
            "password": password,
            "role": role
        })
        if response.status_code == 201:
            st.success("Signup successful! Please login.")
        else:
            st.error(response.json().get("detail", "Unknown error"))

def fetch_inventory():
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching inventory: {e}")
        return []

def fetch_item_name(item_id):
    inventory = fetch_inventory()
    for item in inventory:
        if item["inventory_id"] == item_id:
            return item["name"]
    return "Unknown"

def user_page():
    st.title("User Dashboard")
    st.write("Welcome to your dashboard!")

    # View Inventory
    st.subheader("View Inventory")
    if st.button("Refresh Inventory"):
        inventory = fetch_inventory()
        if inventory:
            for item in inventory:
                st.write(f"- ID: {item['inventory_id']}, {item['name']} ({item['category']}): {item['quantity']} available")
        else:
            st.write("No inventory available.")

    # View User's Orders
    st.subheader("My Orders")
    if st.button("Refresh Orders"):
        user_id = st.session_state["user"]["user_id"]
        try:
            response = requests.get(f"{BASE_URL}/order")
            if response.status_code == 200:
                orders = response.json()
                user_orders = [order for order in orders if order["user_id"] == user_id]
                if user_orders:
                    for order in user_orders:
                        item_name = fetch_item_name(order["inventory_id"])
                        st.write(f"- Order ID: {order['order_id']}, Item: {item_name}, Quantity: {order['quantity']}")
                else:
                    st.write("No orders placed yet.")
            else:
                st.error("Failed to load orders.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching orders: {e}")

    # Place Order
    st.subheader("Place Order")
    inventory_id = st.text_input("Inventory ID")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    if st.button("Place Order"):
        user_id = st.session_state["user"]["user_id"]
        try:
            response = requests.post(f"{BASE_URL}/order", json={
                "user_id": user_id,
                "inventory_id": inventory_id,
                "quantity": quantity,
                "order_date": "2024-12-10"
            })
            if response.status_code == 201:
                st.success("Order placed successfully!")
            else:
                st.error(f"Failed to place order: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error placing order: {e}")

def admin_page():
    st.title("Admin Dashboard")
    st.write("Welcome to the admin dashboard!")

    # View Inventory
    st.subheader("View Inventory")
    if st.button("Refresh Inventory"):
        inventory = fetch_inventory()
        if inventory:
            for item in inventory:
                st.write(f"- ID: {item['inventory_id']}, {item['name']} ({item['category']}): {item['quantity']} available (Threshold: {item['threshold']})")
        else:
            st.write("No inventory available.")

    # Add Inventory
    st.subheader("Add Inventory")
    name = st.text_input("Item Name")
    category = st.text_input("Category")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    threshold = st.number_input("Threshold", min_value=0, step=1)
    if st.button("Add Inventory"):
        try:
            response = requests.post(f"{BASE_URL}/inventory", json={
                "name": name,
                "category": category,
                "quantity": quantity,
                "threshold": threshold
            })
            if response.status_code == 201:
                st.success("Inventory added successfully!")
            else:
                st.error(f"Failed to add inventory: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error adding inventory: {e}")

    # Delete Inventory
    st.subheader("Delete Inventory Item")
    delete_inventory_id = st.text_input("Inventory ID to Delete")
    if st.button("Delete Inventory"):
        try:
            response = requests.delete(f"{BASE_URL}/inventory/{delete_inventory_id}")
            if response.status_code == 204:
                st.success(f"Inventory item ID {delete_inventory_id} deleted successfully!")
            else:
                st.error(f"Failed to delete inventory: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting inventory: {e}")

    # View All Orders
    st.subheader("All Orders")
    if st.button("Refresh Orders"):
        try:
            response = requests.get(f"{BASE_URL}/order")
            if response.status_code == 200:
                orders = response.json()
                if orders:
                    for order in orders:
                        item_name = fetch_item_name(order["inventory_id"])
                        st.write(f"- Order ID: {order['order_id']}, User ID: {order['user_id']}, Item: {item_name}, Quantity: {order['quantity']}")
                else:
                    st.write("No orders placed yet.")
            else:
                st.error("Failed to load orders.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching orders: {e}")

    # Delete User
    st.subheader("Delete User")
    delete_user_id = st.text_input("User ID to Delete")
    if st.button("Delete User"):
        try:
            response = requests.delete(f"{BASE_URL}/user/{delete_user_id}")
            if response.status_code == 204:
                st.success(f"User ID {delete_user_id} deleted successfully!")
            else:
                st.error(f"Failed to delete user: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting user: {e}")

    # View All Users
    st.subheader("View All Users")
    if st.button("Refresh Users"):
        try:
            response = requests.get(f"{BASE_URL}/user")
            if response.status_code == 200:
                users = response.json()
                for user in users:
                    st.write(f"- ID: {user['user_id']}, Name: {user['name']} ({user['role']})")
            else:
                st.error("Failed to load users.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching users: {e}")

def navigate():
    if st.session_state["user"]["role"] == "admin":
        admin_page()
    else:
        user_page()

def main():
    st.sidebar.title("Navigation")
    if "user" in st.session_state:
        st.sidebar.write(f"Logged in as {st.session_state['user']['name']} ({st.session_state['user']['role'].capitalize()})")
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]  # Clear all session state
            st.session_state["rerun"] = True
        else:
            navigate()
    else:
        option = st.sidebar.radio("Menu", ["Login", "Signup"])
        if option == "Login":
            login_page()
        elif option == "Signup":
            signup_page()

if __name__ == "__main__":
    main()
