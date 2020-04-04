import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlApplicationEngine

#from pp import Person
from soloman import register
# Create the application instance.
app = QGuiApplication(sys.argv)

# Register the Python type.  Its URI is 'People', it's v1.0 and the type
# will be called 'Person' in QML.
#qmlRegisterType(Person, 'People', 1, 0, 'Person')

# Create a QML engine.
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

# Create a component factory and load the QML script.
#component = QQmlComponent(engine)
register()
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
