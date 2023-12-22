import sys
import math
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cache = "" # 이항연산을 위함이다

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_operation = QHBoxLayout()
        layout_clear_equal = QHBoxLayout()
        layout_number = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation = QLabel()
        self.equation = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(label_equation, self.equation)

        ### 사칙연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_number.addWidget(button_plus,5,4)
        layout_number.addWidget(button_minus,4,4)
        layout_number.addWidget(button_product,3,4)
        layout_number.addWidget(button_division,2,4)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_C = QPushButton("C")
        button_CE = QPushButton("CE")
        button_backspace = QPushButton("Backspace")


        ### =, C, CE, backspace 버튼을 레이아웃에 추가
        layout_number.addWidget(button_equal, 6, 4)
        layout_number.addWidget(button_CE, 1, 2)
        layout_number.addWidget(button_C, 1, 3)
        layout_number.addWidget(button_backspace, 1, 4)

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_C.clicked.connect(self.button_clear_clicked)
        button_CE.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### %, 1/x, x^2, x^0.5, +/-, . 버튼 생성
        button_mod = QPushButton("%")
        button_flip = QPushButton("1/x")
        button_pow = QPushButton("x^2")
        button_sqrt = QPushButton("x^0.5")
        button_reverse = QPushButton("+/-")
        button_decimal = QPushButton(".")

        ### 버튼 추가
        layout_number.addWidget(button_mod, 1, 1)
        layout_number.addWidget(button_flip, 2, 1)
        layout_number.addWidget(button_pow, 2, 2)
        layout_number.addWidget(button_sqrt, 2, 3)
        layout_number.addWidget(button_reverse, 6, 1)
        layout_number.addWidget(button_decimal, 6, 3)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ##### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number > 0:
                x,y = divmod(number-1, 3)
                layout_number.addWidget(number_button_dict[number], 5-x, y + 1)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 6, 2)


        

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_operation)
        main_layout.addLayout(layout_clear_equal)
        main_layout.addLayout(layout_number)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        # 캐시가 비어 있으면 캐시로 넣는다.
        if self.cache == "":
            self.cache = equation + operation
            self.equation.setText("")
            return
        # 입력값이 없다면, 연산만 바꾼다.
        if equation == "":
            self.cache = self.cache[:-1] + operation
            return
        # 입력값이 있으면, 계산 후 캐시에 다시 저장한다.
        value = eval(self.cache + equation)
        self.cache = str(value) + operation
        self.equation.setText("")

    def button_equal_clicked(self):
        equation = self.equation.text()
        solution = eval(equation)
        self.solution.setText(str(solution))

    def button_clear_clicked(self):
        self.equation.setText("")
        self.solution.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

    ### 단항연산자
    def unary_operation(self, fn):
        equation = self.equation.text()
        if equation == "":
            return
        n = 0
        if self.cache != "":
            n = eval(self.cache + equation)
        else:
            n = float(equation)
        self.equation.setText(str(fn(n)))

    def button_flip_clicked(self):
        self.unary_operation(lambda x: 1/x)

    def button_pow_clicked(self):
        self.unary_operation(lambda x: x*x)

    def button_sqrt_clicked(self):
        self.unary_operation(lambda x: math.sqrt(x))

    def button_reverse_clicked(self):
        self.unary_operation(lambda x: -x)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())