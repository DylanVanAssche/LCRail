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
#include "trip.h"

Trip::Trip(const QList<QRail::RouterEngine::Transfer *> &trip,
           QObject *parent): QAbstractListModel(parent)
{
    m_trip = trip;
}

QHash<int, QByteArray> Trip::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[URIRole] = "URI";
    roles[stationRole] = "station";
    roles[timeRole] = "time";
    roles[delayRole] = "delay";
    roles[isCanceled] = "isCanceled";
    roles[vehicleURIRole] = "vehicleURI";
    roles[vehicleHeadsignRole] = "vehicleHeadsign";
    roles[platformRole] = "platform";
    roles[isNormalPlatformRole] = "isPlatformNormal";
    roles[isPassed] = "isPassed";
    return roles;
}

int Trip::rowCount(const QModelIndex &) const
{
    return m_trip.count();
}

QVariant Trip::data(const QModelIndex &index, int role) const
{
    if (!index.isValid()) {
        return QVariant();
    }
    // Break not needed since return makes the rest unreachable.
    switch (role) {
    case URIRole:
        return QVariant(QString("http://example.com"));
    case stationRole:
        return QVariant(m_trip.at(index.row())->station()->name().value(QLocale::Language::English));
    case timeRole:
        return QVariant(m_trip.at(index.row())->time());
    case delayRole:
        return QVariant(m_trip.at(index.row())->delay());
    case vehicleURIRole:
        return QVariant(QString("http://irail.be/vehicle/IC1234"));
    case vehicleHeadsignRole:
        return QVariant(QString("N/A"));
    case isCanceled:
        return QVariant(m_trip.at(index.row())->isCanceled());
    case platformRole:
        return QVariant(m_trip.at(index.row())->platform());
    case isNormalPlatformRole:
        return QVariant(m_trip.at(index.row())->isNormalPlatform());
    // Expose more stuff from QRail: TO DO
    // arrival platform, time between, rest of N/A, ...
    default:
        return QVariant();
    }
}
