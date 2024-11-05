import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        uic.loadUi('calculator.ui', self)
        
        # Initialize variables
        self.current_number = ''
        self.first_number = None
        self.operator = None
        self.result = None
        
        # Connect number buttons
        self.button0.clicked.connect(lambda: self.number_pressed('0'))
        self.button1.clicked.connect(lambda: self.number_pressed('1'))
        self.button2.clicked.connect(lambda: self.number_pressed('2'))
        self.button3.clicked.connect(lambda: self.number_pressed('3'))
        self.button4.clicked.connect(lambda: self.number_pressed('4'))
        self.button5.clicked.connect(lambda: self.number_pressed('5'))
        self.button6.clicked.connect(lambda: self.number_pressed('6'))
        self.button7.clicked.connect(lambda: self.number_pressed('7'))
        self.button8.clicked.connect(lambda: self.number_pressed('8'))
        self.button9.clicked.connect(lambda: self.number_pressed('9'))
        
        # Connect operator buttons
        self.buttonPlus.clicked.connect(lambda: self.operator_pressed('+'))
        self.buttonMinus.clicked.connect(lambda: self.operator_pressed('-'))
        self.buttonMultiply.clicked.connect(lambda: self.operator_pressed('*'))
        self.buttonDivide.clicked.connect(lambda: self.operator_pressed('/'))
        
        # Connect other buttons
        self.buttonEqual.clicked.connect(self.calculate_result)
        self.buttonClear.clicked.connect(self.clear_all)
        self.buttonDot.clicked.connect(self.decimal_pressed)
        self.buttonBackspace.clicked.connect(self.backspace_pressed)

    def number_pressed(self, number):
        self.current_number += number
        self.display.setText(self.current_number)

    def operator_pressed(self, op):
        if self.current_number:
            if self.first_number is None:
                self.first_number = float(self.current_number)
                self.operator = op
                self.current_number = ''
            else:
                self.calculate_result()
                self.operator = op

    def calculate_result(self):
        if self.first_number is not None and self.current_number and self.operator:
            second_number = float(self.current_number)
            
            if self.operator == '+':
                self.result = self.first_number + second_number
            elif self.operator == '-':
                self.result = self.first_number - second_number
            elif self.operator == '*':
                self.result = self.first_number * second_number
            elif self.operator == '/' and second_number != 0:
                self.result = self.first_number / second_number
            else:
                self.display.setText('Error')
                return

            # Display result
            if self.result.is_integer():
                self.display.setText(str(int(self.result)))
            else:
                self.display.setText(str(self.result))

            # Store result as first number for continued calculations
            self.first_number = self.result
            self.current_number = ''

    def decimal_pressed(self):
        if '.' not in self.current_number:
            if self.current_number == '':
                self.current_number = '0'
            self.current_number += '.'
            self.display.setText(self.current_number)

    def backspace_pressed(self):
        self.current_number = self.current_number[:-1]
        self.display.setText(self.current_number if self.current_number else '0')

    def clear_all(self):
        self.current_number = ''
        self.first_number = None
        self.operator = None
        self.result = None
        self.display.setText('0')

def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()