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

#include "engines/liveboard/liveboardboard.h"
#include "engines/liveboard/liveboardfactory.h"

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
        isExtraStopRole = Qt::UserRole + 15
    };
    explicit Liveboard(QObject *parent = nullptr);
    virtual int rowCount(const QModelIndex&) const;
    virtual QVariant data(const QModelIndex &index, int role) const;
    QRail::StationEngine::Station *station();
    QDateTime from() const;
    QDateTime until() const;
    bool isBusy() const;
    void getBoard(QRail::StationEngine::Station *station);
    void getBoard(const QUrl &uri);

protected:
    QHash<int, QByteArray> roleNames() const;

signals:
    void busyChanged();
    void boardChanged();
    void entriesChanged();
    void stationChanged();
    void fromChanged();
    void untilChanged();

private slots:
    void processBoard(QRail::LiveboardEngine::Board *board);

private:
    bool m_busy;
    QRail::LiveboardEngine::Board *m_board;
    QRail::LiveboardEngine::Factory *m_factory;
    void setBusy(const bool &busy);
};

#endif // LIVEBOARD_H
