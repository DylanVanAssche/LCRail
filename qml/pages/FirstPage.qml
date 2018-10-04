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
    PlatformFlickable {
        anchors.fill: parent
        contentHeight: column.height

        Column {
            id: column
            width: parent.width
            spacing: 50 // Use proper Theme object, needs implementation in UC TO DO

            PageHeader {
                title: "LCRail"
                menu: Menu {}
            }

            Label {
                text: "Select benchmark"
            }

            Button {
                onClicked: {
                    var _page = pageStack.push(Qt.resolvedUrl("StationSelectorPage.qml"));
                    _page.selected.connect(function(uri, name) {
                        console.log(uri)
                        console.log(name)
                        //getData()
                    });
                }
            }
        }
    }
}
