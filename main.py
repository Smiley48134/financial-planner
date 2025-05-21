import numpy as np
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from ui_gui import Ui_MainWindow
import json
class Transaction:
    

    def __init__(self,amount=0,type="",time=None):
        self.amount = amount
        self.type = type
        self.time = time if time else datetime.now()
    def __repr__(self):
        return f"{self.amount} | {self.type} | {self.time}"
    def show_amount(self):
        return self.amount


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.transactions = []
        self.ui.pushButton.clicked.connect(self.add_transaction)
        self.ui.pushButton_2.clicked.connect(self.remove_transaction)

        self.load_transactions()


    def closeEvent(self, event):
        self.save_transactions()
        event.accept()



    def save_transactions(self, filename="transactions.json"):
        try:
            with open(filename, "w") as f:
                # Convert transactions to dicts for JSON
                data = [
                    {"amount": t.amount, "type": t.type, "time": t.time}
                    for t in self.transactions
                ]
                json.dump(data, f, indent=4)
            print("Transactions saved.")
        except Exception as e:
            print(f"Error saving transactions: {e}")

    def load_transactions(self, filename="transactions.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.transactions = [
                    Transaction(**t) for t in data
                ]
            self.update_views()
            print("Transactions loaded.")
        except FileNotFoundError:
            print("No save file found.")
        except Exception as e:
            print(f"Error loading transactions: {e}")


    def add_transaction(self):
        name = self.ui.name.text().strip()
        amount_text = self.ui.amounts.text().strip()
        date = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm")

        if not name or not amount_text:
            return

        try:
            amount = float(amount_text)
        except ValueError:
            return

        if self.ui.radioButton_2.isChecked():  # Expense
            amount = -abs(amount)
        else:  # Income
            amount = abs(amount)

        transaction = Transaction(amount, name, date)
        self.transactions.append(transaction)

        self.update_views()
        self.ui.name.clear()
        self.ui.amounts.clear()

    def remove_transaction(self):
        name_to_remove = self.ui.removename.text().strip()
        self.transactions = [t for t in self.transactions if t.type != name_to_remove]
        self.update_views()
        self.ui.removename.clear()

    def update_views(self):
        income_model = QtCore.QStringListModel()
        expense_model = QtCore.QStringListModel()

        income_items = [str(t) for t in self.transactions if t.amount > 0]
        expense_items = [str(t) for t in self.transactions if t.amount < 0]
        total_value = sum(t.amount for t in self.transactions)

        income_model.setStringList(income_items)
        expense_model.setStringList(expense_items)

        self.ui.income.setModel(income_model)
        self.ui.expenses.setModel(expense_model)

        self.ui.total.clear()
        self.ui.total.addItem(f"Total Balance: {total_value:.2f}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())