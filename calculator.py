import sys
import math
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton
from datetime import datetime


class HistoryWindow(QDialog):
    def __init__(self, history):
        super().__init__()
        self.setWindowTitle("Calculation History")
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        self.historyText = QTextEdit()
        self.historyText.setReadOnly(True)
        self.historyText.setText(history)
        layout.addWidget(self.historyText)

        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton)

        self.setLayout(layout)


class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calculator.ui', self)

        # Initialize variables
        self.current_number = ''
        self.first_number = None
        self.operator = None
        self.result = None
        self.new_calculation = True
        self.history = []

        # Connect number buttons
        self.connect_number_buttons()

        # Connect operator buttons
        self.connect_operator_buttons()

        # Connect scientific function buttons
        self.connect_scientific_buttons()

        # Connect other buttons
        self.connect_other_buttons()

        # Initialize displays
        self.display.setText('0')
        self.processLabel.setText('')

    def connect_number_buttons(self):
        for i in range(10):
            button = getattr(self, f'button{i}')
            button.clicked.connect(lambda x, n=i: self.number_pressed(str(n)))

    def connect_operator_buttons(self):
        self.buttonPlus.clicked.connect(lambda: self.operator_pressed('+'))
        self.buttonMinus.clicked.connect(lambda: self.operator_pressed('-'))
        self.buttonMultiply.clicked.connect(lambda: self.operator_pressed('×'))
        self.buttonDivide.clicked.connect(lambda: self.operator_pressed('÷'))

    def connect_scientific_buttons(self):
        # Trigonometric functions
        self.buttonSin.clicked.connect(lambda: self.scientific_operation('sin'))
        self.buttonCos.clicked.connect(lambda: self.scientific_operation('cos'))
        self.buttonTan.clicked.connect(lambda: self.scientific_operation('tan'))

        # Logarithmic functions
        self.buttonLog.clicked.connect(lambda: self.scientific_operation('log'))
        self.buttonLn.clicked.connect(lambda: self.scientific_operation('ln'))

        # Power functions
        self.buttonPower.clicked.connect(lambda: self.operator_pressed('^'))
        self.buttonSquare.clicked.connect(lambda: self.scientific_operation('square'))
        self.buttonSqrt.clicked.connect(lambda: self.scientific_operation('sqrt'))

        # Constants
        self.buttonPi.clicked.connect(lambda: self.constant_pressed('π'))
        self.buttonE.clicked.connect(lambda: self.constant_pressed('e'))

        # Other functions
        self.buttonExp.clicked.connect(lambda: self.scientific_operation('exp'))
        self.buttonFactorial.clicked.connect(lambda: self.scientific_operation('factorial'))

    def connect_other_buttons(self):
        self.buttonEqual.clicked.connect(self.calculate_result)
        self.buttonClear.clicked.connect(self.clear_all)
        self.buttonDot.clicked.connect(self.decimal_pressed)
        self.buttonBackspace.clicked.connect(self.backspace_pressed)
        self.buttonHistory.clicked.connect(self.show_history)

    def constant_pressed(self, constant):
        if constant == 'π':
            self.current_number = str(math.pi)
        elif constant == 'e':
            self.current_number = str(math.e)
        self.display.setText(self.current_number)

    def scientific_operation(self, operation):
        try:
            if self.current_number:
                num = float(self.current_number)
                result = 0

                if operation == 'sin':
                    result = math.sin(math.radians(num))
                elif operation == 'cos':
                    result = math.cos(math.radians(num))
                elif operation == 'tan':
                    result = math.tan(math.radians(num))
                elif operation == 'log':
                    result = math.log10(num)
                elif operation == 'ln':
                    result = math.log(num)
                elif operation == 'square':
                    result = num ** 2
                elif operation == 'sqrt':
                    result = math.sqrt(num)
                elif operation == 'exp':
                    result = math.exp(num)
                elif operation == 'factorial':
                    result = math.factorial(int(num))

                # Format and display result
                result_str = self.format_result(result)
                self.display.setText(result_str)

                # Add to history
                history_entry = f"{operation}({self.current_number}) = {result_str}"
                self.add_to_history(history_entry)

                self.current_number = result_str
                self.new_calculation = True

        except Exception as e:
            self.display.setText('Error')
            self.clear_all()

    def format_result(self, result):
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            return f"{result:.8f}".rstrip('0').rstrip('.')
        return str(result)

    def add_to_history(self, entry):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{timestamp}] {entry}")

    def calculate_result(self):
        if self.first_number is not None and self.current_number and self.operator:
            try:
                num1 = float(self.first_number)
                num2 = float(self.current_number)

                if self.operator == '+':
                    result = num1 + num2
                elif self.operator == '-':
                    result = num1 - num2
                elif self.operator == '×':
                    result = num1 * num2
                elif self.operator == '÷':
                    if num2 == 0:
                        raise ZeroDivisionError
                    result = num1 / num2
                elif self.operator == '^':
                    result = num1 ** num2

                result_str = self.format_result(result)
                expression = f"{num1} {self.operator} {num2} = {result_str}"

                self.display.setText(result_str)
                self.processLabel.setText('')
                self.add_to_history(expression)

                self.first_number = result_str
                self.current_number = ''
                self.operator = None
                self.new_calculation = True

            except ZeroDivisionError:
                self.display.setText('Error: Division by zero')
                self.clear_all()
            except Exception as e:
                self.display.setText('Error')
                self.clear_all()

    # [Previous methods remain the same: number_pressed, operator_pressed,
    #  decimal_pressed, backspace_pressed, clear_all, show_history]


def main():
    app = QApplication(sys.argv)
    calculator = ScientificCalculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()