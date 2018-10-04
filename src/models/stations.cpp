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
#include "stations.h"

Stations::Stations(QObject *parent) : QAbstractListModel(parent)
{
    m_factory = QRail::StationEngine::Factory::getInstance();
    m_busy = false;
}

int Stations::rowCount(const QModelIndex &) const
{
    return m_results.count();
}

QVariant Stations::data(const QModelIndex &index, int role) const
{
    if (!index.isValid()) {
        return QVariant();
    }
    // Break not needed since return makes the rest unreachable.
    switch (role) {
    case URIRole:
        return QVariant(m_results.at(index.row())->uri());
    case NameRole:
        return QVariant(m_results.at(index.row())->name().value(
                            QLocale::Dutch)); // TO DO localize using QLocale::system().language
    default:
        return QVariant();
    }
}

void Stations::searchByName(const QString &name)
{
    // TO DO: Smarter inserting algorithm, even better: search tree
    this->setBusy(true);
    this->clearSearch();
    if (name.length() > 0) {
        QList<QRail::StationEngine::Station *> stations =  m_factory->getStationsByName(name);
        foreach (QRail::StationEngine::Station *s, stations) {
            this->beginInsertRows(QModelIndex(), m_results.length(), m_results.length());
            m_results.append(s);
            this->endInsertRows();
        }
    }
    this->setBusy(false);
}

void Stations::clearSearch()
{
    this->beginResetModel();
    m_results.clear();
    this->endResetModel();
}

QHash<int, QByteArray> Stations::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[URIRole] = "URI";
    roles[NameRole] = "name";
    return roles;
}

// Getters & Setters
bool Stations::busy() const
{
    return m_busy;
}

void Stations::setBusy(bool busy)
{
    if (m_busy != busy) {
        m_busy = busy;
        emit this->busyChanged();
    }
}
