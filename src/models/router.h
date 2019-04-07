/*
*   This file is part of LCRail.
*
*   LCRail is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   LCRail is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with LCRail.  If not, see <http://www.gnu.org/licenses/>.
*/
#ifndef ROUTER_H
#define ROUTER_H

#include <QtCore/QAbstractListModel>
#include <QtCore/QVariant>
#include <QtCore/QUrl>
#include <QtCore/QUrlQuery>
#include <QtCore/QDateTime>
#include <QtCore/QString>
#include <QtCore/QModelIndex>
#include <QtCore/QList>
#include <QtCore/QHash>
#include <QtCore/QByteArray>

#include "engines/router/routerplanner.h"
#include "engines/router/routerroute.h"
#include "engines/vehicle/vehiclevehicle.h"
#include "trip.h"
#include "../sailfishos.h"

class Router : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(bool busy READ isBusy NOTIFY busyChanged)

public:
    enum Roles {
        tripRole = Qt::UserRole + 1
    };
    explicit Router(QObject *parent = nullptr);
    virtual int rowCount(const QModelIndex &) const;
    virtual QVariant data(const QModelIndex &index, int role) const;
    Q_INVOKABLE void getConnections(const QString &departureStation,
                                    const QString &arrivalStation,
                                    const QDateTime &departureTime,
                                    const quint16 &maxTransfers);
    Q_INVOKABLE void clearRoutes();
    Q_INVOKABLE void abortCurrentOperation();
    bool isBusy() const;

signals:
    void busyChanged();
    void processing(const QString &uri, const QDateTime &timestamp);
    void benchmark(qint64 time);

private slots:
    void handleStream(QRail::RouterEngine::Route *route);
    void handleFinished(QRail::RouterEngine::Journey *journey);
    void handleProcessing(const QUrl &uri);
    void updateReceived(qint64 time);

protected:
    QHash<int, QByteArray> roleNames() const override;

private:
    qint64 m_before;
    qint64 m_after;
    QRail::RouterEngine::Planner *m_planner;
    QList<QRail::RouterEngine::Route *> m_routes;
    bool m_busy;
    bool m_isCancelled;
    void setBusy(const bool &busy);
};

#endif // ROUTER_H
