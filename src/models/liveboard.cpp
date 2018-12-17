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

    // Retrieve the QRail::LiveboardEngine::Factory instance and connect it's signals
    m_factory = QRail::LiveboardEngine::Factory::getInstance();
    connect(m_factory,
            SIGNAL(stream(QRail::VehicleEngine::Vehicle *)),
            this,
            SLOT(handleStream(QRail::VehicleEngine::Vehicle *)));
    connect(m_factory,
            SIGNAL(finished(QRail::LiveboardEngine::Board *)),
            this,
            SLOT(handleFinished(QRail::LiveboardEngine::Board *)));
    connect(m_factory,
            SIGNAL(processing(QUrl)),
            this,
            SLOT(handleProcessing(QUrl)));
    connect(m_factory,
            SIGNAL(error(QString)),
            this,
            SIGNAL(error(QString)));

    // Init variables
    m_entries = QList<QRail::VehicleEngine::Vehicle *>();
    m_liveboard = nullptr;
    m_busy = false;
}

// Invokers
void Liveboard::getBoard(QRail::StationEngine::Station *station,
                         const QRail::LiveboardEngine::Board::Mode &mode)
{
    this->setBusy(true);
    m_factory->getLiveboardByStationURI(station->uri(), mode);
}

void Liveboard::getBoard(const QUrl &uri, const QRail::LiveboardEngine::Board::Mode &mode)
{
    this->setBusy(true);
    m_factory->getLiveboardByStationURI(uri, QDateTime::currentDateTime(),
                                        QDateTime::currentDateTime().addSecs(2 * 3600), mode);
}

void Liveboard::clearBoard()
{
    this->beginResetModel();
    m_entries.clear();
    m_liveboard = nullptr;
    this->endResetModel();
}

// Helpers
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
    roles[hasDelay] = "hasDelay";
    return roles;
}

void Liveboard::loadNext()
{
    if (m_liveboard && !this->isBusy()) {
        qDebug() << "Extending liveboard NEXT";
        this->setBusy(true);
        m_factory->getNextResultsForLiveboard(this->m_liveboard);
    }
}

void Liveboard::loadPrevious()
{
    if (m_liveboard && !this->isBusy()) {
        qDebug() << "Extending liveboard PREVIOUS";
        this->setBusy(true);
        m_factory->getPreviousResultsForLiveboard(this->m_liveboard);
    }
}

void Liveboard::abortCurrentOperation()
{
    qDebug() << "Abort Liveboard";
    m_factory->abortCurrentOperation();
}

int Liveboard::rowCount(const QModelIndex &) const
{
    return m_entries.count();
}

QVariant Liveboard::data(const QModelIndex &index, int role) const
{
    if (!index.isValid()) {
        return QVariant();
    }
    // Break not needed since return makes the rest unreachable.
    switch (role) {
    case URIRole:
        return QVariant(m_entries.at(index.row())->uri().toString());
    case tripURIRole:
        return QVariant(m_entries.at(index.row())->tripURI());
    case headsignRole:
        return QVariant(m_entries.at(index.row())->headsign());
    case arrivalTimeRole:
        return QVariant(m_entries.at(index.row())->intermediaryStops().first()->arrivalTime());
    case arrivalDelayRole:
        return QVariant(m_entries.at(index.row())->intermediaryStops().first()->arrivalDelay());
    case isArrivalCanceledRole:
        return QVariant(m_entries.at(
                            index.row())->intermediaryStops().first()->isArrivalCanceled());
    case departureTimeRole:
        return QVariant(m_entries.at(index.row())->intermediaryStops().first()->departureTime());
    case departureDelayRole:
        return QVariant(m_entries.at(index.row())->intermediaryStops().first()->departureDelay());
    case isDepartureCanceledRole:
        return QVariant(m_entries.at(
                            index.row())->intermediaryStops().first()->isDepartureCanceled());
    case platformRole:
        return QVariant(m_entries.at(index.row())->intermediaryStops().first()->platform());
    case isPlatformNormalRole:
        return QVariant(m_entries.at(
                            index.row())->intermediaryStops().first()->isPlatformNormal());
    case hasLeftRole:
        return QVariant(m_entries.at(index.row())->intermediaryStops().first()->hasLeft());
    case stopTypeRole:
        return QVariant::fromValue(m_entries.at(index.row())->intermediaryStops().first()->type());
    case occupancyLevelRole:
        return QVariant::fromValue(m_entries.at(
                                       index.row())->intermediaryStops().first()->occupancyLevel());
    case isExtraStopRole:
        return QVariant(m_entries.at(index.row())->intermediaryStops().first()->isExtraStop());
    case hasDelay:
        foreach (QRail::VehicleEngine::Vehicle *vehicle, m_entries) {
            if (vehicle->intermediaryStops().first()->arrivalDelay() > 0
                    || vehicle->intermediaryStops().first()->departureDelay() > 0) {
                return true;
            }
        }
        return false;
    default:
        return QVariant();
    }
}

// Processors
void Liveboard::handleStream(QRail::VehicleEngine::Vehicle *entry)
{
    qDebug() << "Inserting:" << entry->uri() << "to:" << entry->headsign() << "time=" <<
             entry->intermediaryStops().first()->departureTime()
             << "+" << entry->intermediaryStops().first()->departureDelay();
    bool foundInsertIndex = false;

    QDateTime newEntryDepartureTime = entry->intermediaryStops().first()->departureTime();
    for (qint16 i = 0; i < m_entries.length(); i++) {
        QDateTime entryDepartureTime = m_entries.at(i)->intermediaryStops().first()->departureTime();

        // TO DO: Smarter inserting: Departure and arrival time are now the same, so this works for now
        if (entryDepartureTime > newEntryDepartureTime) {
            this->beginInsertRows(QModelIndex(), i, i);
            m_entries.insert(i, entry);
            this->endInsertRows();
            foundInsertIndex = true;
            break;
        }
    }

    // Entry should be added in front or at the end of the list
    if (!foundInsertIndex) {
        this->beginInsertRows(QModelIndex(), m_entries.length(), m_entries.length());
        m_entries.append(entry);
        this->endInsertRows();
    }
}

void Liveboard::handleProcessing(const QUrl &uri)
{
    // Task started or running
    QUrlQuery query = QUrlQuery(uri);
    QDateTime timestamp = QDateTime::fromString(query.queryItemValue("departureTime"), Qt::ISODate);
    emit this->processing(uri.toString(), timestamp);
}

void Liveboard::handleFinished(QRail::LiveboardEngine::Board *board)
{
    m_liveboard = board;
    emit this->stationChanged();
    emit this->fromChanged();
    emit this->untilChanged();

    // Task finished
    this->setBusy(false);
}

// Getters & Setters
QRail::StationEngine::Station *Liveboard::station()
{
    return m_liveboard->station();
}

void Liveboard::setStation(QRail::StationEngine::Station *station)
{
    m_liveboard->setStation(station);
    emit this->stationChanged();
}

QDateTime Liveboard::from() const
{
    return m_liveboard->from();
}

void Liveboard::setFrom(const QDateTime &from)
{
    if (m_liveboard->from() != from) {
        m_liveboard->setFrom(from);
        emit this->fromChanged();
    }
}

QDateTime Liveboard::until() const
{
    return m_liveboard->until();
}

void Liveboard::setUntil(const QDateTime &until)
{
    if (m_liveboard->until() != until) {
        m_liveboard->setUntil(until);
        emit this->untilChanged();
    }
}

bool Liveboard::isBusy() const
{
    return m_busy;
}

void Liveboard::setBusy(const bool &busy)
{
    // Only fire the signal when busy state really is changed
    if (m_busy != busy) {
        m_busy = busy;
        emit this->busyChanged();
    }
}
