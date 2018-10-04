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
#ifndef STATIONS_H
#define STATIONS_H

#include <QtCore/QAbstractListModel>
#include <QtCore/QList>

#include "engines/station/stationfactory.h"

class Stations : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(bool busy READ busy WRITE setBusy NOTIFY busyChanged)

public:
    enum Roles {
        URIRole = Qt::UserRole + 1,
        NameRole = Qt::UserRole + 2
    };
    explicit Stations(QObject *parent = nullptr);

    virtual int rowCount(const QModelIndex &) const;
    virtual QVariant data(const QModelIndex &index, int role) const;
    Q_INVOKABLE void searchByName(const QString &name);
    Q_INVOKABLE void clearSearch();
    bool busy() const;

signals:
    void stationsUpdated();
    void busyChanged();

protected:
    QHash<int, QByteArray> roleNames() const;

private:
    QList<QRail::StationEngine::Station *> m_results;
    QRail::StationEngine::Factory *m_factory;
    bool m_busy;
    void setBusy(bool busy);
};

#endif // STATIONS_H
