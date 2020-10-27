import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTableWidgetItem
from PyQt5.QtWidgets import QLCDNumber, QLineEdit, QLabel
from Settings import Ui_MainWindow
import csv
import sqlite3
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
#Если Вы читаете этот комментарий, я вас предупредаю, не смотрите дальше(ну или хотябы удостоверьтесь, что у вас нет сердечно-сосудистых заболеваний)


con = sqlite3.connect("com.db")   #Тут как всегда создаём БД
cur = con.cursor()
result = cur.execute("""CREATE TABLE IF NOT EXISTS commands (Word str, Answer str);""").fetchall()
con.commit()
con.close()


d = 0   #И тут вроде ничего сложного, просто какая-то переменная
p = []  #А вот в этом месте и далее мы обновляем переменную "p"
with open('commands.csv') as csvfile:
    typer = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, row in enumerate(typer):
        p.append(row)

#Простенькая функция для записи в csv файл
def csv_writer(data, path):
    with open(path, "w", newline='\n') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)          #Вчера я играл в дотку и понял, что от ЯЛ горит не сильнее всего

#Конечно, куда же без классов
class MyWidget1(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI('commands.csv')
    
    def initUI(self, table_name):       #Основная функция в классе, она заполняет таблицу и следит за нажатиями кнопок
        with open('commands.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            title = next(reader)
            self.List_of_commands.setColumnCount(len(title))
            self.List_of_commands.setHorizontalHeaderLabels(title)
            self.List_of_commands.setRowCount(0)
            for i, row in enumerate(reader):
                self.List_of_commands.setRowCount(self.List_of_commands.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.List_of_commands.setItem(i, j, QTableWidgetItem(elem))
        self.List_of_commands.resizeColumnsToContents()
        self.Adding.clicked.connect(self.add_function)
        self.starting.clicked.connect(self.pre_and_start)
        self.delete.clicked.connect(self.dele)
        self.stopping.clicked.connect(self.stp)

    def add_function(self):       #Бот без функций - это скушно, почему бы нам не добавить парочку???
        global p
        word = self.lineEdit_3.text()
        self.lineEdit_3.setText('')
        answ = self.plainTextEdit.toPlainText()
        self.plainTextEdit.setPlainText('')
        if (str(word) != '') or (str(answ) != ''):
            p = p + [[str(word), str(answ)]]
            csv_writer(p, 'commands.csv')
            self.initUI('commands.csv')
            
    def pre_and_start(self):       #Тут пользвателя ждёт небольшое путешествие по файлу с программой(увидите после нажатия кнопки "Start")
        global d
        if d == 0:
            con = sqlite3.connect("com.db")
            cur = con.cursor()
            i = []
            with open('commands.csv') as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for index, row in enumerate(reader):
                    if index > 0:
                        i.append(row)
            for q in i:
                cur.execute('INSERT INTO commands VALUES(?, ?)', (q[0], q[1]))
            con.commit()
            con.close()
            self.plainTextEdit.setPlainText('''#################################
Go to program named "Start.py" and run it to continue
#################################''')    #Лоооооол, спойлеры подкатили(НЕ СМОТРИТЕ)
            d += 1


    def dele(self):     #И если у Вас кое-что подгорело, то я сделал кнопку что-бы Вы могли нафиг всё удалить
        csv_writer([['Word', 'Answer']], 'commands.csv')
        self.initUI('commands.csv')
        con = sqlite3.connect("com.db")
        cur = con.cursor()
        cur.execute("""DROP TABLE commands""")
        con.commit()
        con.close()


    def stp(self):   #А куда же без принудительной остановки программы?
        ex1.hide()
        sys.exit()
    
    
app = QApplication(sys.argv)    #Ну а это я просто скопипастил из ЯЛ
ex1 = MyWidget1()
ex1.show()
sys.exit(app.exec_())