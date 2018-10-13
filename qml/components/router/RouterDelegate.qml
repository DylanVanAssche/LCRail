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
import "../../components"
import "../../js/utils.js" as Utils

ListItem {
    property var trip

    contentHeight: connectionList.height + 2*Theme.paddingMedium
    enabled: false

    SilicaListView {
        id: connectionList
        anchors{
            verticalCenter: parent.verticalCenter
        }
        width: parent.width
        height: contentHeight // Follow delegate size
        model: trip
        spacing: connectionList.count == 2? Theme.paddingSmall: 0 // No transfers? add some spacing
        delegate: Loader {
            id: loader
            height: childrenRect.height
            sourceComponent: switch(index){
                             case 0: // departure station
                                 return departureStationIndicator;

                             case connectionList.count-1: // arrival station
                                 return arrivalStationIndicator;

                             default: // transfer station
                                 return transferStationIndicator;
                             }
            onLoaded: {
                //loader.item.width = ListView.view.width
                loader.item.time = model.time
                loader.item.delay = model.delay
                loader.item.station = model.station
                loader.item.platform = "?"
                loader.item.isNormalPlatform = true
                loader.item.vehicleID = model.vehicleURI
                loader.item.vehicleHeadsign = model.vehicleHeadsign
            }
        }

        // Departure station
        Component {
            id: departureStationIndicator
            RouterStationIndicator {
                color: green
            }
        }

        // Arrival station
        Component {
            id: arrivalStationIndicator
            RouterStationIndicator {
                color: red
            }
        }

        // Transfer station
        Component {
            id: transferStationIndicator
            RouterTransferIndicator {}
        }
    }
}
