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
import "../../js/utils.js" as Utils

ListItem {
    property date time
    property int delay
    property string color
    property string station
    property string platform
    property bool isNormalPlatform
    property string vehicleID
    property string vehicleHeadsign

    id: indicator
    width: parent.width
    height: row.height

    Row {
        id: row
        width: parent.width
        anchors {
            left: parent.left
            leftMargin: Theme.horizontalPageMargin
            right: parent.right
            rightMargin: Theme.horizontalPageMargin
        }
        spacing: Theme.paddingLarge

        Rectangle {
            id: timeIndicator
            width: Theme.itemSizeMedium
            height: Theme.itemSizeSmall
            radius: Theme.itemSizeSmall/5
            anchors { verticalCenter: parent.verticalCenter }
            color: indicator.color
            Behavior on height { NumberAnimation { duration: 750 } }
            Behavior on width { NumberAnimation { duration: 750 } }

            Label {
                id: timeLabel
                anchors {
                    centerIn: indicator.delay > 0? undefined: parent;
                    top: indicator.delay > 0? parent.top: undefined;
                    topMargin: Theme.paddingSmall;
                    horizontalCenter: indicator.delay > 0? parent.horizontalCenter: undefined
                }
                font.bold: true
                text: indicator.time.toLocaleTimeString(Qt.locale(), "HH:mm")
            }

            Label {
                anchors { top: timeLabel.bottom; horizontalCenter: parent.horizontalCenter }
                text: Utils.formatDelay(indicator.delay)
                visible: indicator.delay > 0
                font.pixelSize: Theme.fontSizeTiny
                font.bold: true
            }
        }

        Column {
            id: stationInfo
            width: parent.width - timeIndicator.width - vehicleInformation.width - 2*parent.spacing

            Label {
                anchors { left: parent.left; right: parent.right }
                truncationMode: TruncationMode.Fade
                font.capitalization: Font.AllUppercase
                font.bold: true
                text: indicator.station
            }

            Label {
                font.pixelSize: Theme.fontSizeExtraSmall
                //: The platform where the train arrives or departures
                //% "Platform %0"
                text: "Platform %0".arg(indicator.platform) //qsTrId("berail-trip-platform").arg(indicator.platform)

                Rectangle {
                    // Make the Rectangle a little bit bigger then the platform number
                    anchors.centerIn: parent
                    width: parent.width*1.2
                    height: parent.height*1.05
                    radius: parent.width/4
                    opacity: Theme.highlightBackgroundOpacity
                    color: indicator.isNormalPlatform? transparent: yellow
                }
            }
        }

        Column {
            id: vehicleInformation
            width: Math.max(vehicleInformationID.width, vehicleInformationHeadsign.width)

            Label {
                anchors.right: parent.right
                id: vehicleInformationID
                text: Utils.filterId(vehicleID)
                font.pixelSize: Theme.fontSizeSmall
            }

            Label {
                anchors.right: parent.right
                id: vehicleInformationHeadsign
                text: vehicleHeadsign
                font.pixelSize: Theme.fontSizeExtraSmall
            }
        }
    }
}
