#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QTextEdit, QInputDialog
import json

#работа с тегами

def show_noutes():
    key = ListW.selectedItems()[0].text()
    TextW.setText(notes[key]['текст заметки'])
    ListW1.clear()
    ListW1.addItems(notes[key]['теги'])

def add_notes():
    note_name, ok = QInputDialog.getText(window, 'Добавить заметку','Название заметки:')

    if ok and note_name != '':
        notes[note_name] = {'текст заметки': '', 'теги': []}
        ListW.addItem(note_name)
        ListW1.addItems(notes[note_name]['теги'])
        with open('str.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def add_tag():
    if ListW.selectedItems():
        key = ListW.selectedItems()[0].text()
        tag = LineE.text()
        if not tag in notes[key]['теги']: 
            notes[key]['теги'].append(tag)
            ListW1.addItem(tag)
            LineE.clear()
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys= True, ensure_ascii = False)
    else:
        print('Заметка для добавления тега не выбрана!')


def search_tag():
    tag = LineE.text()
    if PushB5.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        PushB5.setText('Сбросить поиск')
        ListW.clear()
        ListW1.clear()
        ListW.addItems(notes_filtered)
    elif PushB5.text() == 'Сбросить поиск':
        LineE.clear()
        ListW.clear()
        ListW1.clear()
        ListW.addItems(notes)
        PushB5.setText('Искать заметку по тегу')
    else:
        pass

def save_note():
    if ListW.selectedItems():
        key = ListW.selectedItems()[0].text()
        notes[key]['текст заметки'] = TextW.toPlainText()
        with open('str.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def del_notes():
     if ListW.selectedItems():
        key = ListW.selectedItems()[0].text()   
        del notes[key]
        ListW.clear()
        ListW1.clear()
        TextW.clear()
        ListW.addItems(notes)
        with open('str.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def del_tag():
    if ListW.selectedItems():
        key = ListW.selectedItems()[0].text() 
        tag = ListW1.selectedItems()[0].text() 
        notes[key]['теги'].remove(tag)
        ListW1.clear()
        ListW1.addItems(notes[key]['теги'])
        with open('str.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)




#создание приложения
app = QApplication([]) 

#главное окошко 
window = QWidget()
window.setWindowTitle('Умные заметки')
window.resize(1000,600)

#создание виджетов
TextW = QTextEdit()
TextW.setFixedSize(600,550)
ListW = QListWidget()
PushB = QPushButton('Создать заметку')
PushB1 = QPushButton('Удалить заметку')
PushB2 = QPushButton('Сохранить заметку')
ListW1 = QListWidget()
LineE = QLineEdit()
PushB3 = QPushButton('Добавить к заметке')
PushB4 = QPushButton('Открепить от заметки')
PushB5 = QPushButton('Искать заметки по тегу')

l1 = QVBoxLayout()

l1.addWidget(ListW, alignment = Qt.AlignCenter)

l1.addWidget(PushB, alignment = Qt.AlignCenter)
l1.addWidget(PushB1, alignment = Qt.AlignCenter)
l1.addWidget(PushB2, alignment = Qt.AlignCenter)

l1.addWidget(ListW1, alignment = Qt.AlignCenter)
l1.addWidget(LineE, alignment = Qt.AlignCenter)

l1.addWidget(PushB3, alignment = Qt.AlignCenter)
l1.addWidget(PushB4, alignment = Qt.AlignCenter)
l1.addWidget(PushB5, alignment = Qt.AlignCenter)

l2 = QHBoxLayout()

l2.addWidget(TextW, alignment = Qt.AlignCenter)
l2.addLayout(l1)
window.setLayout(l2)

with open('str.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)

ListW.addItems(notes)

#работа кнопок
ListW.clicked.connect(show_noutes)
PushB.clicked.connect(add_notes)
PushB3.clicked.connect(add_tag)
PushB5.clicked.connect(search_tag)
PushB2.clicked.connect(save_note)
PushB4.clicked.connect(del_tag)
PushB1.clicked.connect(del_notes)

window.show()
app.exec_()