# NOTICE:
#
# Application name defined in TARGET has a corresponding QML filename.
# If name defined in TARGET is changed, the following needs to be done
# to match new name:
#   - corresponding QML filename must be changed
#   - desktop icon filename must be changed
#   - desktop filename must be changed
#   - icon definition filename in desktop file must be changed
#   - translation filenames have to be changed

# The name of your application
TARGET = lcrail

# QMake config
CONFIG += sailfishapp \
        c++11

# Qt modules
QT += core \
    network \
    positioning \
    concurrent \
sql

SOURCES += src/lcrail.cpp \
    src/models/liveboard.cpp \
    src/models/stations.cpp \
    src/models/router.cpp \
    src/models/trip.cpp

# Enable GCOV coverage reports (https://medium.com/@kelvin_sp/generating-code-coverage-with-qt-5-and-gcov-on-mac-os-4999857f4676)
# --coverage option is synonym for: -fprofile-arcs -ftest-coverage -lgcov
QMAKE_CXXFLAGS += --coverage
QMAKE_LFLAGS += --coverage

# QRail library build location
CONFIG(debug, debug|release) {
    QRAIL_LOCATION = $$PWD/QRail/build/debug
}
else {
    QRAIL_LOCATION = $$PWD/QRail/build/release
}
LIBS += $$QRAIL_LOCATION/libqrail.a

## Headers include path of the QRail library
INCLUDEPATH += $$PWD/QRail/src/include \
    $$PWD/QRail/qtcsv/include

DISTFILES += qml/lcrail.qml \
    qml/cover/CoverPage.qml \
    qml/pages/FirstPage.qml \
    rpm/lcrail.changes \
    rpm/lcrail.spec \
    rpm/lcrail.yaml \
    translations/*.ts \
    lcrail.desktop \
    qml/universal-components/README.md \
    qml/universal-components/controls/UC/ApplicationWindow.qml \
    qml/universal-components/controls/UC/BackgroundRectangle.qml \
    qml/universal-components/controls/UC/BusyIndicator.qml \
    qml/universal-components/controls/UC/Button.qml \
    qml/universal-components/controls/UC/ComboBox.qml \
    qml/universal-components/controls/UC/Dialog.qml \
    qml/universal-components/controls/UC/IconButton.qml \
    qml/universal-components/controls/UC/Label.qml \
    qml/universal-components/controls/UC/Menu.qml \
    qml/universal-components/controls/UC/MenuItem.qml \
    qml/universal-components/controls/UC/Page.qml \
    qml/universal-components/controls/UC/PageHeader.qml \
    qml/universal-components/controls/UC/PlatformFlickable.qml \
    qml/universal-components/controls/UC/PlatformListView.qml \
    qml/universal-components/controls/UC/Popup.qml \
    qml/universal-components/controls/UC/ProgressBar.qml \
    qml/universal-components/controls/UC/Screen.qml \
    qml/universal-components/controls/UC/ScrollBar.qml \
    qml/universal-components/controls/UC/SearchField.qml \
    qml/universal-components/controls/UC/SectionHeader.qml \
    qml/universal-components/controls/UC/Slider.qml \
    qml/universal-components/controls/UC/Switch.qml \
    qml/universal-components/controls/UC/TextArea.qml \
    qml/universal-components/controls/UC/TextField.qml \
    qml/universal-components/controls/UC/TextSwitch.qml \
    qml/universal-components/controls/UC/TopMenu.qml \
    qml/universal-components/controls/UC/VerticalScrollDecorator.qml \
    qml/universal-components/silica/UC/ApplicationWindow.qml \
    qml/universal-components/silica/UC/BackgroundRectangle.qml \
    qml/universal-components/silica/UC/BusyIndicator.qml \
    qml/universal-components/silica/UC/Button.qml \
    qml/universal-components/silica/UC/ComboBox.qml \
    qml/universal-components/silica/UC/Dialog.qml \
    qml/universal-components/silica/UC/IconButton.qml \
    qml/universal-components/silica/UC/Label.qml \
    qml/universal-components/silica/UC/Menu.qml \
    qml/universal-components/silica/UC/MenuItem.qml \
    qml/universal-components/silica/UC/Page.qml \
    qml/universal-components/silica/UC/PageHeader.qml \
    qml/universal-components/silica/UC/PlatformFlickable.qml \
    qml/universal-components/silica/UC/PlatformListView.qml \
    qml/universal-components/silica/UC/Popup.qml \
    qml/universal-components/silica/UC/ProgressBar.qml \
    qml/universal-components/silica/UC/Screen.qml \
    qml/universal-components/silica/UC/ScrollBar.qml \
    qml/universal-components/silica/UC/SearchField.qml \
    qml/universal-components/silica/UC/SectionHeader.qml \
    qml/universal-components/silica/UC/Slider.qml \
    qml/universal-components/silica/UC/Switch.qml \
    qml/universal-components/silica/UC/TextArea.qml \
    qml/universal-components/silica/UC/TextField.qml \
    qml/universal-components/silica/UC/TextSwitch.qml \
    qml/universal-components/silica/UC/TopMenu.qml \
    qml/universal-components/silica/UC/VerticalScrollDecorator.qml \
    qml/universal-components/tests/tst_button.qml \
    qml/universal-components/ubuntu/UC/Button.qml \
    qml/universal-components/ubuntu/UC/Label.qml \
    qml/universal-components/ubuntu/UC/Page.qml \
    qml/universal-components/ubuntu/UC/PlatformFlickable.qml \
    qml/universal-components/ubuntu/UC/Slider.qml \
    qml/universal-components/ubuntu/UC/Switch.qml \
    qml/universal-components/ubuntu/UC/TextArea.qml \
    qml/universal-components/ubuntu/UC/TextField.qml \
    qml/universal-components/ubuntu/UC/VerticalScrollDecorator.qml \
    qml/universal-components/tests/README.rst \
    qml/components/Menu.qml \
    qml/components/ConnectionSelector.qml \
    qml/pages/LiveboardPage.qml \
    qml/components/liveboard/LiveboardHeader.qml \
    qml/components/liveboard/LiveboardDelegate.qml \
    qml/js/utils.js \
    qml/pages/StationSelectorPage.qml \
    qml/components/station/StationSelectorHeader.qml \
    qml/components/station/StationSelectorDelegate.qml \
    qml/pages/RouterPage.qml \
    qml/components/router/RouterDelegate.qml \
    qml/components/router/RouterStationIndicator.qml \
    qml/components/router/RouterTransferIndicator.qml

SAILFISHAPP_ICONS = 86x86 108x108 128x128 172x172

# to disable building translations every time, comment out the
# following CONFIG line
CONFIG += sailfishapp_i18n

# German translation is enabled as an example. If you aren't
# planning to localize your app, remember to comment out the
# following TRANSLATIONS line. And also do not forget to
# modify the localized app name in the the .desktop file.
TRANSLATIONS += translations/lcrail-de.ts

HEADERS += \
    src/models/liveboard.h \
    src/models/stations.h \
    src/models/router.h \
    src/models/trip.h
