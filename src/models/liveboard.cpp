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
#include "liveboard.h"

Liveboard::Liveboard(QObject *parent): QAbstractListModel(parent)
{
    // Register custom types to the Qt meta object system
    qRegisterMetaType<QRail::VehicleEngine::Stop::Type>("QRail::VehicleEngine::Stop::Type");
    qRegisterMetaType<QRail::VehicleEngine::Stop::OccupancyLevel>("QRail::VehicleEngine::Stop::OccupancyLevel");
    m_factory = QRail::LiveboardEngine::Factory::getInstance();
    connect(m_factory, SIGNAL(finished(QRail::LiveboardEngine::Board*)), this, SLOT(processBoard(QRail::LiveboardEngine::Board*)));
}

int Liveboard::rowCount(const QModelIndex &) const
{
    return m_board->entries().count();
}

QVariant Liveboard::data(const QModelIndex &index, int role) const
{
    if(!index.isValid()) {
        return QVariant();
    }
    // Break not needed since return makes the rest unreachable.
    switch(role) {
    case URIRole:
        return QVariant(m_board->entries().at(index.row())->uri());
    case tripURIRole:
        return QVariant(m_board->entries().at(index.row())->tripURI());
    case headsignRole:
        return QVariant(m_board->entries().at(index.row())->headsign());
    case arrivalTimeRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->arrivalTime());
    case arrivalDelayRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->arrivalDelay());
    case isArrivalCanceledRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->isArrivalCanceled());
    case departureTimeRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->departureTime());
    case departureDelayRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->departureDelay());
    case isDepartureCanceledRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->isDepartureCanceled());
    case platformRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->platform());
    case isPlatformNormalRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->isPlatformNormal());
    case hasLeftRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->hasLeft());
    case stopTypeRole:
        return QVariant::fromValue(m_board->entries().at(index.row())->intermediaryStops().first()->type());
    case occupancyLevelRole:
        return QVariant::fromValue(m_board->entries().at(index.row())->intermediaryStops().first()->occupancyLevel());
    case isExtraStopRole:
        return QVariant(m_board->entries().at(index.row())->intermediaryStops().first()->isExtraStop());
    default:
        return QVariant();
    }
}

// Invokers
void Liveboard::getBoard(QRail::StationEngine::Station *station)
{
    m_factory->getLiveboardByStationURI(station->uri());
}

void Liveboard::getBoard(const QUrl &uri)
{
    m_factory->getLiveboardByStationURI(uri);
}

QHash<int, QByteArray> Liveboard::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[URIRole] = "URI";
    roles[tripURIRole] = "tripURIRole";
    roles[headsignRole] = "headsign";
    roles[arrivalTimeRole] = "arrivalTime";
    roles[arrivalDelayRole] = "arrivalDelay";
    roles[isArrivalCanceledRole] = "isArrivalCanceled";
    roles[departureTimeRole] = "departureTime";
    roles[departureDelayRole] = "departureDelay";
    roles[isDepartureCanceledRole] = "isDepartureCanceled";
    roles[platformRole] = "platform";
    roles[isPlatformNormalRole] = "isPlatformNormal";
    roles[hasLeftRole] = "hasLeft";
    roles[stopTypeRole] = "stopType";
    roles[occupancyLevelRole] = "occupancy";
    roles[isExtraStopRole] = "isExtraStop";
    return roles;
}

// Processors
void Liveboard::processBoard(QRail::LiveboardEngine::Board *board)
{
    m_board = board;
    qDebug() << "Board received from factory for station:"
             << board->station()->name().value(QLocale::Language::Dutch)
             << "with" << board->entries().count() << "entries";
    emit this->boardChanged();
    emit this->entriesChanged();
    emit this->stationChanged();
    emit this->fromChanged();
    emit this->untilChanged();
}

// Getters & Setters
QRail::StationEngine::Station *Liveboard::station()
{
    return m_board->station();
}

QDateTime Liveboard::from() const
{
    return m_board->from();
}

QDateTime Liveboard::until() const
{
    return m_board->until();
}

bool Liveboard::isBusy() const
{
    return m_busy;
}

void Liveboard::setBusy(const bool &busy)
{
    m_busy = busy;
    emit this->busyChanged();
}
