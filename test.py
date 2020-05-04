import sys
import os

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlApplicationEngine, QQmlEngine, QQmlPropertyMap

#from pp import Person
from soloman import register
#from soloman.pyqt_inter_audio import QAudio
#from soloman.pyqt_inter_video import QVideo
# Create the application instance.
app = QGuiApplication(sys.argv)



"""def register():
    qmlRegisterType(QAudio, 'soloman', 1, 0, 'Audio')
    qmlRegisterType(QVideo, 'soloman', 1, 0, 'Video')"""
# Register the Python type.  Its URI is 'People', it's v1.0 and the type
# will be called 'Person' in QML.
#qmlRegisterType(Person, 'People', 1, 0, 'Person')
#os.environ['QML2_IMPORT_PATH'] = '.'
# Create a QML engine.
register()

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

# Create a component factory and load the QML script.
#component = QQmlComponent(engine)

#QQmlEngine().addImportPath(__file__.replace('\\soloman\\__init__.py', ''))
#engine.rootContext().setContextProperty('ddata', p_map)


engine.load(QUrl('example.qml'))

# Create an instance of the component.
#person = component.create()

"""if person is not None:
    # Print the value of the properties.
    print("The person's name is %s." % person.saveFolder)
else:
    # Print all errors that occurred.
    for error in component.errors():
        print(error.toString())"""

sys.exit(app.exec_())
