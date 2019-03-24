#ifndef SAILFISHOS_H
#define SAILFISHOS_H

#include <QtCore/QObject>
#include <nemonotifications-qt5/notification.h>
#define MAX_BODY_LENGTH 200
#define MAX_PREVIEW_LENGTH 100

class SailfishOS : public QObject
{
    Q_OBJECT
public:
    explicit SailfishOS(QObject *parent = nullptr);
    static void createNotification(QString title, QString text, QString feedback, QString category);
};

#endif // SAILFISHOS_H
