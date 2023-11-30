import sqlite3
import uuid


class Executer:

    def __init__(self, file_path):
        self.__conn = sqlite3.connect(file_path)
        self.__cursor = self.__conn.cursor()

    def insert_table(self,
                     table_name: str,
                     *args) -> None:
        execution_string = "CREATE TABLE IF NOT EXISTS " + table_name + "("

        for i in args:
            execution_string += i + ", "

        execution_string = execution_string[:-2] + ");"

        self.__cursor.execute(execution_string.upper())

    def list_tables(self) -> list:
        command = "SELECT name FROM sqlite_master WHERE type='table';"
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def list_food_item_from_pk(self, pk) -> list:
        command = "SELECT FOOD_DESCRIPTION FROM FOOD_ITEM WHERE FOOD_ID='{}'".format(pk)
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def list_food_id_from_name(self, name) -> list:
        command = "SELECT FOOD_ID FROM FOOD_ITEM WHERE FOOD_DESCRIPTION='{}'".format(name.upper())
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def list_ingredient_name_from_pk(self, name) -> list:
        command = "SELECT INGREDIENT_NAME FROM INGREDIENT WHERE INGREDIENT_ID='{}'".format(name.upper())
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def insert_into(self,
                    table_name: str,
                    values: tuple,
                    columns=None):

        base_string = "INSERT INTO " + table_name

        if columns is not None:
            base_string += str(columns)
            if len(columns) == 1:
                base_string = base_string[:-2] + ")"

        if len(values) == 1:
            base_string += " VALUES" + " " + str(values)
            base_string = base_string[:-2] + ");"
        else:
            base_string += " VALUES" + " " + str(values) + ";"

        self.__cursor.execute(base_string.upper())

    def delete_from_table(self,
                          table_name: str,
                          *args):

        query = "DELETE FROM {}".format(table_name)

        for i in args:
            query += " " + i

        self.__cursor.execute(query.upper())

    def delete_all_data(self):

        tables_order = [
            "MANAGER",
            "INVENTORY",
            "CHEF",
            "BILL",
            "WAITER",
            "CUSTOMER",
            "FOOD_ORDER",
            "FOOD_ITEM",
            "INGREDIENT",
            "SUPPLIER"
        ]

        for table_name in tables_order:
            self.delete_from_table(table_name)

    def fetch_data(self,
                   table: str,
                   *args,
                   select_col=None,
                   ret_str=False):

        base_str = "SELECT"
        if select_col is None:
            base_str += " *"
        else:
            base_str += " "
            for i in select_col:
                base_str += i + ", "
            base_str = base_str[:-2]

        base_str += " FROM {}".format(table)

        for i in args:
            base_str += " " + i

        self.__cursor.execute(base_str.upper() + ";")

        if ret_str:
            return base_str.upper() + ";"
        else:
            return self.__cursor.fetchall(),

    def make_view(self,
                  view_name: str,
                  table: str,
                  *args,
                  select_col=None):

        create_str = "CREATE VIEW {} AS".format(view_name)

        base_str = self.fetch_data(table,
                                   *args,
                                   select_col=select_col,
                                   ret_str=True)

        full_str = create_str + " " + base_str

        self.__cursor.execute(full_str.upper())

    def close_connection(self):
        self.__conn.close()

    def commit(self):
        self.__conn.commit()


if __name__ == '__main__':
    executer = Executer("menu_db.sqlite")

    # Customer table
    command_list = ["Customer_ID VARCHAR(100) PRIMARY KEY",
                    "Customer_Name VARCHAR(100) NOT NULL"]
    executer.insert_table("Customer", *command_list)

    # Supplier table
    command_list = ["Supplier_ID VARCHAR(100) PRIMARY KEY",
                    "Supplier_Name VARCHAR(100) NOT NULL",
                    "Address VARCHAR(100) NOT NULL",
                    "Zip_Code VARCHAR(100) NOT NULL",
                    "Country VARCHAR(100) NOT NULL",
                    "State VARCHAR(100) NOT NULL"]
    executer.insert_table("Supplier", *command_list)

    # Ingredient table
    command_list = ["Ingredient_ID VARCHAR(100) PRIMARY KEY",
                    "Ingredient_Name VARCHAR(100) NOT NULL",
                    "Quantity_Used INTEGER NOT NULL",
                    "Expiration_Date DATE NOT NULL",
                    "Supplier_ID VARCHAR(100) NOT NULL",
                    "FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID)"]
    executer.insert_table("Ingredient", *command_list)

    # Food Item table
    command_list = ["Food_ID VARCHAR(100) PRIMARY KEY",
                    "Food_Description VARCHAR(100) NOT NULL",
                    "Quantity INTEGER NOT NULL",
                    "Ingredient_ID VARCHAR(100) NOT NULL",
                    "FOREIGN KEY (Ingredient_ID) REFERENCES Ingredient(Ingredient_ID)"]
    executer.insert_table("Food_Item", *command_list)

    # Order table
    command_list = ["Order_ID VARCHAR(100) PRIMARY KEY",
                    "Food_ID VARCHAR(100) NOT NULL",
                    "FOREIGN KEY (Food_ID) REFERENCES Food_Item(Food_ID)"]
    executer.insert_table("Food_Order", *command_list)

    # Waiter table
    command_list = ["Waiter_ID VARCHAR(100) PRIMARY KEY",
                    "Customer_ID VARCHAR(100) NOT NULL",
                    "Order_ID VARCHAR(100) NOT NULL",
                    "FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)",
                    "FOREIGN KEY (Order_ID) REFERENCES Food_Order(Order_ID)"]
    executer.insert_table("Waiter", *command_list)

    # Bill table
    command_list = ["Bill_ID VARCHAR(100) PRIMARY KEY",
                    "Order_ID VARCHAR(100) NOT NULL",
                    "FOREIGN KEY (Order_ID) REFERENCES Food_Order(Order_ID)"]
    executer.insert_table("Bill", *command_list)

    # Chef table
    command_list = ["Chef_ID VARCHAR(100) PRIMARY KEY",
                    "Chef_Name VARCHAR(100) NOT NULL",
                    "Order_ID VARCHAR(100) NOT NULL",
                    "FOREIGN KEY (Order_ID) REFERENCES Food_Order(Order_ID)"]
    executer.insert_table("Chef", *command_list)

    # Inventory table
    command_list = ["Inventory_ID VARCHAR(100) PRIMARY KEY",
                    "Ingredient_ID VARCHAR(100) NOT NULL",
                    "Inventory_Quantity INTEGER NOT NULL",
                    "FOREIGN KEY (Ingredient_ID) REFERENCES Ingredient(Ingredient_ID)"]
    executer.insert_table("Inventory", *command_list)

    # Manager table
    command_list = ["Manager_ID VARCHAR(100) PRIMARY KEY",
                    "Inventory_ID VARCHAR(100) NOT NULL",
                    "FOREIGN KEY (Inventory_ID) REFERENCES Inventory(Inventory_ID)"]

    executer.insert_table("Manager", *command_list)

    customer_1 = str(uuid.uuid4())
    customer_2 = str(uuid.uuid4())
    customer_3 = str(uuid.uuid4())

    chef_1 = str(uuid.uuid4())
    chef_2 = str(uuid.uuid4())
    chef_3 = str(uuid.uuid4())

    ingredient_1 = str(uuid.uuid4())
    ingredient_2 = str(uuid.uuid4())
    ingredient_3 = str(uuid.uuid4())

    food_item_1 = str(uuid.uuid4())
    food_item_2 = str(uuid.uuid4())
    food_item_3 = str(uuid.uuid4())

    order_1 = str(uuid.uuid4())
    order_2 = str(uuid.uuid4())
    order_3 = str(uuid.uuid4())

    waiter_1 = str(uuid.uuid4())
    waiter_2 = str(uuid.uuid4())
    waiter_3 = str(uuid.uuid4())

    bill_1 = str(uuid.uuid4())
    bill_2 = str(uuid.uuid4())
    bill_3 = str(uuid.uuid4())

    supplier_1 = str(uuid.uuid4())
    supplier_2 = str(uuid.uuid4())
    supplier_3 = str(uuid.uuid4())

    inventory_ingredient_1 = str(uuid.uuid4())
    inventory_ingredient_2 = str(uuid.uuid4())
    inventory_ingredient_3 = str(uuid.uuid4())

    inventory_1 = str(uuid.uuid4())
    inventory_2 = str(uuid.uuid4())
    inventory_3 = str(uuid.uuid4())

    manager_1 = str(uuid.uuid4())
    manager_2 = str(uuid.uuid4())
    manager_3 = str(uuid.uuid4())

    role_admin = str(uuid.uuid4())
    role_shipper = str(uuid.uuid4())
    role_recipient = str(uuid.uuid4())

    user_1 = str(uuid.uuid4())
    user_2 = str(uuid.uuid4())
    user_3 = str(uuid.uuid4())

    executer.insert_into("Customer", (customer_1, "Mike"))
    executer.insert_into("Customer", (customer_2, "Adam"),
                         columns=("Customer_ID",
                                  "Customer_Name",))
    executer.insert_into("Customer", (customer_3, "John"),
                         columns=("Customer_ID",
                                  "Customer_Name",))

    print("Inserted data into the {} table".format("Customer"))
    # ---------------------------------------------------------------------------------------------
    executer.insert_into("Chef", (chef_1, "Josh", order_1))
    executer.insert_into("Chef", (chef_2, "Sarah", order_2))
    executer.insert_into("Chef", (chef_3, "Liam", order_3))

    print("Inserted data into the {} table".format("Chef"))
    # ----------------------------------------------------------------------------------------------
    executer.insert_into("Ingredient", (ingredient_1, "Tomato", "5", "2023-01-01", supplier_1))
    executer.insert_into("Ingredient", (ingredient_2, "Onion", "8", "2023-02-01", supplier_2))
    executer.insert_into("Ingredient", (ingredient_3, "Rice", "10", "2023-03-01", supplier_3))

    print("Inserted data into the {} table".format("Ingredient"))
    # ----------------------------------------------------------------------------------------------
    executer.insert_into("Food_Item", (food_item_1, "Pasta", "3", ingredient_1))
    executer.insert_into("Food_Item", (food_item_2, "Soup", "2", ingredient_2))
    executer.insert_into("Food_Item", (food_item_3, "Fried Rice", "4", ingredient_3))

    print("Inserted data into the {} table".format("Food_Item"))
    # ----------------------------------------------------------------------------------------------
    executer.insert_into("Food_Order", (order_1, food_item_1))
    executer.insert_into("Food_Order", (order_2, food_item_2))
    executer.insert_into("Food_Order", (order_3, food_item_3))

    print("Inserted data into the {} table".format("Food_Order"))
    # ----------------------------------------------------------------------------------------------

    executer.insert_into("Waiter", (waiter_1, customer_1, order_1))
    executer.insert_into("Waiter", (waiter_2, customer_2, order_2))
    executer.insert_into("Waiter", (waiter_3, customer_3, order_3))

    print("Inserted data into the {} table".format("Waiter"))

    # ----------------------------------------------------------------------------------------------

    executer.insert_into("Bill", (bill_1, order_1))
    executer.insert_into("Bill", (bill_2, order_2))
    executer.insert_into("Bill", (bill_3, order_3))

    print("Inserted data into the {} table".format("Bill"))

    # ----------------------------------------------------------------------------------------------

    executer.insert_into("Supplier", (supplier_1, "Supplier", "Address", "Zip", "Country", "State"))
    executer.insert_into("Supplier", (supplier_2, "Supplier", "Address", "Zip", "Country", "State"))
    executer.insert_into("Supplier", (supplier_3, "Supplier", "Address", "Zip", "Country", "State"))

    print("Inserted data into the {} table".format("Supplier"))

    # ----------------------------------------------------------------------------------------------

    executer.insert_into("Inventory", (inventory_1, ingredient_1, 20))
    executer.insert_into("Inventory", (inventory_2, ingredient_2, 15))
    executer.insert_into("Inventory", (inventory_3, ingredient_3, 10))

    print("Inserted data into the {} table".format("Inventory"))

    # ----------------------------------------------------------------------------------------------

    executer.insert_into("Manager", (manager_1, inventory_1))
    executer.insert_into("Manager", (manager_2, inventory_2))
    executer.insert_into("Manager", (manager_3, inventory_3))

    print("Inserted data into the {} table".format("Manager"))

    # ----------------------------------------------------------------------------------------------

    executer.make_view("Customer_View",
                       "Food_Item",
                       select_col=("Food_ID",
                                   "Food_Description"))

    executer.make_view("Chef_View",
                       "Food_Order",
                       select_col=("Order_ID",
                                   "Food_ID"))

    executer.make_view("Manager_View",
                       "Inventory",
                       select_col=("Inventory_ID",
                                   "Ingredient_ID",
                                   "Inventory_Quantity"))

    print("Created the {}, {}, and {} views".format("CUSTOMER",
                                                    "CHEF",
                                                    "MANAGER"))

    executer.commit()
    executer.close_connection()


