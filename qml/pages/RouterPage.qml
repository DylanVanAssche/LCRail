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

import QtQuick 2.2
import Sailfish.Silica 1.0
import LCRail.Views.Router 1.0
import "../components/router"
import "../js/utils.js" as Utils

Page {
    property string from
    property string to
    property date departureTime: new Date()
    property int maxTransfers: 4

    property date _before
    property date _after

    // For performance reasons we wait until the Page is fully loaded before doing an API request
    onStatusChanged: {
        if(status === PageStatus.Active) {
            getData()
        }
        else if(status === PageStatus.Deactivating && router.busy) {
            router.abortCurrentOperation()
            console.warn("Routing operation aborted")
        }
    }

    function getData() {
        console.log("Fetching connections")
        _before = new Date();
        if(from.length > 0 && to.length > 0) {
            router.getConnections(from, to, departureTime, maxTransfers);
        }
        else {
            console.error("From and To stations not found");
        }
    }

    SilicaFlickable {
        anchors.fill: parent
        contentHeight: column.height

        Column {
            id: column
            width: parent.width

            PageHeader {
                id: header
                title: "Planner"
            }

            SilicaListView {
                id: connectionsListView
                width: parent.width
                height: contentHeight
                delegate: RouterDelegate {
                    width: ListView.view.width
                    trip: model.trip
                }
                spacing: Theme.paddingLarge
                model: Router {
                    id: router
                    onBusyChanged: {
                        if(!busy) {
                            _after = new Date();
                            header.description = _after.getTime() - _before.getTime() + " ms";
                        }
                    }
                    onProcessing: header.description = timestamp.toLocaleString(Qt.locale(), "HH:mm dd/MM/yyyy")
                }
                VerticalScrollDecorator {}
            }
        }
    }
}
