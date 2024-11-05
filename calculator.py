import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5 import uic
import math


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

        if self.pending_operation == '+':
            self.result += current_value
        elif self.pending_operation == '-':
            self.result -= current_value
        elif self.pending_operation == '×':
            self.result *= current_value
        elif self.pending_operation == '÷':
            if current_value == 0:
                self.display.setText('Error')
                return
            self.result /= current_value
        elif self.pending_operation == '^':
            self.result = pow(self.result, current_value)

        self.processLabel.setText(f"{self.result} {self.pending_operation} {current_value} =")
        self.display.setText(str(self.result))
        self.current_input = str(self.result)
        self.pending_operation = None

    def scientific_operation(self, operation):
        """Handle scientific operations"""
        try:
            if self.current_input:
                value = float(self.current_input)

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
                elif operation == 'sqrt':
                    result = math.sqrt(value)
                elif operation == 'factorial':
                    result = math.factorial(int(value))

                self.processLabel.setText(f"{operation}({value}) =")
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
        """Shows calculation history"""
        # Implement history functionality here
        pass


def main():
    app = QApplication(sys.argv)
    calculator = ScientificCalculator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()