import sys
import _pickle as cPickle
import smtplib
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PedidoUI import Ui_MainWindow
from Emergente1 import Ui_Dialog
from Emergente2 import Ui_Dialog2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Ventana opciones de categorias
class PopUp(QDialog,Ui_Dialog):
	"""docstring for PopUp"""
	def __init__(self,*args,**kwargs):
		QDialog.__init__(self,*args,**kwargs)
		self.setupUi(self)
	#Cuerpo
		self.Dic = {}
		self.ListaCategoria = []
		self.UpdateList()
		self.botonAgr.clicked.connect(self.AgregarItems)
		self.botonBor.clicked.connect(self.BorrarLista)
		self.botonAceptar.clicked.connect(self.close)


	#Simplemente guarda los valores de Main en esta Clase
	def ObtenerValores(self, Dic):
		self.Dic = Dic

	#Agrega strings al diccionario de proveedores
	#Y tambien actualiza el listWiget con la info
	def AgregarItems(self):
		AuxText = self.lineEdit.text()
		self.lineEdit.clear()
		if AuxText:
			self.Dic[AuxText] = []
			self.UpdateList()

#Actualizo la lista, borrando el listWidget
	def UpdateList(self):
		self.listWidget.clear()
		self.ListaCategoria = list(self.Dic)
		self.listWidget.addItems(self.ListaCategoria)

	def BorrarLista(self):
		linea = self.listWidget.currentRow()
		del self.Dic[self.ListaCategoria[linea]]
		self.UpdateList()

	def Envio(self):
		return self.Dic

#Ventana de opciones para los mails
class PopUp2(QDialog,Ui_Dialog2):
	def __init__(self,*args,**kwargs):
		QDialog.__init__(self,*args,**kwargs)
		self.setupUi(self)
		#Inicio la Libreta
		self.Libreta = {}
		#Inicio el programa
		
		#Conecto botones
		self.pushButton.clicked.connect(self.AgregarDire)

	def ObtenerValores(self, Dic):
		self.Libreta = Dic

	def Autocompleto(self):
		self.lineEdit_2.setText(self.Libreta[0])
		self.lineEdit.setText(self.Libreta[1])

	def AgregarDire(self):
		self.Libreta[0] = self.lineEdit_2.text() #Usuario
		self.Libreta[1] = self.lineEdit.text()   #Contraseña
		if self.lineEdit_3.text():
			self.Libreta[2].append(self.lineEdit_3.text())
			self.lineEdit_3.clear()
		self.Guardar()

	def Guardar(self):
		with open("LibretaDirecciones", 'wb') as fp:
			cPickle.dump(self.Libreta, fp)



	def Envio(self):
		return self.Libreta

	
#Clase prencipal
class ProgramaPedido(QMainWindow, Ui_MainWindow): 
	def __init__(self,*args,**kwargs):
		QMainWindow.__init__(self,*args,**kwargs)
		self.setupUi(self)
		#Cuaerpo del Main
		#Creo una clase PopUp
		self.Dialog = PopUp(self)
		#Creo el segundo popUp
		self.Dialog2 = PopUp2(self)
		#Creo bases de datos
		self.Pedidos = []
		self.Categorias = {}
		self.Libreta = {
		0:"X",
		1:"X",
		2: []
		}
		self.Mensaje = ""
		#Inicializo el programa
		self.BaseProve()
		self.ComboBox()
		self.UpdateLista()
		self.LeerArchivo()
		self.UpdateDir()

		#Le envio al PopUp el Diccionario
		#con las categorias
		self.Dialog.ObtenerValores(self.Categorias)
		#Le envio la libreta la Pop2
		self.Dialog2.ObtenerValores(self.Libreta)
		self.Dialog2.Autocompleto()
		#Guardo antes de Salir
		app.aboutToQuit.connect(self.Cerrado)
		
		#Botones Conectados:
		self.toolButton.clicked.connect(self.open_dialog)
		self.toolButton_2.clicked.connect(self.opcionesMail)
		self.BotonQuit.clicked.connect(self.Quitar)
		self.botonAdd.clicked.connect(self.AgregarArt)
		self.comboBox_2.activated.connect(self.UpdateLista)
		self.comboBox.activated.connect(self.UpdateSeleccion)
		self.botonEnviar.clicked.connect(self.Emails)
		self.BotonAdj.clicked.connect(self.Adjuntar)
		self.botonAdjT.clicked.connect(self.AdjuntarTodo)

	#Esta Funciones agrega los articulos al listWidget
	#Toma el texto del comboBox con las categorias
	#Busca en el diccionario, agrega el art a la lista
	#Y los sube al Widget
	def AgregarArt(self):
		artText = self.lineEdit.text()
		self.lineEdit.clear()
		if artText:
			AuxText = str(self.comboBox_2.currentText())
			try:
				self.Categorias[AuxText].append(artText)
			except:
				pass
		
		self.UpdateLista()


	def Cerrado(self):
		with open("BaseProve", 'wb') as fp:
			cPickle.dump(self.Categorias, fp)

		
	def Quitar(self):	
		linea = self.listWidget.currentRow()
		try:
			del self.Categorias[self.comboBox_2.currentText()][linea]
		except:
			pass
		self.UpdateLista()

	def UpdateLista(self):
		self.listWidget.clear()
		AuxText = str(self.comboBox_2.currentText())
		try:
			self.listWidget.addItems(self.Categorias[AuxText])
		except:
			flag = 1
		
	#Simplemente activa la ventana emergente para poder
	#Agregar o quitar categorias	
	def open_dialog(self):
		self.Dialog.UpdateList()
		self.Dialog.exec_()
		self.Categorias = self.Dialog.Envio()
		self.ComboBox()

	#Lee la base de datos de Provedores
	#Si no hay, la crea.
	def BaseProve(self):
		FlagEOF = 0
		#Pruebo si existe la Base, sino, la creo.
		try:
			fp = open("BaseProve","rb")
			#Cargo el diccionario donde los Indices son
			#La categoria, y el valor es una lista de Articulos
			while FlagEOF == 0 :
				try:
					self.Categorias = cPickle.load(fp)
				except EOFError:
					FlagEOF = 1
					fp.close()
		except FileNotFoundError:
			fp = open("BaseProve","wb")
			fp.close()

		

	#Actualizo las opciones del combo Box
	def ComboBox(self):
		self.comboBox_2.clear()
		ListaAux = list(self.Categorias)
		self.comboBox_2.addItems(ListaAux)
		
	#Abro el Widget de Opciones para el Mail
	#Cuando Cierro, Guardo la Libreta
	#Cargo el Combobox con direcciones
	def opcionesMail(self):
		self.Dialog2.exec_()
		self.Libreta = self.Dialog2.Envio()
		self.UpdateDir()
		print(self.Libreta)
	
	def UpdateDir(self):
		self.comboBox.clear()
		self.comboBox.addItems(self.Libreta[2])
		self.lineEdit_2.clear()
		self.lineEdit_2.setText(self.comboBox.currentText())
	
	def UpdateSeleccion(self):
		self.lineEdit_2.clear()
		self.lineEdit_2.setText(self.comboBox.currentText())
#Adjunto 1 item
	def Adjuntar(self):
		#Obtengo la Categoria
		AuxText = str(self.comboBox_2.currentText())
		#Obtengo la fila del item, como se agregan al final
		#La fila conicide con el Indice de la Lista
		AuxRow = self.listWidget.currentRow()
		#Guardo el item.
		try:
			AuxItem = self.Categorias[AuxText][AuxRow]
			self.plainTextEdit.appendPlainText(AuxItem)
			#Ahora lo borro de la lista
			del self.Categorias[AuxText][AuxRow]
			#Actualizo la lista
			self.UpdateLista()
		except:
			pass
		
#Adjunto toda la lista		
	def AdjuntarTodo(self):
		#Obtengo la Categoria
		AuxText = str(self.comboBox_2.currentText())
		#Obtengo una Lista de Articulos de Categorias
		try:
			AuxList = list(self.Categorias[AuxText])
			#Recorro la lista, y agrego los items
			for indx, value in enumerate(AuxList):
				self.plainTextEdit.appendPlainText(AuxList[indx])
			#Ahora lo borro de la lista
			self.Categorias[AuxText] = []
			#Actualizo la lista
			self.UpdateLista()
		except:
			pass

#Envio de Mails
	def Emails(self):
		#Creo un objeto s donde guardo los datos de mi Gmail
		s = smtplib.SMTP(host="smtp.gmail.com", port=587)
		s.starttls()
		s.login(self.Libreta[0],self.Libreta[1])
		msg = MIMEMultipart()  #Creo un mensaje
		#Configuro Headers
		msg["From"] = self.Libreta[0]
		msg["To"] = self.comboBox.currentText()
		msg["Subject"] = "Pedido"
		#Llamo al Creador de Mensajes
		self.CrearMensaje()
		#Agrego el mensaje
		msg.attach(MIMEText(self.Mensaje, "plain"))
		#Envio el Mensaje
		s.send_message(msg)
#Creo el Mensaje
	def CrearMensaje(self):
		self.Mensaje = self.plainTextEdit.toPlainText()
		with open("Mensaje.txt","w") as fp:
			fp.write(str(self.Mensaje))

#Leo la libreta de direcciones
	def LeerArchivo(self):
		FlagEOF = 0
		#Pruebo si existe la Base, sino, la creo.
		try:
			fp = open("LibretaDirecciones","rb")
			#Cargo ambas listas con las libretas
			#de direcciones
			while FlagEOF == 0 :
				try:
					self.Libreta = cPickle.load(fp)
				except EOFError:
					FlagEOF = 1
					fp.close()
				
		except FileNotFoundError:
			fp = open("LibretaDirecciones","wb")
			fp.close()


	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	prog = ProgramaPedido()
	prog.show()
	sys.exit(app.exec_())