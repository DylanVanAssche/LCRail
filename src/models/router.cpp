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
    switch (role) {
    case tripRole:
        return QVariant::fromValue(new Trip(m_routes.at(index.row())->transfers()));
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
        this->clearRoutes();
        m_planner->getConnections(QUrl(departureStation),
                                  QUrl(arrivalStation),
                                  departureTime,
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
    }
}

void Router::handleStream(QRail::RouterEngine::Route *route)
{
    qDebug() << "Inserting:" << route->departureTime() << "|" << route->arrivalTime();
    bool foundInsertIndex = false;

    QDateTime newEntryDepartureTime = route->departureTime();
    for (qint16 i = 0; i < m_routes.length(); i++) {
        QDateTime entryDepartureTime = m_routes.at(i)->departureTime();

        // TO DO: Smarter inserting: Departure and arrival time are now the same, so this works for now
        if (entryDepartureTime > newEntryDepartureTime) {
            this->beginInsertRows(QModelIndex(), i, i);
            m_routes.insert(i, route);
            this->endInsertRows();
            foundInsertIndex = true;
            break;
        }
    }

    // Entry should be added in front or at the end of the list
    if (!foundInsertIndex) {
        this->beginInsertRows(QModelIndex(), m_routes.length(), m_routes.length());
        m_routes.append(route);
        this->endInsertRows();
    }
}

void Router::handleFinished(QRail::RouterEngine::Journey *journey)
{
    Q_UNUSED(journey->routes());
    qDebug() << "Finished routing";
    this->setBusy(false);
}

void Router::handleProcessing(const QUrl &uri)
{
    // Task started or running
    QUrlQuery query = QUrlQuery(uri);
    QDateTime timestamp = QDateTime::fromString(query.queryItemValue("departureTime"), Qt::ISODate);
    emit this->processing(uri.toString(), timestamp);
}

// Getters & Setters
bool Router::isBusy() const
{
    return m_busy;
}

void Router::setBusy(const bool &busy)
{
    m_busy = busy;
    emit this->busyChanged();
}
