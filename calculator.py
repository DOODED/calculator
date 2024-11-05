import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLineEdit, QLabel, QDialog, QListWidget,
                             QHBoxLayout, QVBoxLayout, QStyle, QScrollArea)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import uic
import math


class HistoryDialog(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculation History")
        self.setMinimumSize(400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
        """)

        # Create layout
        layout = QVBoxLayout()

        # Add header
        header_label = QLabel("Calculation History")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Create list widget for history
        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)
        self.history_list.setSpacing(2)

        # Add history items
        for item in reversed(history):
            self.history_list.addItem(item)

        layout.addWidget(self.history_list)

        # Add buttons
        button_layout = QHBoxLayout()

        clear_button = QPushButton("Clear History")
        clear_button.clicked.connect(self.clear_history)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        button_layout.addWidget(clear_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def clear_history(self):
        self.history_list.clear()
        self.parent().history.clear()


class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('calculator.ui', self)

        # Initialize variables
        self.current_input = ''
        self.result = 0
        self.pending_operation = None
        self.last_button_was_operator = False
        self.history = []  # List to store calculation history

        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QLabel {
                color: #666;
                font-size: 14px;
            }
        """)

        # Connect buttons
        self.connect_number_buttons()
        self.connect_operator_buttons()
        self.connect_scientific_buttons()
        self.connect_other_buttons()

        # Show the calculator
        self.show()

    def connect_number_buttons(self):
        """Connect number buttons (0-9) and decimal point"""
        for i in range(10):
            button = getattr(self, f'button{i}')
            button.clicked.connect(lambda x, n=i: self.number_pressed(str(n)))

        self.buttonDot.clicked.connect(lambda: self.number_pressed('.'))

    def connect_operator_buttons(self):
        """Connect basic arithmetic operator buttons"""
        self.buttonPlus.clicked.connect(lambda: self.operator_pressed('+'))
        self.buttonMinus.clicked.connect(lambda: self.operator_pressed('-'))
        self.buttonMultiply.clicked.connect(lambda: self.operator_pressed('×'))
        self.buttonDivide.clicked.connect(lambda: self.operator_pressed('÷'))
        self.buttonEqual.clicked.connect(self.calculate_result)

    def connect_scientific_buttons(self):
        """Connect scientific function buttons"""
        self.buttonSin.clicked.connect(lambda: self.scientific_operation('sin'))
        self.buttonCos.clicked.connect(lambda: self.scientific_operation('cos'))
        self.buttonTan.clicked.connect(lambda: self.scientific_operation('tan'))
        self.buttonLog.clicked.connect(lambda: self.scientific_operation('log'))
        self.buttonLn.clicked.connect(lambda: self.scientific_operation('ln'))
        self.buttonExp.clicked.connect(lambda: self.scientific_operation('exp'))
        self.buttonPower.clicked.connect(lambda: self.operator_pressed('^'))
        self.buttonSquare.clicked.connect(lambda: self.scientific_operation('square'))
        self.buttonSqrt.clicked.connect(lambda: self.scientific_operation('sqrt'))
        self.buttonFactorial.clicked.connect(lambda: self.scientific_operation('factorial'))
        self.buttonPi.clicked.connect(lambda: self.constant_pressed('π'))
        self.buttonE.clicked.connect(lambda: self.constant_pressed('e'))

    def connect_other_buttons(self):
        """Connect utility buttons"""
        self.buttonClear.clicked.connect(self.clear_all)
        self.buttonBackspace.clicked.connect(self.backspace)
        self.buttonHistory.clicked.connect(self.show_history)

    def add_to_history(self, expression, result):
        """Add calculation to history"""
        history_entry = f"{expression} = {result}"
        self.history.append(history_entry)
        # Keep only the last 20 calculations
        if len(self.history) > 20:
            self.history.pop(0)

    def number_pressed(self, number):
        """Handle number button presses"""
        if self.last_button_was_operator:
            self.current_input = ''
            self.last_button_was_operator = False

        if number == '.' and '.' in self.current_input:
            return

        self.current_input += number
        self.display.setText(self.current_input)

    def operator_pressed(self, operator):
        """Handle operator button presses"""
        if self.current_input:
            if self.pending_operation:
                self.calculate_result()

            self.result = float(self.current_input)
            self.pending_operation = operator
            self.processLabel.setText(f"{self.current_input} {operator}")
            self.last_button_was_operator = True

    def calculate_result(self):
        """Calculate and display result"""
        if not self.pending_operation or not self.current_input:
            return

        current_value = float(self.current_input)
        expression = f"{self.result} {self.pending_operation} {current_value}"

        try:
            if self.pending_operation == '+':
                self.result += current_value
            elif self.pending_operation == '-':
                self.result -= current_value
            elif self.pending_operation == '×':
                self.result *= current_value
            elif self.pending_operation == '÷':
                if current_value == 0:
                    raise ZeroDivisionError
                self.result /= current_value
            elif self.pending_operation == '^':
                self.result = pow(self.result, current_value)

            # Add to history
            self.add_to_history(expression, self.result)

            self.processLabel.setText(f"{expression} =")
            self.display.setText(str(self.result))
            self.current_input = str(self.result)
            self.pending_operation = None

        except ZeroDivisionError:
            self.display.setText('Error: Division by zero')
        except Exception as e:
            self.display.setText('Error')

    def scientific_operation(self, operation):
        """Handle scientific operations"""
        try:
            if self.current_input:
                value = float(self.current_input)
                expression = f"{operation}({value})"

                if operation == 'sin':
                    result = math.sin(math.radians(value))
                elif operation == 'cos':
                    result = math.cos(math.radians(value))
                elif operation == 'tan':
                    result = math.tan(math.radians(value))
                elif operation == 'log':
                    result = math.log10(value)
                elif operation == 'ln':
                    result = math.log(value)
                elif operation == 'exp':
                    result = math.exp(value)
                elif operation == 'square':
                    result = value ** 2
                    expression = f"({value})²"
                elif operation == 'sqrt':
                    result = math.sqrt(value)
                    expression = f"√({value})"
                elif operation == 'factorial':
                    result = math.factorial(int(value))
                    expression = f"{value}!"

                # Add to history
                self.add_to_history(expression, result)

                self.processLabel.setText(f"{expression} =")
                self.display.setText(str(result))
                self.current_input = str(result)
                self.result = result
        except Exception as e:
            self.display.setText('Error')

    def constant_pressed(self, constant):
        """Handle mathematical constants"""
        if constant == 'π':
            self.current_input = str(math.pi)
        elif constant == 'e':
            self.current_input = str(math.e)

        self.display.setText(self.current_input)

    def clear_all(self):
        """Clears all input and resets calculator"""
        self.display.clear()
        self.processLabel.clear()
        self.current_input = ''
        self.result = 0
        self.pending_operation = None

    def clear_entry(self):
        """Clears only the current entry"""
        self.display.clear()
        self.current_input = ''

    def backspace(self):
        """Removes the last character from the display"""
        current = self.display.text()
        self.display.setText(current[:-1])
        self.current_input = current[:-1]

    def show_history(self):
        """Shows calculation history in a custom dialog"""
        dialog = HistoryDialog(self.history, self)
        dialog.exec_()


def main():
    app = QApplication(sys.argv)
    calculator = ScientificCalculator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()