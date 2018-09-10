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
import LCRail.Views.Liveboard 1.0

Page {
    property date before
    property date after

    Liveboard {
        id: liveboard
        onBoardChanged: console.debug("Liveboard received in QML");
        onBusyChanged: {
            if(!busy) {
                after = new Date();
                console.debug("Bad benchmark: " + (after.getTime() - before.getTime()) + "ms")
            }

            console.debug("Busy?" + busy)
        }
        onProgressUpdated: progressText.text = uri.toString().replace("https://graph.irail.be/sncb/connections?departureTime=", "");
    }

    PlatformFlickable {
        anchors.fill: parent
        contentHeight: column.height

        Column {
            id: column
            width: parent.width

            PageHeader {
                title: "LCRail"
                menu: Menu {
                    busy: liveboard.busy
                }
            }

            Label {
                id: progressText
            }

            Rectangle {
                anchors.horizontalCenter: parent.horizontalCenter
                width: 100
                height: 100
                radius: parent.width/2
                color: liveboard.busy? "red": "green"
                opacity: 0.75
            }

            Button {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "GET liveboard"
                onClicked: {
                    before = new Date();
                    liveboard.getBoard("http://irail.be/stations/NMBS/008814332");
                }
            }

            ConnectionSelector {}
        }
    }
}
