import tkinter as tk
import uuid
from tkinter import ttk

from db import Executer

LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Restaurant Database Management System")
        self.geometry("750x600")

        self.ex = Executer("menu_db.sqlite")

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (HomePage, CustomerPage, ChefPage, ManagerPage):
            frame = F(container, self.ex, self)

            # initializing frame of that object from
            # HomePage, CustomerPage, ChefPage, ManagerPage respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]

        if cont == ChefPage:
            frame.refresh(self)

        frame.tkraise()


# first window frame HomePage

class HomePage(tk.Frame):
    def __init__(self, parent, executer, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Home Page", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=2, padx=10, pady=10)

        button0 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(HomePage))
        button0.grid(row=0, column=0, padx=10, pady=10)

        button1 = ttk.Button(self, text="Customer: View Menu and Order Food",
                             command=lambda: controller.show_frame(CustomerPage))
        button1.grid(row=4, column=2, padx=10, pady=20)

        button2 = ttk.Button(self, text="Chef: View Current Orders",
                             command=lambda: controller.show_frame(ChefPage))
        button2.grid(row=5, column=2, padx=10, pady=20)

        button3 = ttk.Button(self, text="Manager: View Ingredient Inventory",
                             command=lambda: controller.show_frame(ManagerPage))
        button3.grid(row=6, column=2, padx=10, pady=10)


# second window frame CustomerPage
class CustomerPage(tk.Frame):

    def __init__(self, parent, executer, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Customer Page", font=LARGEFONT)
        label.grid(row=0, column=2, padx=10, pady=10)

        self.ex = executer

        menulabel = ttk.Label(self, text="MENU:")
        menulabel.grid(row=1, column=2, padx=10, pady=10)

        button0 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(HomePage))
        button0.grid(row=0, column=0, padx=10, pady=10)

        # Fetch and display food items from the database
        food_items = self.ex.fetch_data("Food_Item", select_col=("Food_ID", "Food_Description"))

        for i, food_item in enumerate(food_items[0]):
            label = ttk.Label(self, text=food_item[1])
            label.grid(row=i + 2, column=2, padx=10, pady=10)

        # Entry for customer to input the food item they want
        food_entry_label = ttk.Label(self, text="Enter Food Item:")
        food_entry_label.grid(row=len(food_items[0]) + 2, column=2, padx=10, pady=20)

        food_entry = ttk.Entry(self)
        food_entry.grid(row=len(food_items[0]) + 3, column=2, padx=10, pady=10)

        # Submit order button
        submit_order_button = ttk.Button(self, text="Submit Order", command=lambda: self.submit_order(food_entry.get()))
        submit_order_button.grid(row=len(food_items[0]) + 4, column=2, padx=10, pady=10)

        self.ex.commit()
        # self.ex.close_connection()

    def submit_order(self, food_description):
        food_query = self.ex.list_food_id_from_name(food_description)
        order_id = str(uuid.uuid4())
        food_id = food_query[0][0]
        self.ex.insert_into("Food_Order", (order_id, food_id))

        self.ex.commit()
        # self.ex.close_connection()


# third window frame ChefPage
class ChefPage(tk.Frame):
    def __init__(self, parent, executer, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.update(self)
        tk.Frame.update_idletasks(self)
        label = ttk.Label(self, text="Chef Page", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        self.ex = executer

        button0 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(HomePage))
        button0.grid(row=0, column=0, padx=10, pady=10)

        # Fetch and display current orders for the chef
        current_orders = self.ex.fetch_data("Food_Order")
        for i, order in enumerate(current_orders[0]):
            food_name = self.ex.list_food_item_from_pk(order[1])[0][0]
            label = ttk.Label(self, text=f"Food Item: {food_name}, Order ID: {order[0]}")
            label.grid(row=i + 1, column=1, padx=10, pady=10)

        self.ex.commit()
        # self.ex.close_connection()

    def refresh(self, controller):
        # Add code here to refresh or update the content of the chef page
        current_orders = self.ex.fetch_data("Food_Order")

        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        label = ttk.Label(self, text="Chef Page", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        button0 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(HomePage))
        button0.grid(row=0, column=0, padx=10, pady=10)

        # Display updated current orders for the chef
        for i, order in enumerate(current_orders[0]):
            food_name = self.ex.list_food_item_from_pk(order[1])[0][0]
            label = ttk.Label(self, text=f"Food Item: {food_name}, Order ID: {order[0]}")
            label.grid(row=i + 1, column=1, padx=10, pady=10)

        self.ex.commit()


class ManagerPage(tk.Frame):
    def __init__(self, parent, executer, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Manager Page", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        self.ex = executer

        button0 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(HomePage))
        button0.grid(row=0, column=0, padx=10, pady=10)

        # Password entry for manager
        password_entry_label = ttk.Label(self, text="Enter Password:")
        password_entry_label.grid(row=1, column=1, padx=10, pady=10)

        password_entry = ttk.Entry(self, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Submit password button
        submit_password_button = ttk.Button(self, text="Submit Password",
                                            command=lambda: self.submit_password(password_entry.get(), controller))
        submit_password_button.grid(row=3, column=1, padx=10, pady=10)

    def submit_password(self, entered_password, controller):
        if entered_password == "manager123":
            # Fetch and display inventory for the manager
            inventory_data = self.ex.fetch_data("Manager_View",
                                                select_col=("Inventory_ID", "Ingredient_ID", "Inventory_Quantity"))
            for i, inventory in enumerate(inventory_data[0]):
                ingredient_name = self.ex.list_ingredient_name_from_pk(inventory[1])[0][0]
                label = ttk.Label(self,
                                  text=f"Ingredient: {ingredient_name}, Quantity: {inventory[2]}, Inventory ID: {inventory[0]}")
                label.grid(row=i + 4, column=1, padx=10, pady=10)
        else:
            # Display an error message or take appropriate action for incorrect password
            pass


# Driver Code
app = tkinterApp()
# app.protocol("WM_DELETE_WINDOW", app.close_connection)
app.mainloop()
