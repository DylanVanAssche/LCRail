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
        onBoardChanged: {
            entriesList.model = liveboard
            entriesList.visible = true
        }
        onBusyChanged: {
            if(!busy) {
                after = new Date();
                progressText.text = "Finished in: " + (after.getTime() - before.getTime()) + "ms" // Ugly benchmark, use something better please! -> QElapsedTimer
            }
            console.debug("Busy?" + busy)
        }
        onProgressUpdated: progressText.text = "Page=" + uri.toString().replace("https://graph.irail.be/sncb/connections?departureTime=", "");
    }

    PlatformFlickable {
        anchors.fill: parent
        contentHeight: column.height

        Column {
            id: column
            width: parent.width
            spacing: 50 // Use proper Theme object, needs implementation in UC TO DO

            PageHeader {
                title: "LCRail"
                menu: Menu {
                    busy: liveboard.busy
                }
            }

            Row {
                spacing: 25
                anchors.horizontalCenter: parent.horizontalCenter

                Label {
                    id: progressText
                }

                Rectangle {
                    width: 100
                    height: 100
                    radius: parent.width/2
                    color: liveboard.busy? "red": "green"
                    opacity: 0.75
                }
            }

            Button {
                id: getButton
                anchors.horizontalCenter: parent.horizontalCenter
                text: "GET liveboard"
                onClicked: {
                    before = new Date();
                    entriesList.visible = false;
                    liveboard.getBoard("http://irail.be/stations/NMBS/008811189"); // Vilvoorde
                }
            }

            PlatformListView {
                id: entriesList
                width: parent.width
                height: 1100 // Ugly
                clip: true // Only paint within it's borders
                delegate: Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: model.headsign + " " + model.departureTime.toTimeString() // QDateTime is automatically converted, see https://doc.qt.io/qt-5/qtqml-cppintegration-data.html
                }

                VerticalScrollDecorator {}
            }

            //ConnectionSelector {}
        }
    }
}
