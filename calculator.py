import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton
from datetime import datetime


class HistoryWindow(QDialog):
    def __init__(self, history):
        super().__init__()
        self.setWindowTitle("Calculation History")
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        # Create text edit for history
        self.historyText = QTextEdit()
        self.historyText.setReadOnly(True)
        self.historyText.setText(history)
        layout.addWidget(self.historyText)

        # Create close button
        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton)

        self.setLayout(layout)


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
        self.new_calculation = True
        self.history = []

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
        self.buttonMultiply.clicked.connect(lambda: self.operator_pressed('×'))
        self.buttonDivide.clicked.connect(lambda: self.operator_pressed('÷'))

        # Connect other buttons
        self.buttonEqual.clicked.connect(self.calculate_result)
        self.buttonClear.clicked.connect(self.clear_all)
        self.buttonDot.clicked.connect(self.decimal_pressed)
        self.buttonBackspace.clicked.connect(self.backspace_pressed)
        self.buttonHistory.clicked.connect(self.show_history)

        # Initialize displays
        self.display.setText('0')
        self.processLabel.setText('')

    def number_pressed(self, number):
        if self.new_calculation:
            self.current_number = ''
            self.new_calculation = False

        self.current_number += number
        self.display.setText(self.current_number)

    def operator_pressed(self, op):
        if self.current_number:
            if self.first_number is None:
                self.first_number = float(self.current_number)
                self.operator = op
                self.processLabel.setText(f"{self.current_number} {op}")
                self.current_number = ''
            else:
                self.calculate_result()
                self.operator = op
                self.processLabel.setText(f"{self.first_number} {op}")
        elif self.first_number is not None:
            self.operator = op
            self.processLabel.setText(f"{self.first_number} {op}")

    def calculate_result(self):
        if self.first_number is not None and self.current_number and self.operator:
            second_number = float(self.current_number)
            expression = f"{self.first_number} {self.operator} {second_number} ="

            try:
                if self.operator == '+':
                    self.result = self.first_number + second_number
                elif self.operator == '-':
                    self.result = self.first_number - second_number
                elif self.operator == '×':
                    self.result = self.first_number * second_number
                elif self.operator == '÷':
                    if second_number == 0:
                        raise ZeroDivisionError
                    self.result = self.first_number / second_number

                # Display result
                if isinstance(self.result, float) and self.result.is_integer():
                    result_str = str(int(self.result))
                else:
                    result_str = f"{self.result:.8f}".rstrip('0').rstrip('.')

                self.processLabel.setText(expression)
                self.display.setText(result_str)

                # Add to history
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history_entry = f"[{timestamp}] {expression} {result_str}"
                self.history.append(history_entry)

                # Store result as first number for continued calculations
                self.first_number = float(result_str)
                self.current_number = ''
                self.new_calculation = True

            except ZeroDivisionError:
                self.display.setText('Error: Division by zero')
                self.clear_all()
            except Exception as e:
                self.display.setText('Error')
                self.clear_all()

    def decimal_pressed(self):
        if self.new_calculation:
            self.current_number = '0'
            self.new_calculation = False

        if '.' not in self.current_number:
            if self.current_number == '':
                self.current_number = '0'
            self.current_number += '.'
            self.display.setText(self.current_number)

    def backspace_pressed(self):
        if not self.new_calculation:
            self.current_number = self.current_number[:-1]
            self.display.setText(self.current_number if self.current_number else '0')

    def clear_all(self):
        self.current_number = ''
        self.first_number = None
        self.operator = None
        self.result = None
        self.new_calculation = True
        self.display.setText('0')
        self.processLabel.setText('')

    def show_history(self):
        history_text = '\n'.join(self.history) if self.history else "No calculation history"
        history_window = HistoryWindow(history_text)
        history_window.exec_()


def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()