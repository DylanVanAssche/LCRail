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
#include "router.h"

Router::Router(QObject *parent) : QAbstractListModel(parent)
{
    // Register custom types to the Qt meta object system
    qRegisterMetaType<Trip *>("Trip *");
    qRegisterMetaType<QRail::RouterEngine::Route *>("QRail::RouterEngine::Route *");
    qRegisterMetaType<QList<QRail::RouterEngine::Route *>>("QList<QRail::RouterEngine::Route *>");
    qRegisterMetaType<QRail::VehicleEngine::Vehicle *>("QRail::VehicleEngine::Vehicle *");

    // Retrieve the QRail::RouterEngine::Planner instance and connect its signals
    m_planner = QRail::RouterEngine::Planner::getInstance();
    connect(m_planner,
            SIGNAL(finished(QRail::RouterEngine::Journey *)),
            this,
            SLOT(handleFinished(QRail::RouterEngine::Journey *)));
    connect(m_planner,
            SIGNAL(stream(QRail::RouterEngine::Route *)),
            this,
            SLOT(handleStream(QRail::RouterEngine::Route *)));
    connect(m_planner,
            SIGNAL(processing(QUrl)),
            this,
            SLOT(handleProcessing(QUrl)));
    connect(m_planner, SIGNAL(updateReceived(qint64)), this, SLOT(updateReceived(qint64)));

    // Init variables
    m_routes = QList<QRail::RouterEngine::Route *>();
    m_busy = false;
}

QHash<int, QByteArray> Router::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[tripRole] = "trip";
    return roles;
}

int Router::rowCount(const QModelIndex &) const
{
    return m_routes.count();
}

QVariant Router::data(const QModelIndex &index, int role) const
{
    if (!index.isValid()) {
        return QVariant();
    }
    // Break not needed since return makes the rest unreachable.
    QSharedPointer<Trip> trip; // http://www.cplusplus.com/forum/beginner/48287/
    switch (role) {
    case tripRole:
        trip = QSharedPointer<Trip>(new Trip(m_routes.at(index.row())->transfers()), &QObject::deleteLater);
        return QVariant::fromValue(trip);
    default:
        return QVariant();
    }
}

void Router::getConnections(const QString &departureStation,
                            const QString &arrivalStation,
                            const QDateTime &departureTime,
                            const quint16 &maxTransfers)
{
    if (!this->isBusy()) {
        this->setBusy(true);
        m_before = QDateTime::currentMSecsSinceEpoch();
        this->clearRoutes();
        qDebug() << "DEPARTURE TIME ROUTER:" << departureTime.toUTC();
        m_planner->getConnections(QUrl(departureStation),
                                  QUrl(arrivalStation),
                                  departureTime.toUTC(),
                                  maxTransfers);
    }
}

void Router::clearRoutes()
{
    this->beginResetModel();
    m_routes.clear();
    // clear journey here
    this->endResetModel();
}

void Router::abortCurrentOperation()
{
    if(this->isBusy()) {
        qDebug() << "Abort Planner";
        m_planner->abortCurrentOperation();
        m_planner->unwatchAll();
    }
}

void Router::handleStream(QRail::RouterEngine::Route *route)
{
    qDebug() << "***************** CSA STREAM ********************";
    qDebug() << "Inserting:" << route->departureTime() << "|" << route->arrivalTime();
    this->setBusy(true);

    QDateTime newEntryDepartureTime = route->departureTime();
    for (qint16 i = 0; i < m_routes.length(); i++) {
        QDateTime entryDepartureTime = m_routes.at(i)->departureTime();

        // Remove duplicates (updates)
        if((m_routes.at(i)->departureTime().addSecs(-m_routes.at(i)->departureDelay()) == route->departureTime().addSecs(-route->departureDelay()))
            && (m_routes.at(i)->arrivalTime().addSecs(-m_routes.at(i)->arrivalDelay()) == route->arrivalTime().addSecs(-route->arrivalDelay()))) {
            qDebug() << "FOUND ROUTE! CHECKING DELAYS";
            qDebug() << "CHECK ROUTE:"
                     << "DEPARTURE:" << m_routes.at(i)->departureTime().toString(Qt::ISODate) << "+" << m_routes.at(i)->departureDelay() << "vs" << route->departureTime().toString(Qt::ISODate) << "+" << route->departureDelay()
                     << "ARRIVAL:" << m_routes.at(i)->arrivalTime().toString(Qt::ISODate) << "+" << m_routes.at(i)->arrivalDelay() << "vs" << route->arrivalTime().toString(Qt::ISODate) << "+" << route->arrivalDelay();

            foreach(QRail::RouterEngine::Transfer *transfer, route->transfers()) {
                if (transfer->type() == QRail::RouterEngine::Transfer::Type::TRANSFER) {
                    qDebug() << "TRANSFER:"
                             << "Changing vehicle at"
                             << transfer->time().time().toString("hh:mm")
                             << transfer->station()->name().value(QLocale::Language::Dutch)
                             << transfer->arrivalLeg()->vehicleInformation()->uri()
                             << transfer->departureLeg()->vehicleInformation()->uri();
                } else if (transfer->type() == QRail::RouterEngine::Transfer::Type::DEPARTURE) {
                    qDebug() << "DEPARTURE:"
                             << transfer->time().time().toString("hh:mm")
                             << transfer->station()->name().value(QLocale::Language::Dutch)
                             << transfer->departureLeg()->vehicleInformation()->uri();
                } else if (transfer->type() == QRail::RouterEngine::Transfer::Type::ARRIVAL) {
                    qDebug() << "ARRIVAL:"
                             << transfer->time().time().toString("hh:mm")
                             << transfer->station()->name().value(QLocale::Language::Dutch)
                             << transfer->arrivalLeg()->vehicleInformation()->uri();
                }
            }

            if(m_routes.at(i)->departureDelay() != route->departureDelay() || m_routes.at(i)->arrivalDelay() != route->arrivalDelay()) {
                qDebug() << "ROUTE AFFECTED, REPLACING...";

                // Remove old entry
                this->beginRemoveRows(QModelIndex(), i, i);
                m_routes.removeAt(i);
                this->endRemoveRows();

                // Insert new entry
                this->beginInsertRows(QModelIndex(), i, i);
                m_routes.insert(i, route);
                this->endInsertRows();

                // Notify user
                SailfishOS::createNotification("Route updated!",
                                               "Route from " + route->departureStation()->departure()->station()->name().value(QLocale::Language::Dutch)
                                               + " (" + route->departureTime().toLocalTime().toString("hh:mm") + ") to "
                                               + route->arrivalStation()->arrival()->station()->name().value(QLocale::Language::Dutch)
                                               + " (" + route->arrivalTime().toLocalTime().toString("hh:mm") + ") has been updated.",
                                               "social",
                                               "lcrail-liveboard-update");
            }

            return;
        }

        // TO DO: Smarter inserting: Departure and arrival time are now the same, so this works for now
        if (entryDepartureTime > newEntryDepartureTime) {
            this->beginInsertRows(QModelIndex(), i, i);
            m_routes.insert(i, route);
            this->endInsertRows();
            return;
        }
    }

    // Entry should be added in front or at the end of the list (if not found above)
    this->beginInsertRows(QModelIndex(), m_routes.length(), m_routes.length());
    m_routes.append(route);
    this->endInsertRows();
}

void Router::handleFinished(QRail::RouterEngine::Journey *journey)
{
    m_planner->unwatchAll();
    m_planner->watch(journey);
    qDebug() << "Finished routing";
    m_after = QDateTime::currentMSecsSinceEpoch();
    qDebug() << "AFTER:" << m_after;
    qDebug() << "BEFORE:" << m_before;
    emit this->benchmark(m_after - m_before);
    this->setBusy(false);
}

void Router::handleProcessing(const QUrl &uri)
{
    // Task started or running
    QUrlQuery query = QUrlQuery(uri);
    QDateTime timestamp = QDateTime::fromString(query.queryItemValue("departureTime"), Qt::ISODate);
    emit this->processing(uri.toString(), timestamp);
}

void Router::updateReceived(qint64 time)
{
    this->setBusy(true);
    m_before = time;
}

// Getters & Setters
bool Router::isBusy() const
{
    return m_busy;
}

void Router::setBusy(const bool &busy)
{
    if(m_busy != busy) {
        m_busy = busy;
        emit this->busyChanged();
    }
}
