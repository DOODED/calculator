import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QLineEdit, QTextEdit, QVBoxLayout, QLabel)
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculation History')
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        self.history_label = QLabel('Calculation History:')
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)

        layout.addWidget(self.history_label)
        layout.addWidget(self.history_text)

        self.setLayout(layout)

    def update_history(self, history_list):
        self.history_text.clear()
        for item in history_list:
            self.history_text.append(item)


class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI file
        uic.loadUi('calculator.ui', self)

        # Initialize variables
        self.current_number = ''
        self.result = 0
        self.operation = ''
        self.new_number = True
        self.history = []
        self.is_dark_theme = False

        # Create history window
        self.history_window = HistoryWindow()

        # Initialize display
        self.display.setText('0')
        self.processLabel.setText('')

        # Connect number buttons
        for i in range(10):
            button = getattr(self, f'button{i}')
            button.clicked.connect(lambda x, n=i: self.number_pressed(n))

        # Connect operation buttons
        self.buttonPlus.clicked.connect(lambda: self.operation_pressed('+'))
        self.buttonMinus.clicked.connect(lambda: self.operation_pressed('-'))
        self.buttonMultiply.clicked.connect(lambda: self.operation_pressed('×'))
        self.buttonDivide.clicked.connect(lambda: self.operation_pressed('÷'))

        # Connect special buttons
        self.buttonEqual.clicked.connect(self.calculate_result)
        self.buttonClear.clicked.connect(self.clear)
        self.buttonDot.clicked.connect(self.decimal_pressed)
        self.buttonBackspace.clicked.connect(self.backspace)

        # Connect scientific calculator buttons
        self.buttonSin.clicked.connect(lambda: self.scientific_operation('sin'))
        self.buttonCos.clicked.connect(lambda: self.scientific_operation('cos'))
        self.buttonTan.clicked.connect(lambda: self.scientific_operation('tan'))
        self.buttonLog.clicked.connect(lambda: self.scientific_operation('log'))
        self.buttonLn.clicked.connect(lambda: self.scientific_operation('ln'))
        self.buttonSquare.clicked.connect(lambda: self.scientific_operation('square'))
        self.buttonSqrt.clicked.connect(lambda: self.scientific_operation('sqrt'))
        self.buttonFactorial.clicked.connect(lambda: self.scientific_operation('factorial'))
        self.buttonPi.clicked.connect(lambda: self.constant_pressed('π'))
        self.buttonE.clicked.connect(lambda: self.constant_pressed('e'))
        self.buttonExp.clicked.connect(lambda: self.operation_pressed('exp'))
        self.buttonPower.clicked.connect(lambda: self.operation_pressed('^'))

        # Connect theme button
        self.buttonTheme.clicked.connect(self.toggle_theme)

        # Connect history button
        self.buttonHistory.clicked.connect(self.toggle_history)

    def toggle_history(self):
        if self.history_window.isVisible():
            self.history_window.hide()
        else:
            self.history_window.show()
            self.history_window.update_history(self.history)

    def number_pressed(self, number):
        if self.new_number:
            self.display.clear()
            self.new_number = False

        current = self.display.text()
        new_number = current + str(number)
        self.display.setText(new_number)

    def operation_pressed(self, op):
        self.result = float(self.display.text().replace('π', str(math.pi)).replace('e', str(math.e)))
        self.operation = op
        self.new_number = True
        self.processLabel.setText(f'{self.result} {op}')

    def calculate_result(self):
        if not self.operation:
            return

        second_number = float(self.display.text().replace('π', str(math.pi)).replace('e', str(math.e)))
        expression = f'{self.result} {self.operation} {second_number}'

        try:
            if self.operation == '+':
                result = self.result + second_number
            elif self.operation == '-':
                result = self.result - second_number
            elif self.operation == '×':
                result = self.result * second_number
            elif self.operation == '÷':
                if second_number == 0:
                    raise ZeroDivisionError
                result = self.result / second_number
            elif self.operation == '^':
                result = self.result ** second_number
            elif self.operation == 'exp':
                result = self.result * (10 ** second_number)

            # Add to history and update history window
            history_entry = f'{expression} = {result}'
            self.history.append(history_entry)
            if self.history_window.isVisible():
                self.history_window.update_history(self.history)

            self.display.setText(str(result))
            self.processLabel.setText('')
            self.operation = ''
            self.new_number = True

        except ZeroDivisionError:
            self.display.setText('Error: Division by zero')
            self.new_number = True
        except Exception as e:
            self.display.setText('Error')
            self.new_number = True

    def scientific_operation(self, operation):
        try:
            number = float(self.display.text().replace('π', str(math.pi)).replace('e', str(math.e)))
            expression = f'{operation}({number})'

            if operation == 'sin':
                result = math.sin(number)
            elif operation == 'cos':
                result = math.cos(number)
            elif operation == 'tan':
                result = math.tan(number)
            elif operation == 'log':
                result = math.log10(number)
            elif operation == 'ln':
                result = math.log(number)
            elif operation == 'square':
                result = number ** 2
                expression = f'{number}²'
            elif operation == 'sqrt':
                result = math.sqrt(number)
                expression = f'√{number}'
            elif operation == 'factorial':
                result = math.factorial(int(number))
                expression = f'{number}!'

            # Add to history and update history window
            history_entry = f'{expression} = {result}'
            self.history.append(history_entry)
            if self.history_window.isVisible():
                self.history_window.update_history(self.history)

            self.display.setText(str(result))
            self.new_number = True

        except Exception as e:
            self.display.setText('Error')
            self.new_number = True

    def constant_pressed(self, constant):
        if constant == 'π':
            self.display.setText('π')
        elif constant == 'e':
            self.display.setText('e')
        self.new_number = False

    def decimal_pressed(self):
        if '.' not in self.display.text():
            self.display.setText(self.display.text() + '.')

    def clear(self):
        self.display.setText('0')
        self.processLabel.setText('')
        self.result = 0
        self.operation = ''
        self.new_number = True

    def backspace(self):
        current = self.display.text()
        if len(current) > 1:
            self.display.setText(current[:-1])
        else:
            self.display.setText('0')
            self.new_number = True

    def toggle_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: white;
                }
                QPushButton {
                    background-color: #f0f0f0;
                    color: black;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
            """)
            self.history_window.setStyleSheet("""
                QWidget {
                    background-color: white;
                    color: black;
                }
                QTextEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #ccc;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #333;
                }
                QPushButton {
                    background-color: #444;
                    color: white;
                    border: 1px solid #555;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
                QLineEdit {
                    background-color: #444;
                    color: white;
                    border: 1px solid #555;
                    border-radius: 5px;
                }
                QLabel {
                    color: white;
                }
            """)
            self.history_window.setStyleSheet("""
                QWidget {
                    background-color: #333;
                    color: white;
                }
                QTextEdit {
                    background-color: #444;
                    color: white;
                    border: 1px solid #555;
                }
            """)
        self.is_dark_theme = not self.is_dark_theme


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = ScientificCalculator()
    calculator.show()
    sys.exit(app.exec_())