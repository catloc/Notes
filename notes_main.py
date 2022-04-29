from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QInputDialog
import json

app = QApplication ([])

''' Описываем структуру файла ''' 

notes = {
    'Название заметки' :
    {
        'текст' : 'Очень важный текст заметки',
        'теги' : ['черновик', 'мысли']
    }
}

with open ('notes_data.json', 'w') as file:
    json.dump(notes, file)

notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')

list_notes = QListWidget()
list_notes_lable = QLabel('Список заметок')

button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

list_tag = QListWidget()
list_tag_label = QLabel('Список тегов')

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
field_text.setPlaceholderText('Введите текст...')

button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_lable)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
col_2.addLayout(row_1)
col_2.addWidget(button_note_save)

col_2.addWidget(list_tag_label)
col_2.addWidget(list_tag)
col_2.addWidget(field_tag)
row_2 = QHBoxLayout()
row_2.addWidget(button_tag_add)
row_2.addWidget(button_tag_del)
col_2.addLayout(row_2)
col_2.addWidget(button_tag_search)

layout_notes.addLayout(col_1)
layout_notes.addLayout(col_2)
notes_win.setLayout(layout_notes)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'Название заметки')
    if ok and note_name != '':
        notes[note_name] = {'текст' : '', 'теги' : []}
        list_notes.addItem(note_name)
        list_tag.addItems(notes[note_name]['теги'])
    else:
        print('Заметка не выбрана')

def show_notes():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tag.clear()
    list_tag.addItems(notes[name]['теги'])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes)
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print('Заметка для удаления не выбрана!')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tag.addItem(tag)
            list_tag.clear()
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print('Заметка для добавления тега не выбрана!')
            
def del_tag():
    if list_tag.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tag.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tag.clear()
        list_tag.addItems(notes[key]['теги'])
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
    else:
        print('Тег для удаления не выбран!')

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')
    else:
        pass


list_notes.itemClicked.connect(show_notes)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

notes_win.show()

with open ('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec()