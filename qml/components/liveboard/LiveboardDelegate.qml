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
//import "../../UC" // Needs porting to UC

import QtQuick 2.0
import Sailfish.Silica 1.0
import "../../js/utils.js" as Utils

ListItem {
    property date scheduledTime
    property int delay
    property bool hasDelay
    property string platform
    property bool isPlatformNormal
    property string headsign
    property string vehicleID

    Label {
        id: time
        anchors {
            left: parent.left
            leftMargin: Theme.horizontalPageMargin
            verticalCenter: parent.verticalCenter
        }
        truncationMode: TruncationMode.Fade
        font.bold: true
        color: yellow
        text: scheduledTime.toLocaleTimeString(Qt.locale(), "HH:mm")
    }

    Label {
        id: delayIndicator
        anchors {
            right: parent.right
            rightMargin: Theme.horizontalPageMargin
            verticalCenter: parent.verticalCenter
        }
        truncationMode: TruncationMode.Fade
        font.bold: true
        color: red
        opacity: delay > 0? 1.0: 0.0 // Make text invisible when delay == 0
        Behavior on opacity { FadeAnimator {} }
        visible: hasDelay // Only visible when model hasDelay
        text: Utils.formatDelay(delay)
    }

    Rectangle {
        id: platformIndicator
        // Anchor to the right element depending on if the model hasDelay or not
        anchors {
            right: hasDelay? delayIndicator.left: parent.right
            rightMargin: hasDelay? Theme.paddingLarge: Theme.horizontalPageMargin
        }
        width: parent.height
        height: parent.height
        color: isPlatformNormal? transparent: yellow

        Label {
            anchors { centerIn: parent }
            truncationMode: TruncationMode.Fade
            font.bold: true
            color: isPlatformNormal? yellow: black
            text: platform
        }
    }

    Label {
        id: type
        anchors {
            right: platformIndicator.left
            rightMargin: Theme.paddingLarge
            verticalCenter: parent.verticalCenter
        }
        truncationMode: TruncationMode.Fade
        font.bold: true
        color: yellow
        text: Utils.filterId(vehicleID)
    }

    Label {
        // Scale the direction label depending on all the other labels
        anchors {
            left: time.right
            leftMargin: Theme.paddingLarge
            right: type.left
            rightMargin: Theme.paddingLarge
            verticalCenter: parent.verticalCenter
        }
        truncationMode: TruncationMode.Fade
        font.bold: true
        color: yellow
        text: headsign
    }

    Rectangle {
        id: background
        z: -1 // Make ListItem highlight visible
        color: index%2? black: grey
        anchors { fill: parent }
    }
}
