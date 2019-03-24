#include "sailfishos.h"

SailfishOS::SailfishOS(QObject *parent) : QObject(parent)
{

}

void SailfishOS::createNotification(QString title, QString text, QString feedback, QString category) {
    // Trim when too long
    const QString body = text.length() > MAX_BODY_LENGTH ? text.left(MAX_BODY_LENGTH-3) + "..." : text;
    const QString preview = text.length() > MAX_PREVIEW_LENGTH ? text.left(MAX_PREVIEW_LENGTH-3) + "..." : text;

    // Build Notification object
    Notification notification;
    notification.setAppName("LCRail");
    notification.setAppIcon("harbour-lcrail");
    notification.setBody(body);
    notification.setPreviewSummary(title);
    notification.setPreviewBody(preview);
    notification.setCategory(category);
    notification.setHintValue("x-nemo-feedback", feedback);
    notification.setHintValue("x-nemo-priority", 120);
    notification.setHintValue("x-nemo-display-on", true);
    notification.publish();
}
