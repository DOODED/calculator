import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 파일 로드
        uic.loadUi('calculator.ui', self)

        # 초기 상태 설정
        self.current_number = ''
        self.result = 0
        self.operation = ''
        self.new_number = True
        self.history = []
        self.is_dark_theme = False

        # 디스플레이 초기화
        self.display.setText('0')
        self.processLabel.setText('')

        # 숫자 버튼 연결
        for i in range(10):
            button = getattr(self, f'button{i}')
            button.clicked.connect(lambda x, n=i: self.number_pressed(n))

        # 연산 버튼 연결
        self.buttonPlus.clicked.connect(lambda: self.operation_pressed('+'))
        self.buttonMinus.clicked.connect(lambda: self.operation_pressed('-'))
        self.buttonMultiply.clicked.connect(lambda: self.operation_pressed('×'))
        self.buttonDivide.clicked.connect(lambda: self.operation_pressed('÷'))

        # 특수 버튼 연결
        self.buttonEqual.clicked.connect(self.calculate_result)
        self.buttonClear.clicked.connect(self.clear)
        self.buttonDot.clicked.connect(self.decimal_pressed)
        self.buttonBackspace.clicked.connect(self.backspace)

        # 과학 계산기 버튼 연결
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

        # 테마 버튼 연결
        self.buttonTheme.clicked.connect(self.toggle_theme)

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

        if self.operation == '+':
            result = self.result + second_number
        elif self.operation == '-':
            result = self.result - second_number
        elif self.operation == '×':
            result = self.result * second_number
        elif self.operation == '÷':
            if second_number == 0:
                result = 'Error'
            else:
                result = self.result / second_number
        elif self.operation == '^':
            result = self.result ** second_number
        elif self.operation == 'exp':
            result = self.result * (10 ** second_number)

        self.display.setText(str(result))
        self.processLabel.setText('')
        self.operation = ''
        self.new_number = True
        self.history.append(f'{self.result} {self.operation} {second_number} = {result}')

    def scientific_operation(self, operation):
        try:
            number = float(self.display.text().replace('π', str(math.pi)).replace('e', str(math.e)))

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
            elif operation == 'sqrt':
                result = math.sqrt(number)
            elif operation == 'factorial':
                result = math.factorial(int(number))

            self.display.setText(str(result))
            self.new_number = True

        except Exception as e:
            self.display.setText('Error')

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
        self.is_dark_theme = not self.is_dark_theme


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = ScientificCalculator()
    calculator.show()
    sys.exit(app.exec_())