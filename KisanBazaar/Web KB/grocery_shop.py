import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea, QMainWindow,
    QGridLayout, QMessageBox, QListWidget, QListWidgetItem,
    QFrame, QFileDialog, QLineEdit, QComboBox, QToolButton, QMenu,
    QDialog, QFormLayout, QDialogButtonBox, QRadioButton
)
from PyQt6.QtGui import QPixmap, QFont, QTextDocument, QAction, QIntValidator
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer


class GroceryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KisanBazaar")
        self.resize(1200, 700)

        self.cart = []
        self.products = self.load_products()
        self.filtered_products = self.products.copy()
        self.selected_payment_method = "Cash"
        self.init_intro_screen()

    def load_products(self):
        try:
            with open("products.json", "r") as file:
                return json.load(file)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products.json: {e}")
            return {}
    def init_intro_screen(self):
        intro_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_row = QHBoxLayout()
        cart_icon = QLabel("🛒")
        cart_icon.setFont(QFont("Segoe UI Emoji", 48))

        title = QLabel("KisanBazaar")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: #212529;")
        title_row.addWidget(cart_icon)
        title_row.addSpacing(10)
        title_row.addWidget(title)

        tagline = QLabel("Fresh. Local. Delivered Fast.")
        tagline.setFont(QFont("Segoe UI", 18))
        tagline.setStyleSheet("color: #6c757d;")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        description = QLabel(
            "Welcome to KisanBazaar - your one-stop destination for farm-fresh vegetables, pulses, dairy, and more. "
            "We deliver quality directly from local farmers to your doorstep. Support local, eat fresh!"
        )
        description.setWordWrap(True)
        description.setFont(QFont("Segoe UI", 14))
        description.setStyleSheet("color: #495057; padding: 0 40px;")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_btn = QPushButton("🏍️ Start Shopping")
        self.start_btn.setFont(QFont("Arial", 16))
        self.start_btn.setFixedSize(220, 50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        self.start_btn.clicked.connect(self.init_grocery_screen)

        layout.addLayout(title_row)
        layout.addWidget(tagline)
        layout.addWidget(description)
        layout.addSpacing(30)
        layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        intro_widget.setLayout(layout)
        intro_widget.setStyleSheet("background-color: #f8f9fa;")
        self.setCentralWidget(intro_widget)

    def intro_key_event(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.start_btn.click()
    def init_grocery_screen(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # ----- Sidebar -----
        sidebar_nav = QVBoxLayout()
        sidebar_nav.setAlignment(Qt.AlignmentFlag.AlignTop)

        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(180)
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #343a40;
                color: white;
                border-right: 2px solid #dee2e6;
            }
            QPushButton {
                background-color: #343a40;
                color: white;
                border: none;
                padding: 14px 20px;
                font-size: 16px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #495057;
            }
        """)

        home_btn = QPushButton("🏠 Home")
        home_btn.clicked.connect(self.init_intro_screen)

        shop_btn = QPushButton("🛒 Shop")
        shop_btn.clicked.connect(self.init_grocery_screen)

        orders_btn = QPushButton("📜 My Orders")
        orders_btn.clicked.connect(self.show_order_history)

        about_btn = QPushButton("ℹ️ About")
        about_btn.clicked.connect(self.show_about_info)

        exit_btn = QPushButton("🚪 Exit")
        exit_btn.clicked.connect(self.close)

        sidebar_nav.addWidget(home_btn)
        sidebar_nav.addWidget(shop_btn)
        sidebar_nav.addWidget(orders_btn)
        sidebar_nav.addWidget(about_btn)
        sidebar_nav.addStretch()
        sidebar_nav.addWidget(exit_btn)

        sidebar_widget.setLayout(sidebar_nav)
        main_layout.addWidget(sidebar_widget)

        # ----- Left Panel -----
        left_panel = QVBoxLayout()
        filter_bar = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search products...")
        self.search_bar.setFixedHeight(40)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ced4da;
                border-radius: 20px;
                padding-left: 15px;
                font-size: 15px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #0d6efd;
                background-color: #f8f9fa;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_products)

        self.category_dropdown = QToolButton()
        self.category_dropdown.setText("📂 Categories")
        self.category_dropdown.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.category_menu = QMenu()
        all_action = QAction("All Categories", self)
        all_action.triggered.connect(lambda: self.category_filter_handler("All Categories"))
        self.category_menu.addAction(all_action)

        for category in self.products:
            action = QAction(category, self)
            action.triggered.connect(lambda _, c=category: self.category_filter_handler(c))
            self.category_menu.addAction(action)

        self.category_dropdown.setMenu(self.category_menu)
        self.category_dropdown.setStyleSheet("""
            QToolButton {
                background-color: #f1f3f5;
                border: 2px solid #ced4da;
                border-radius: 20px;
                padding: 8px 16px;
                font-size: 15px;
            }
            QToolButton::menu-indicator {
                image: none;
            }
        """)

        self.current_category = "All Categories"
        filter_bar.addWidget(self.search_bar, 3)
        filter_bar.addSpacing(10)
        filter_bar.addWidget(self.category_dropdown, 1)
        left_panel.addLayout(filter_bar)

        self.product_area = QScrollArea()
        self.product_area.setWidgetResizable(True)

        self.product_widget = QWidget()
        self.product_layout = QVBoxLayout(self.product_widget)
        self.product_area.setWidget(self.product_widget)
        left_panel.addWidget(self.product_area)

        # Add scroll buttons
        scroll_buttons = QHBoxLayout()
        scroll_to_top_btn = QPushButton("⬆️ Top")
        scroll_to_bottom_btn = QPushButton("⬇️ Bottom")

        scroll_to_top_btn.setStyleSheet("padding: 6px; background-color: #198754; color: white; border-radius: 6px;")
        scroll_to_bottom_btn.setStyleSheet("padding: 6px; background-color: #0d6efd; color: white; border-radius: 6px;")

        scroll_to_top_btn.clicked.connect(lambda: self.product_area.verticalScrollBar().setValue(0))
        scroll_to_bottom_btn.clicked.connect(lambda: self.product_area.verticalScrollBar().setValue(self.product_area.verticalScrollBar().maximum()))

        scroll_buttons.addWidget(scroll_to_top_btn)
        scroll_buttons.addWidget(scroll_to_bottom_btn)
        left_panel.addLayout(scroll_buttons)

        self.render_products()
        # ----- Cart Sidebar -----
        cart_layout = QVBoxLayout()
        cart_layout.setContentsMargins(15, 15, 15, 15)
        cart_layout.setSpacing(15)

        cart_title = QLabel("🛒 Your Cart")
        cart_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        cart_title.setStyleSheet("color: #212529;")

        self.cart_list = QListWidget()
        self.cart_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 15px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 6px;
            }
            QListWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
        """)

        remove_btn = QPushButton("❌ Remove Selected")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bb2d3b;
            }
        """)
        remove_btn.clicked.connect(self.remove_selected_item)

        self.total_label = QLabel("Total: ₹0")
        self.total_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #212529;")

        pay_button = QPushButton("💳 Place Order")
        pay_button.setFixedHeight(40)
        pay_button.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        pay_button.clicked.connect(self.show_bill)

        cart_layout.addWidget(cart_title)
        cart_layout.addWidget(self.cart_list)
        cart_layout.addWidget(remove_btn)
        cart_layout.addWidget(self.total_label)
        cart_layout.addWidget(pay_button)

        sidebar = QWidget()
        sidebar.setLayout(cart_layout)
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-left: 2px solid #dee2e6;
            }
        """)

        main_layout.addLayout(left_panel, 3)
        main_layout.addWidget(sidebar, 1)
        self.setCentralWidget(main_widget)

    def show_order_history(self):
        try:
            with open("customer_bill.txt", "r", encoding="utf-8") as f:
                history = f.read().strip()
            if not history:
                history = "🕒 No order history found."
        except FileNotFoundError:
            history = "🕒 No order history file found."

        dlg = QDialog(self)
        dlg.setWindowTitle("📜 My Orders")
        dlg.resize(500, 400)
        layout = QVBoxLayout()

        label = QLabel("Your Past Orders:")
        label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(label)

        history_label = QLabel(history)
        history_label.setFont(QFont("Consolas", 10))
        history_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        history_label.setStyleSheet("background-color: #f1f1f1; padding: 10px; border: 1px solid #ccc;")
        history_label.setWordWrap(True)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(history_label)
        layout.addWidget(scroll)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dlg.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        dlg.setLayout(layout)
        dlg.exec()

    def show_about_info(self):
        QMessageBox.information(
            self, "About KisanBazaar",
            "🌾 KisanBazaar is a modern grocery shopping application\n"
            "designed to support local farmers and deliver quality\n"
            "products to your doorstep.\n\nBuilt with ❤️ using PyQt6."
        )
    def category_filter_handler(self, cat):
        self.current_category = cat
        self.filter_products()

    def filter_products(self):
        keyword = self.search_bar.text().lower()
        selected_cat = self.current_category
        self.filtered_products = {}

        for cat, items in self.products.items():
            if selected_cat != "All Categories" and cat != selected_cat:
                continue
            filtered = [item for item in items if keyword in item["name"].lower()]
            if filtered:
                self.filtered_products[cat] = filtered

        self.render_products()

    def render_products(self):
        for i in reversed(range(self.product_layout.count())):
            item = self.product_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                self.product_layout.removeItem(item)

        for category, items in self.filtered_products.items():
            cat_label = QLabel(f"🛍️  <b style='font-size:22px;'>{category}</b>")
            cat_label.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #1976D2;
                    background-color: #E3F2FD;
                    padding: 10px 18px;
                    border-radius: 12px;
                    border: 2px solid #64B5F6;
                    margin: 15px 10px 5px 10px;
                }
            """)
            grid = QGridLayout()
            grid.setHorizontalSpacing(20)
            grid.setVerticalSpacing(20)

            for i, item in enumerate(items):
                grid.addWidget(self.create_product_card(item), i // 3, i % 3)

            self.product_layout.addWidget(cat_label)
            self.product_layout.addLayout(grid)

        self.product_layout.addSpacing(100)

    def create_product_card(self, item):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #dee2e6;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image = QLabel()
        pixmap = QPixmap(item.get("image", "")) if os.path.exists(item.get("image", "")) else QPixmap()
        if pixmap.isNull():
            image.setText("🧺")
            image.setFont(QFont("Arial", 42))
        else:
            image.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name = QLabel(item["name"])
        name.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        unit = item.get("unit", "")
        price = QLabel(f"₹{item['price']} / {unit}" if unit else f"₹{item['price']}")
        price.setFont(QFont("Arial", 13))
        price.setStyleSheet("color: #6c757d; padding: 4px; border: 1px solid #dee2e6; border-radius: 6px; background-color: #f8f9fa;")
        price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        qty_selector = QComboBox()
        qty_selector.setStyleSheet("""
            QComboBox {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-width: 90px;
            }
        """)
        for i in range(1, item.get("stock", 10) + 1):
            qty_selector.addItem(str(i))

        add_btn = QPushButton("Add to Cart")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        add_btn.clicked.connect(lambda _, i=item, q=qty_selector: self.add_to_cart(i, int(q.currentText())))

        layout.addWidget(image)
        layout.addWidget(name)
        layout.addWidget(price)
        layout.addWidget(qty_selector)
        layout.addWidget(add_btn)

        card.setLayout(layout)
        return card
    def add_to_cart(self, item, quantity):
        current_stock = item.get("stock", 10)
        if quantity > current_stock:
            QMessageBox.warning(self, "Stock Error", f"Only {current_stock} in stock!")
            return

        item["stock"] = current_stock - quantity
        self.cart.append((item, quantity))
        self.cart_list.addItem(QListWidgetItem(f"{item['name']} x{quantity} - ₹{item['price'] * quantity}"))
        self.update_total()

    def remove_selected_item(self):
        selected_items = self.cart_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No Selection", "Please select an item to remove.")
            return

        for item_widget in selected_items:
            row = self.cart_list.row(item_widget)
            item_data, quantity = self.cart[row]
            item_data["stock"] += quantity  # restore stock
            self.cart_list.takeItem(row)
            del self.cart[row]

        self.update_total()

    def update_total(self):
        total = sum(item['price'] * qty for item, qty in self.cart)
        self.total_label.setText(f"Total: ₹{total}")
    def show_upi_qr_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Pay via UPI")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📱 Scan this QR to pay:"))

        qr = QLabel()
        qr.setPixmap(QPixmap("upi_qr.png").scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        qr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(qr)

        done_btn = QPushButton("Done")
        done_btn.clicked.connect(dialog.accept)
        layout.addWidget(done_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        dialog.setLayout(layout)
        dialog.exec()

    def get_card_details(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Enter Card Details")
        layout = QFormLayout()

        card_number = QLineEdit()
        card_number.setPlaceholderText("1234 5678 9012 3456")
        card_number.setMaxLength(19)
        layout.addRow("Card Number:", card_number)

        expiry = QLineEdit()
        expiry.setPlaceholderText("MM/YY")
        layout.addRow("Expiry Date:", expiry)

        cvv = QLineEdit()
        cvv.setPlaceholderText("CVV")
        cvv.setEchoMode(QLineEdit.EchoMode.Password)
        cvv.setValidator(QIntValidator(100, 999))
        layout.addRow("CVV:", cvv)

        name = QLineEdit()
        name.setPlaceholderText("Name on Card")
        layout.addRow("Name:", name)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return {
                "card_number": card_number.text(),
                "expiry": expiry.text(),
                "cvv": cvv.text(),
                "name": name.text()
            }
        return None

    def show_payment_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Payment Method")
        dialog.setFixedSize(350, 220)

        layout = QVBoxLayout()
        title = QLabel("💳 Select Payment Method")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.payment_options = {
            "Cash": QRadioButton("💵 Cash"),
            "Card": QRadioButton("💳 Card"),
            "UPI": QRadioButton("📱 UPI")
        }
        self.payment_options["Cash"].setChecked(True)

        for btn in self.payment_options.values():
            btn.setFont(QFont("Segoe UI", 13))
            layout.addWidget(btn)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.setStyleSheet("""
            QDialog { background-color: #ffffff; border-radius: 8px; }
            QRadioButton { padding: 6px; }
            QDialogButtonBox QPushButton {
                background-color: #0d6efd; color: white; padding: 6px 12px; border-radius: 5px;
            }
            QDialogButtonBox QPushButton:hover { background-color: #0b5ed7; }
        """)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            for method, btn in self.payment_options.items():
                if btn.isChecked():
                    return method
        return None
    def show_loading_dialog(self, message="Processing..."):
      dialog = QDialog(self)
      dialog.setWindowTitle("⏳ Please Wait")
      layout = QVBoxLayout()
      label = QLabel(message)
      label.setFont(QFont("Arial", 13))
      label.setAlignment(Qt.AlignmentFlag.AlignCenter)
      layout.addWidget(label)
      dialog.setLayout(layout)
      dialog.setModal(True)
      dialog.setFixedSize(300, 100)

    # Close after 2.5 seconds
      QTimer.singleShot(2500, dialog.accept)
      dialog.exec()

    def show_bill(self):
        if not self.cart:
            QMessageBox.information(self, "Cart Empty", "🛒 Please add items to cart.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Order",
            "Are you sure you want to place this order?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        payment_method = self.show_payment_dialog()
        if not payment_method:
            QMessageBox.information(self, "Cancelled", "Returning to Shop.")
            self.init_grocery_screen()
            return
        
        loading = QMessageBox(self)
        loading.setWindowTitle("Processing Payment")
        #loading.setText("⏳ Processing your card payment, please wait...")
        #loading.setStandardButtons(QMessageBox.StandardButton.NoButton)
        loading.show()
        QApplication.processEvents()
        import time
        time.sleep(2.5)  # Simulate 2.5 seconds delay
        loading.close()

        self.selected_payment_method = payment_method

        if payment_method == "UPI":
            self.show_upi_qr_dialog()
        elif payment_method == "Card":
            card_info = self.get_card_details()
            if not card_info:
                QMessageBox.information(self, "Cancelled", "Returning to Shop.")
                self.init_grocery_screen()
                return

        total = 0
        bill_lines = [
            "====================================",
            "         GROCERY SHOP BILL",
            "====================================",
            f"{'Item':<20}{'Qty':<5}{'Price':>7}"
        ]

        for item, qty in self.cart:
            cost = item['price'] * qty
            bill_lines.append(f"{item['name']:<20}{qty:<5}₹{cost:>6}")
            total += cost

        bill_lines.append("------------------------------------")
        bill_lines.append(f"{'Total Amount:':<25}₹{total:>6}")
        bill_lines.append(f"{'Payment Mode:':<25}{self.selected_payment_method}")
        bill_lines.append("====================================")

        bill_text = "\n".join(bill_lines)
        QMessageBox.information(self, "Payment Successful", bill_text)

        save_pdf = QMessageBox.question(
            self,
            "Save as PDF",
            "Do you want to save the bill as PDF?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if save_pdf == QMessageBox.StandardButton.Yes:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "bill.pdf", "PDF Files (*.pdf)")
            if file_path:
                self.export_bill_to_pdf(bill_text, file_path)

        with open("customer_bill.txt", "a", encoding="utf-8") as f:
            f.write("\n" + bill_text + "\n")

        self.cart.clear()
        self.cart_list.clear()
        self.update_total()

    def export_bill_to_pdf(self, text, filename):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(filename)
        doc = QTextDocument()
        doc.setPlainText(text)
        doc.print(printer)

# 🚀 Entry Point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GroceryApp()
    window.show()
    sys.exit(app.exec())
