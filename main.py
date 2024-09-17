from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets


class myWin(QtWidgets.QMainWindow, Ui_MainWindow):

    siganl_resetscrollbar = pyqtSignal() #滑动条位置保持在最上面
    def __init__(self):
        super(myWin, self).__init__()
        self.setupUi(self)

        self.InitPaintBoard()

        self.setWindowTitle("画图板")  # 设置窗口名
        self.largestNumber = 0

        self.siganl_resetscrollbar.connect(self.on_signal_resetscrollbar)  #滑动条位置保持在最上面

    #滑动条位置保持在最上面
    def on_signal_resetscrollbar(self):
        self.scroll_area.verticalScrollBar().setValue(0)

    # 背景图平铺
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("background/background5.jpeg")
        painter.drawPixmap(self.rect(), pixmap)
    # 背景图平铺结束

    def InitPaintBoard(self):
        self.__paintBoard = PaintBoard(self)
        paintboardlayout = QtWidgets.QVBoxLayout(self)
        self.groupBox.setLayout(paintboardlayout)
        #paintboardlayout.addWidget(self.__paintBoard)



        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.__paintBoard)
        self.scroll_area.setMinimumWidth(500)
        #不要允许WIDGE自适应，第2给PAINTBOARD一个默认的大小就可以让他出现滚动条和滑快
        #self.scroll_area.setWidgetResizable(True) # 允许 widget 自适应内容大小
        #self.__paintBoard.setGeometry(0,0,1000,1000)
        self.__paintBoard.setGeometry(0, 0, paintBoardWidth, paintBoardHeight)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
 

        paintboardlayout.addWidget(self.scroll_area)
      

        #将按钮选择的新的画板尺寸传递到painboard.py
        self.__paintBoard.paintBoardSizeT(paintBoardWidth,paintBoardHeight)

        #新加显示颜色下拉的代码
        #获取颜色列表(字符串类型)
        self.__colorList = QColor.colorNames()
        self.__fillColorList(self.comboBox)

        #新加定义画笔粗线的代码
        self.spinBox.setMaximum(20)
        self.spinBox.setMinimum(1)
        self.spinBox.setValue(10) #默认粗细为10
        self.spinBox.setSingleStep(1) #最小变化值为2



        self.__paintBoard.change_pen_thickness(10)
        self.__paintBoard.change_pen_color(Qt.black)

        self.pushButton.clicked.connect(self.clear_paintboard)  #正确
        self.comboBox.currentIndexChanged.connect(self.change_pen_color)
        self.spinBox.valueChanged.connect(self.on_PenThicknessChange)


        #绑定橡皮，粗细，颜色选择信号
        self.checkBox.clicked.connect(self.on_cbtn_Eraser_clicked)
        # self.spinBox.valueChanged.connect(self.on_PenThicknessChange)#关联spinBox值变化信号和函数on_PenThicknessChange
        self.comboBox.currentIndexChanged.connect(self.on_PenColorChange) #关联下拉列表的当前索引变更信号与函数on_PenColorChange

        #将按键按下信号与画板清空函数相关联
        self.pushButton.clicked.connect(self.clear_paintboard)
        self.pushButton_2.clicked.connect(self.Quit)
        self.pushButton_3.clicked.connect(self.on_btn_Save_Clicked)
        self.pushButton_4.clicked.connect(self.on_btn_undoLastLine_Clicked)
        self.pushButton_5.clicked.connect(self.on_btn_redoLastLine_Clicked)

        self.pushButton_6.clicked.connect(self.paintBoardChange)
        self.pushButton_7.clicked.connect(self.paintBoardChangeH)

        #self.pushButton.hide()
        self.pushButton_5.hide()


    def paintBoardChange(self):
        comboBoxTEXT=self.comboBox_2.currentText()
        print("TEXT",comboBoxTEXT)

        global paintBoardHeight
        global paintBoardWidth

        if comboBoxTEXT=="1000x1000":
            paintBoardHeight=1000
            paintBoardWidth=1000
        if comboBoxTEXT=="A5_148x241":
            paintBoardHeight=241
            paintBoardWidth=148
        if comboBoxTEXT=="A4_210x297":
            paintBoardHeight=297
            paintBoardWidth=210
        if comboBoxTEXT=="A3_297x420":
            paintBoardHeight=420
            paintBoardWidth=297
        if comboBoxTEXT=="A2_420x594":
            paintBoardHeight=594
            paintBoardWidth=420
        if comboBoxTEXT=="A1_594x841":
            paintBoardHeight=841
            paintBoardWidth=594

        print("paintBoardHeight-button", paintBoardHeight)
        print("paintBoardWidth-button", paintBoardWidth)

        self.__paintBoard.setGeometry(0, 0, paintBoardWidth, paintBoardHeight)

        #将按钮选择的新的画板尺寸传递到painboard.py
        self.__paintBoard.paintBoardSizeT(paintBoardWidth,paintBoardHeight)


        #初始化画板
        self.clear_paintboard()


    def clear_paintboard(self):
        self.__paintBoard.clear()

    def change_pen_color(self):
        color_index = self.comboBox.currentIndex()
        color_str = self.comboBox.itemText(color_index)
        self.__paintBoard.change_pen_color(color_str)




    #橡皮选不选中的绑定函数
    def on_cbtn_Eraser_clicked(self):
        print("on_cbtn_Eraser_clicked")
        if self.checkBox.isChecked():
            self.__paintBoard.change_eraser_mode = True #进入橡皮擦模式
        else:
            self.__paintBoard.change_eraser_mode = False #退出橡皮擦模式

    #撤销上一条线
    def on_btn_undoLastLine_Clicked(self):
        print("on_btn_undoLastLine_Clicked")
        #self.undoLastLine()
        try:
            self.__paintBoard.undoLastLine()

        except Exception as e:
            print(f"An error occurred: {e}")


        # 删除最后一行文本
        with open("coordinates.txt", "r") as file:
            lines = file.readlines()
        if lines:
            lines = lines[:-1]  # 删除最后一行
            with open("coordinates.txt", "w") as file:
                file.writelines(lines)


    #恢复上一条线
    def on_btn_redoLastLine_Clicked(self):
        print("on_btn_redoLastLine_Clicked")
        try:
            self.__paintBoard.redoLastLine()
        except Exception as e:
            print(f"An error occurred: {e}")

    def __fillColorList(self, comboBox):

        index_black = 0
        index = 0
        for color in self.__colorList:
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70,20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix),None)
            comboBox.setIconSize(QSize(70,20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        comboBox.setCurrentIndex(index_black)

    #颜色选择的函数
    def on_PenColorChange(self):
        color_index = self.comboBox.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.change_pen_color(color_str)

    #画笔粗细改变的函数
    def on_PenThicknessChange(self):
        penThickness = self.spinBox.value()
        self.__paintBoard.change_pen_thickness(penThickness)


    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        # image = self.__paintBoard.GetContentAsQImage()
        # image.save(savePath[0])
        # print(savePath[0])

        img = self.groupBox.grab()
        img.save(savePath[0])

    def Quit(self):
        self.close()


    def on_login(self):
        print("test")



if __name__=="__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app=QtWidgets.QApplication(sys.argv)
    Widget=myWin()
    Widget.showMaximized();
    sys.exit(app.exec_())
