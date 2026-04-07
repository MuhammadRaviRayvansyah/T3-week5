Nama: Muhammad Ravi Rayvansyah
NIM: F1D02410078
Kelas: C

import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QFileDialog, QFontDialog, 
                             QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton)
from PySide6.QtGui import QAction, QKeySequence, QIcon, QFont, QTextCursor
from PySide6.QtCore import Qt

class FindReplace(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find | Replace")
        self.editor = parent.editor if parent else None
        
        layout = QVBoxLayout()
        
        find_layout = QHBoxLayout()
        self.find_input = QLineEdit()
        find_layout.addWidget(QLabel("Find:"))
        find_layout.addWidget(self.find_input)
        
        replace_layout = QHBoxLayout()
        self.replace_input = QLineEdit()
        replace_layout.addWidget(QLabel("Replace:"))
        replace_layout.addWidget(self.replace_input)
        
        button_layout = QHBoxLayout()
        self.find_button = QPushButton("Find Next")
        self.replace_button = QPushButton("Replace")
        self.replace_all_button = QPushButton("Replace All")
        
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.replace_button)
        button_layout.addWidget(self.replace_all_button)
        
        layout.addLayout(find_layout)
        layout.addLayout(replace_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.find_button.clicked.connect(self.find_next)
        self.replace_button.clicked.connect(self.replace)
        self.replace_all_button.clicked.connect(self.replace_all)

    def find_next(self):
        text = self.find_input.text()
        if text and self.editor:
            found = self.editor.find(text)
            if not found:
                self.editor.moveCursor(QTextCursor.MoveOperation.Start)
                if not self.editor.find(text):
                    QMessageBox.information(self, "Notepad Clone", f"Teks '{text}' tidak ditemukan.")

    def replace(self):
        text_to_find = self.find_input.text()
        cursor = self.editor.textCursor()
        
        if cursor.hasSelection() and cursor.selectedText() == text_to_find:
            cursor.insertText(self.replace_input.text())
            self.editor.find(text_to_find)
        else:
            self.find_next()

    def replace_all(self):
        text = self.find_input.text()
        replace_text = self.replace_input.text()
        if not text: return
        
        self.editor.moveCursor(QTextCursor.MoveOperation.Start)
        count = 0
        while self.editor.find(text):
            self.editor.textCursor().insertText(replace_text)
            count += 1
        QMessageBox.information(self, "Notepad Clone", f"{count} teks berhasil diganti.")


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_modified = False
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.setCentralWidget(self.editor)
        
        self.editor.textChanged.connect(self.text_changed)
        
        self.setup_ui()
        self.update_title()
        
    def setup_ui(self):
        self.resize(1000, 600)
        self.style_qss()
        
        self.create_actions()
        
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("File")
        file_menu.addActions([self.new, self.open, self.save, self.save_as])
        
        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addActions([self.undo, self.redo, self.cut, self.copy, self.paste, self.select_all, self.find_word])
        
        format_menu = menu_bar.addMenu("Format")
        format_menu.addActions([self.font_word, self.wrap])
        
        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(self.about)
        
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        toolbar.addActions([self.new, self.open, self.save])
        toolbar.addSeparator()
        toolbar.addActions([self.cut, self.copy, self.paste])
        toolbar.addSeparator()
        toolbar.addAction(self.find_word)
        
        self.status_bar = self.statusBar()
        self.status_label = QLabel("Baris: 1 | Karakter: 0")
        self.format_label = QLabel("UTF-8 | Word Wrap: ON")
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.format_label)

    def create_actions(self):
        icon_path = "icons" 

        def load_icon(name):
            return QIcon(os.path.join(icon_path, name))

        self.new = QAction(load_icon("new.png"), "New", self, shortcut=QKeySequence.New, triggered=self.new_file)
        self.open = QAction(load_icon("open.png"), "Open", self, shortcut=QKeySequence.Open, triggered=self.open_file)
        self.save = QAction(load_icon("save.png"), "Save", self, shortcut=QKeySequence.Save, triggered=self.save_file)
        self.save_as = QAction(load_icon("save-as.png"),"Save As", self, shortcut=QKeySequence.SaveAs, triggered=self.save_as_file)
        
        self.undo = QAction(load_icon("undo.png"), "Undo", self, shortcut=QKeySequence.Undo, triggered=self.editor.undo)
        self.redo = QAction(load_icon("redo.png"),"Redo", self, shortcut=QKeySequence.Redo, triggered=self.editor.redo)
        self.cut = QAction(load_icon("cut.png"), "Cut", self, shortcut=QKeySequence.Cut, triggered=self.editor.cut)
        self.copy = QAction(load_icon("copy.png"), "Copy", self, shortcut=QKeySequence.Copy, triggered=self.editor.copy)
        self.paste = QAction(load_icon("paste.png"), "Paste", self, shortcut=QKeySequence.Paste, triggered=self.editor.paste)
        self.select_all = QAction(load_icon("select-all.png"),"Select All", self, shortcut=QKeySequence.SelectAll, triggered=self.editor.selectAll)
        self.find_word = QAction(load_icon("find.png"), "Find", self, shortcut=QKeySequence.Find, triggered=self.find_dialog)
        
        self.font_word = QAction("Font...", self, triggered=self.change_font)
        self.wrap = QAction("Word Wrap", self, checkable=True, triggered=self.toggle_wrap)
        self.wrap.setChecked(True)
        self.about = QAction("About Notepad", self, triggered=self.about_dialog)

    def style_qss(self):
        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Peringatan: style.qss tidak ditemukan.")

    def update_title(self):
        title = os.path.basename(self.current_file) if self.current_file else "Untitled"
        modifier = "*" if self.is_modified else ""
        self.setWindowTitle(f"{title}{modifier} - Notepad Clone")

    def text_changed(self):
        self.is_modified = True
        self.update_title()
        text = self.editor.toPlainText()
        baris = self.editor.document().blockCount()
        karakter = len(text)
        self.status_label.setText(f"Baris: {baris} | Karakter: {karakter}")

    def save_changed(self):
        if not self.is_modified: 
            return True
            
        res = QMessageBox.question(self, "Notepad Clone", "Simpan perubahan?", QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
                                 
        if res == QMessageBox.StandardButton.Save: 
            return self.save_file()
        elif res == QMessageBox.StandardButton.Discard:
            return True
        else: 
            return False

    def new_file(self):
        if self.save_changed():
            self.editor.clear()
            self.current_file = None
            self.is_modified = False
            self.update_title()

    def open_file(self):
        if self.save_changed():
            f_name, _ = QFileDialog.getOpenFileName(self, "Open", "", "Text Files (*.txt);;All Files (*)")
            if f_name:
                with open(f_name, 'r', encoding='utf-8') as f:
                    self.editor.setText(f.read())
                self.current_file = f_name
                self.is_modified = False
                self.update_title()

    def save_file(self):
        if not self.current_file: return self.save_as_file()
        with open(self.current_file, 'w', encoding='utf-8') as f:
            f.write(self.editor.toPlainText())
        self.is_modified = False
        self.update_title()
        return True

    def save_as_file(self):
        f_name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)")
        if f_name:
            self.current_file = f_name
            return self.save_file()
        return False

    def change_font(self):
        font, ok = QFontDialog.getFont(self.editor.font(), self)
        if ok:
            self.editor.setFont(font)

    def toggle_wrap(self):
        mode = QTextEdit.WidgetWidth if self.wrap.isChecked() else QTextEdit.NoWrap
        self.editor.setLineWrapMode(mode)
        status = "ON" if self.wrap.isChecked() else "OFF"
        self.format_label.setText(f"UTF-8 | Word Wrap: {status}")

    def find_dialog(self):
        dialog = FindReplace(self)
        dialog.show()

    def about_dialog(self):
        QMessageBox.about(self, "About", "Notepad Clone v1.0\nCreated by MRR")

    def closeEvent(self, event):
        if self.save_changed(): event.accept()
        else: event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Notepad()
    window.show()
    sys.exit(app.exec())
