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
#ifndef LIVEBOARD_H
#define LIVEBOARD_H

#include <QtCore/QAbstractListModel>
#include <QtCore/QDateTime>
#include <QtCore/QList>
#include <QtCore/QModelIndex>
#include <QtCore/QUrl>
#include <QtCore/QUrlQuery>
#include <QtCore/QHash>
#include <QtCore/QByteArray>
#include <QtCore/QVariant>
#include <algorithm>

#include "engines/liveboard/liveboardboard.h"
#include "engines/liveboard/liveboardfactory.h"
#include "engines/station/stationstation.h"
#include "engines/vehicle/vehiclevehicle.h"

class Liveboard : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(bool busy READ isBusy NOTIFY busyChanged)
    Q_PROPERTY(QRail::StationEngine::Station *station READ station NOTIFY stationChanged)
    Q_PROPERTY(QDateTime from READ from NOTIFY fromChanged)
    Q_PROPERTY(QDateTime until READ until NOTIFY untilChanged)

public:
    // Entries roles
    enum Roles {
        URIRole = Qt::UserRole + 1,
        tripURIRole = Qt::UserRole + 2,
        headsignRole = Qt::UserRole + 3,
        arrivalTimeRole = Qt::UserRole + 4,
        arrivalDelayRole = Qt::UserRole + 5,
        isArrivalCanceledRole = Qt::UserRole + 6,
        departureTimeRole = Qt::UserRole + 7,
        departureDelayRole = Qt::UserRole + 8,
        isDepartureCanceledRole = Qt::UserRole + 9,
        platformRole = Qt::UserRole + 10,
        isPlatformNormalRole = Qt::UserRole + 11,
        hasLeftRole = Qt::UserRole + 12,
        stopTypeRole = Qt::UserRole + 13,
        occupancyLevelRole = Qt::UserRole + 14,
        isExtraStopRole = Qt::UserRole + 15,
        hasDelay = Qt::UserRole + 16
    };
    explicit Liveboard(QObject *parent = nullptr);
    virtual int rowCount(const QModelIndex &) const;
    virtual QVariant data(const QModelIndex &index, int role) const;
    QRail::StationEngine::Station *station();
    QDateTime from() const;
    QDateTime until() const;
    bool isBusy() const;
    Q_INVOKABLE void getBoard(QRail::StationEngine::Station *station,
                              const QRail::LiveboardEngine::Board::Mode &mode = QRail::LiveboardEngine::Board::Mode::DEPARTURES);
    Q_INVOKABLE void getBoard(const QUrl &uri,
                              const QRail::LiveboardEngine::Board::Mode &mode = QRail::LiveboardEngine::Board::Mode::DEPARTURES);

    Q_INVOKABLE void clearBoard();
    Q_INVOKABLE void loadNext(); // fetchMore is only usuable for synced operations
    Q_INVOKABLE void loadPrevious();

protected:
    QHash<int, QByteArray> roleNames() const override;

signals:
    void busyChanged();
    void entriesChanged();
    void stationChanged();
    void fromChanged();
    void untilChanged();
    void processing(const QString &uri, const QDateTime &timestamp);
    void error(const QString &message);
    void finished();

private slots:
    void handleStream(QRail::VehicleEngine::Vehicle *entry);
    void handleProcessing(const QUrl &uri);
    void handleFinished(QRail::LiveboardEngine::Board *board);

private:
    bool m_busy;
    QRail::LiveboardEngine::Board *m_liveboard;
    QList<QRail::VehicleEngine::Vehicle *> m_entries;
    bool m_hasDelay;
    QRail::LiveboardEngine::Factory *m_factory;
    void setBusy(const bool &busy);
    void setFrom(const QDateTime &from);
    void setUntil(const QDateTime &until);
    void setStation(QRail::StationEngine::Station *station);
};

#endif // LIVEBOARD_H
