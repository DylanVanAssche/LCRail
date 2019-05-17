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

Rectangle {
    //: Liveboard title
    //% "Liveboard"
    //~ A list of all departing/arriving trains in a station.
    property string title
    property string benchmark
    property date _currentTime: new Date()
    signal timeUpdate(date currentTime)
    signal selectStation()

    color: blue
    width: parent.width
    height: Theme.itemSizeHuge

    Timer {
        running: Qt.application.active
        interval: 503 // Prime number will improve update
        repeat: true
        onTriggered: {
            _currentTime = new Date()
            timeUpdate(_currentTime)
        }
    }

    Label {
        width: parent.width
        anchors {
            left: parent.left;
            right: parent.right
            top: parent.top
            topMargin: Theme.paddingLarge
            leftMargin: Theme.horizontalPageMargin
            rightMargin: Theme.horizontalPageMargin
        }
        font.pixelSize: Theme.fontSizeExtraLarge
        font.bold: true
        truncationMode: TruncationMode.Fade
        horizontalAlignment: Text.AlignHCenter
        text: title
    }

    Label {
        anchors { left: parent.left; leftMargin: Theme.horizontalPageMargin; bottom: parent.bottom; bottomMargin: Theme.paddingLarge }
        font.bold: true
        truncationMode: TruncationMode.Fade
        horizontalAlignment: Text.AlignLeft
        text: _currentTime.toLocaleTimeString(Qt.locale(), "HH:mm:ss")
    }

    Label {
        anchors { right: parent.right; rightMargin: Theme.horizontalPageMargin; bottom: parent.bottom; bottomMargin: Theme.paddingLarge }
        font.bold: true
        truncationMode: TruncationMode.Fade
        horizontalAlignment: Text.AlignLeft
        visible: benchmark.length >= 0
        text: benchmark
    }

    BackgroundItem {
        anchors.fill: parent
        onClicked: selectStation()
    }
}
