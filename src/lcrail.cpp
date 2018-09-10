#ifdef QT_QML_DEBUG
#include <QtQuick>
#endif

#include <sailfishapp.h>
#include <QQmlEngine>
#include <QUrl>
#include "engines/station/stationfactory.h"

int main(int argc, char *argv[])
{
    initQRail();
    // SailfishApp::main() will display "qml/LCRail.qml", if you need more
    // control over initialization, you can use:
    //
    //   - SailfishApp::application(int, char *[]) to get the QGuiApplication *
    //   - SailfishApp::createView() to get a new QQuickView * instance
    //   - SailfishApp::pathTo(QString) to get a QUrl to a resource file
    //   - SailfishApp::pathToMainQml() to get a QUrl to the main QML file
    //
    // To display the view, call "show()" (will show fullscreen on device).
    QRail::StationEngine::Factory *factory = QRail::StationEngine::Factory::getInstance();
    factory->getStationByURI(QUrl("https://irail.be/stations/NMBS/008812005"));

    return SailfishApp::main(argc, argv);
}
