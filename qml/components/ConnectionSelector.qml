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
import "../UC"

Column {
    width: parent.width
    spacing: Theme.paddingLarge

    property string _fromURI
    property string _fromName: "From"
    property string _toURI
    property string _toName: "To"

    signal selected(string fromURI, string toURI)

    Row {
        width: parent.width

        Column {
            id: selectors
            width: parent.width*(2/3)

            BackgroundRectangle {
                width: parent.width

                Label {
                    anchors.centerIn: parent
                    text: _fromName
                }
                onClicked: {
                    var _page = pageStack.push(Qt.resolvedUrl("../pages/StationSelectorPage.qml"));
                    _page.selected.connect(function(uri, name) {
                        _fromURI = uri
                        _fromName = name
                    });
                }
            }

            BackgroundRectangle {
                width: parent.width

                Label {
                    anchors.centerIn: parent
                    text: _toName
                }
                onClicked: {
                    var _page = pageStack.push(Qt.resolvedUrl("../pages/StationSelectorPage.qml"));
                    _page.selected.connect(function(uri, name) {
                        _toURI = uri
                        _toName = name
                    });
                }
            }
        }

        BackgroundRectangle {
            width: parent.width/3
            height: selectors.height

            Label {
                anchors.centerIn: parent
                text: "SWITCH"
            }
            onClicked: {
                var uri = _fromURI;
                _fromURI = _toURI;
                _toURI = uri;

                var name = _fromName;
                _fromName = _toName;
                _toName = name;
            }
        }
    }

    Button {
        anchors {
            horizontalCenter: parent.horizontalCenter
        }
        enabled: _fromURI.length > 0 && _toURI.length > 0
        text: "Plan!"
        onClicked: selected(_fromURI, _toURI)
    }
}
