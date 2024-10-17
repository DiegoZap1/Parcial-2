from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,
                             QMainWindow,QFormLayout,QLineEdit,
                             QPushButton,QMessageBox,QInputDialog)
from PyQt5.QtCore import Qt
import sqlite3
import sys

conexion = sqlite3.connect('Empleados')
cursor = conexion.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS empleado(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT,
               email TEXT,
               telefono TEXT,
               dui TEXT,
               departamento TEXT,
               sueldo REAL)''')

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        inicio = QLabel('Gestor de Empleados \n')
        inicio.setAlignment(Qt.AlignCenter)

        # Datos
        nombre = QLabel('Nombre Completo: ')
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText('Nombre')

        email = QLabel('Email: ')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email')

        telefono = QLabel('Telefono: ')
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText('Telefono')

        dui = QLabel('Dui: ')
        self.dui_input = QLineEdit()
        self.dui_input.setPlaceholderText('Dui')

        departamento = QLabel('Departamento: ')
        self.departamento_input = QLineEdit()
        self.departamento_input.setPlaceholderText('Departamento')

        sueldo = QLabel('Sueldo: ')
        self.sueldo_input = QLineEdit()
        self.sueldo_input.setPlaceholderText('Sueldo')

        # Botones
        buscar = QPushButton('Buscar')
        buscar.clicked.connect(self.buscarempleado)
        btnAgregar = QPushButton('Agregar')
        btnAgregar.clicked.connect(self.agregar)
        actualizar = QPushButton('Actualizar')
        actualizar.clicked.connect(self.actualizarempleado)
        borrar = QPushButton('Borrar Empleado')
        borrar.clicked.connect(self.borrar)

        layout = QFormLayout()
        layout.addRow(inicio)
        layout.addRow(buscar)
        layout.addRow(nombre, self.nombre_input)
        layout.addRow(email, self.email_input)
        layout.addRow(telefono, self.telefono_input)
        layout.addRow(dui,self.dui_input)
        layout.addRow(departamento, self.departamento_input)
        layout.addRow(sueldo, self.sueldo_input)
        layout.addRow(btnAgregar)
        layout.addRow(actualizar)
        layout.addRow(borrar)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
    
    def buscarempleado(self):
        try:
            buscar, ok = QInputDialog.getText(self,'Buscar','¿Qué empleado quiere buscar?')
            if ok:
                cursor.execute('''SELECT * FROM empleado WHERE nombre LIKE ?''', (f'%{buscar}%',))
                self.empleado = cursor.fetchone()

            self.nombre_input.setText(self.empleado[1])
            self.email_input.setText(self.empleado[2])
            self.telefono_input.setText(self.empleado[3])
            self.dui_input.setText(self.empleado[4])
            self.departamento_input.setText(self.empleado[5])
            self.sueldo_input.setText(str(self.empleado[6]))
        except:
            QMessageBox.information(self,'Empleado Inexistente','El empleado no existe')
            return
    
    def agregar(self):
        nombre = self.nombre_input.text().strip()
        email = self.email_input.text().strip()
        telefono = self.telefono_input.text().strip()
        dui = self.dui_input.text().strip()
        departamento = self.departamento_input.text().strip()
        sueldo_texto = self.sueldo_input.text().strip()
        
        if not (nombre or email or telefono or dui or departamento or sueldo_texto):
            QMessageBox.information(self,"Error","Por favor agrega todos los datos")
            return
        else:
            pass
        try:
            sueldo = float(sueldo_texto)
            QMessageBox.information(self,"Agregado","!Usuario agregado con exito!")
        except:
            QMessageBox.information(self,"Dato incorrecto","Ingrese un sueldo valido")
            
        cursor.execute('''INSERT INTO empleado(nombre,email,telefono,dui,departamento,sueldo)
                       VALUES (?,?,?,?,?,?)''',(nombre,email,telefono,dui,departamento,sueldo))
        conexion.commit()

        self.nombre_input.clear()
        self.email_input.clear()
        self.telefono_input.clear()
        self.dui_input.clear()
        self.departamento_input.clear()
        self.sueldo_input.clear()
    
    def actualizarempleado(self):
        nombre = self.nombre_input.text()
        email = self.email_input.text()
        telefono = self.telefono_input.text()
        dui = self.dui_input.text()
        departamento = self.departamento_input.text()
        sueldo_texto = self.sueldo_input.text()

        try:
            sueldo = float(sueldo_texto)
            QMessageBox.information(self,"Actualizado","¡Empleado Actualizado con exito!")
        except:
            QMessageBox.information(self,"Error","Escriba un sueldo valido")

        cursor.execute('''
        UPDATE empleado
        SET nombre = ?, email = ?, telefono = ?, dui = ?, departamento = ?, sueldo = ?
        WHERE id = ?''', (nombre,email,telefono,dui,departamento,sueldo,self.empleado[0]))
        conexion.commit()

        self.nombre_input.clear()
        self.email_input.clear()
        self.telefono_input.clear()
        self.dui_input.clear()
        self.departamento_input.clear()
        self.sueldo_input.clear()
    

    def borrar(self):
        borrar,ok = QInputDialog.getText(self,"Borrar?","¿Desea borrar este empleado? (Si/No)")
        if ok:
            if borrar.lower() == "si":
                cursor.execute('''DELETE FROM empleado WHERE id = ?''',(self.empleado[0],))
                conexion.commit()
                QMessageBox.information(self,"Borrado","¡Empleado Borrado con exito!")
        else:
            QMessageBox.information(self,"Cancelado","Operacion cancelada")
            return
        
        self.nombre_input.clear()
        self.email_input.clear()
        self.telefono_input.clear()
        self.dui_input.clear()
        self.departamento_input.clear()
        self.sueldo_input.clear()

app = QApplication(sys.argv)
ventana = mainwindow()
ventana.show()
app.exec()