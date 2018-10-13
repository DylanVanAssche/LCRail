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

import QtQuick 2.0
import Sailfish.Silica 1.0
import "../../js/utils.js" as Utils

ListItem {
    property bool isFirstItem: false
    property bool isLastItem: false
    property date time
    property int delay
    property string station
    property string platform
    property bool isNormalPlatform
    property string vehicleID
    property string vehicleHeadsign

    id: indicator
    contentHeight: Theme.itemSizeExtraLarge
    width: parent.width

    Item {
        anchors {
            left: parent.left
            leftMargin: Theme.horizontalPageMargin
            right: parent.right
            rightMargin: Theme.horizontalPageMargin
        }

        Column {
            id: stopIndicator
            anchors {
                left: parent.left
                leftMargin: (Theme.itemSizeMedium-width)/2 // Center in TripStationIndicator Rectangle
            }

            Rectangle {
                width: Theme.iconSizeExtraSmall
                height: indicator.height/2
                // We don't use at the moment the property vehicleArrived since it's buggy on the API side
                // new Date() is required to compare it with the current Date
                color: isFirstItem? transparent: new Date(indicator.time) <= new Date()? Theme.secondaryHighlightColor: Theme.secondaryColor
            }

            Rectangle {
                width: Theme.iconSizeExtraSmall
                height: indicator.height/2
                // We don't use at the moment the property vehicleLeft since it's buggy on the API side
                // new Date() is required to compare it with the current Date
                // Hide this Rectangle when it's the last stop by making it transparant
                color: isLastItem? transparent: new Date(indicator.time) <= new Date()? Theme.secondaryHighlightColor: Theme.secondaryColor
            }
        }

        Rectangle {
            // Creates a darker background to avoid ugly overlaps due the fact that the Theme colors are partly transparent
            width: Theme.iconSizeSmall*1.25 // Theme.iconSizeMedium is too big
            height: Theme.iconSizeSmall*1.25
            anchors.centerIn: stopIndicator
            radius: width/2
            color: black

            Rectangle {
                width: Theme.iconSizeSmall*1.25 // Theme.iconSizeMedium is too big
                height: Theme.iconSizeSmall*1.25
                anchors.centerIn: parent
                radius: width/2
                color: Theme.secondaryColor
            }
        }

        Column {
            id: timeIndicator
            width: Theme.itemSizeSmall // Follow the size of the children
            anchors {
                left: stopIndicator.right
                leftMargin: Theme.paddingLarge
                verticalCenter: stopIndicator.verticalCenter
            }

            Label {
                anchors.horizontalCenter: parent.horizontalCenter
                font.capitalization: Font.SmallCaps
                text: indicator.time.toLocaleTimeString(Qt.locale(), "HH:mm")
            }

            Label {
                anchors.horizontalCenter: parent.horizontalCenter
                font.capitalization: Font.SmallCaps
                font.pixelSize: Theme.fontSizeSmall
                font.bold: true
                visible: indicator.delay > 0
                color: red
                text: Utils.formatDelay(indicator.delay)
            }
        }

        Column {
            anchors {
                left: timeIndicator.right
                leftMargin: Theme.paddingMedium
                right: parent.right
                rightMargin: Theme.horizontalPageMargin
                verticalCenter: stopIndicator.verticalCenter
            }

            Label {
                id: station
                width: parent.width
                truncationMode: TruncationMode.Fade
                font.capitalization: Font.SmallCaps
                font.bold: true
                text: indicator.station
            }

            Label {
                anchors { left: parent.left }
                width: contentWidth
                font.pixelSize: Theme.fontSizeExtraSmall
                truncationMode: TruncationMode.Fade
                text: "Platform %0".arg(indicator.platform)

                Rectangle {
                    // Make the Rectangle a little bit bigger then the time indicator
                    anchors.centerIn: parent
                    width: parent.width*1.1
                    height: parent.height*0.9
                    radius: parent.width/4
                    opacity: Theme.highlightBackgroundOpacity
                    color: indicator.isNormalPlatform? transparent: yellow
                }
            }
        }
    }
}
