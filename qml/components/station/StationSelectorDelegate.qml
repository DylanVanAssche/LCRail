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

ListItem {
    property string searchString

    id: stationItem

    ListView.onAdd: AddAnimation {
        target: stationItem
    }

    ListView.onRemove: RemoveAnimation {
        target: stationItem
    }

    Label {
        anchors {
            left: parent.left
            right: parent.right
            leftMargin: Theme.horizontalPageMargin
            rightMargin: Theme.horizontalPageMargin
            verticalCenter: parent.verticalCenter
        }
        color: searchString.length > 0 ? (highlighted ? Theme.secondaryHighlightColor : Theme.secondaryColor)
                                       : (highlighted ? Theme.highlightColor : Theme.primaryColor)
        truncationMode: TruncationMode.Fade
        textFormat: Text.StyledText
        text: Theme.highlightText(model.name, searchString, Theme.highlightColor)
    }
}
