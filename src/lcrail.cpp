#ifdef QT_QML_DEBUG
#include <QtQuick>
#endif

#include <sailfishapp.h>
#include <QQmlEngine>
#include <QUrl>
#include <QtQml>

#include "qrail.h"
#include "models/liveboard.h"
#include "models/stations.h"
#include "models/router.h"

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
    qmlRegisterUncreatableType<QRail::LiveboardEngine::Board>("LCRail.Models.Liveboard.Board", 1, 0,
                                                              "Board", "read only");
    qmlRegisterUncreatableType<QRail::StationEngine::Station>("LCRail.Models.Station", 1, 0, "Station",
                                                              "read only");
    qmlRegisterUncreatableType<QRail::RouterEngine::Route>("LCRail.Models.Route", 1, 0, "Route",
                                                           "read only");
    qmlRegisterType<Liveboard>("LCRail.Views.Liveboard", 1, 0, "Liveboard");
    qmlRegisterType<Router>("LCRail.Views.Router", 1, 0, "Router");
    qmlRegisterType<Stations>("LCRail.Views.Stations", 1, 0, "StationsSearch");

    return SailfishApp::main(argc, argv);
}
