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
#ifndef TRIP_H
#define TRIP_H

#include <QtCore/QAbstractListModel>
#include <QtCore/QList>
#include <QtCore/QObject>
#include <QtCore/QUrl>
#include <QtCore/QVariant>
#include <QtCore/QModelIndex>
#include <QtCore/QString>
#include <QtCore/QHash>
#include <QtCore/QByteArray>

#include "engines/router/routertransfer.h"

class Trip : public QAbstractListModel
{
public:
    enum Roles {
        URIRole = Qt::UserRole + 1,
        stationRole = Qt::UserRole + 2,
        timeRole = Qt::UserRole + 3,
        delayRole = Qt::UserRole + 4,
        isCanceled = Qt::UserRole + 5,
        vehicleURIRole = Qt::UserRole + 6,
        vehicleHeadsignRole = Qt::UserRole + 7,
        platformRole = Qt::UserRole + 8,
        isNormalPlatformRole = Qt::UserRole + 9,
        isPassed = Qt::UserRole + 10
    };
    explicit Trip(const QList<QRail::RouterEngine::Transfer *> &trip,
                  QObject *parent = nullptr);
    virtual int rowCount(const QModelIndex &) const;
    virtual QVariant data(const QModelIndex &index, int role) const;

protected:
    QHash<int, QByteArray> roleNames() const override;

private:
    QList<QRail::RouterEngine::Transfer *> m_trip;
};

#endif // TRIP_H
