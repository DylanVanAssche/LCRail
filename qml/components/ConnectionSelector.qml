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

Column {
    width: parent.width

    Row {
        width: parent.width

        Column {
            id: selectors
            width: parent.width*(2/3)

            BackgroundRectangle {
                width: parent.width

                Label {
                    anchors.centerIn: parent
                    text: "From"
                }
            }

            BackgroundRectangle {
                width: parent.width

                Label {
                    anchors.centerIn: parent
                    text: "To"
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
        }
    }
}
