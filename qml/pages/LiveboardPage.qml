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
import "../UC"
import "../components"
import "../components/liveboard"
import Sailfish.Silica 1.0 // Needs porting to UC
import LCRail.Views.Liveboard 1.0

Page {
    property date _before
    property date _after
    property string _stationURI
    property string _stationName

    // For performance reasons we wait until the Page is fully loaded before doing an API request
    onStatusChanged: status === PageStatus.Active? getData(): undefined

    function getData() {
        _before = new Date();
        if(_stationURI.indexOf("http://irail.be/stations/NMBS/") !== -1) { // QRail should validate the URI itself TO DO
            header.title = "Loading ...";
            liveboard.clearBoard();
            liveboard.getBoard(_stationURI);
        }
    }

    LiveboardHeader {
        id: header
        anchors {
            left: parent.left;
            right: parent.right
        }
        opacity: 0.9
        onSelectStation: {
            var _page = pageStack.push(Qt.resolvedUrl("StationSelectorPage.qml"));
            _page.selected.connect(function(uri, name) {
                _stationURI = uri
                _stationName = name
                // Page is automatically updated due statusChanged
            });
        }
    }

    PlatformListView {
        id: entriesList
        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        clip: true // Paint only within defined borders
        delegate: LiveboardDelegate {
            width: ListView.view.width
            scheduledTime: model.departureTime
            delay: model.departureDelay
            hasDelay: model.hasDelay
            platform: model.platform
            isPlatformNormal: model.isPlatformNormal
            headsign: model.headsign
            vehicleID: model.URI.split("/")[4] // Only ID
        }
        ListView.onAdd: FadeAnimation {}
        ListView.onRemove: FadeAnimation {}

        model: Liveboard {
            id: liveboard
            onBusyChanged: {
                if(!busy) {
                    _after = new Date();
                    header.benchmark = _after.getTime() - _before.getTime() + " ms";
                    header.title = _stationName;
                }
            }
            onProcessing: header.benchmark = timestamp.toLocaleString(Qt.locale(), "HH:mm dd/MM/yyyy")
        }

        VerticalScrollDecorator {}
    }
}
