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
import "../components"
import "../components/station"
import LCRail.Views.Stations 1.0

Page {
    property string _searchString
    signal selected(string uri, string name)

    id: searchPage
    // For performance reasons we wait until a search request has been performed before doing an API request
    on_SearchStringChanged: getData()

    function getData() {
        search.searchByName(_searchString);
    }

    SilicaFlickable {
        anchors.fill: parent

        // When set as header of the SilicaListView focus is lost almost on every keystroke
        StationSelectorHeader {
            id: header
            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
            }
            onSearchStringChanged: _searchString = header.searchString
            busy: search.busy
        }

        SilicaListView {
            id: stationListView
            anchors {
                top: header.bottom
                bottom: parent.bottom
                left: parent.left
                right: parent.right
            }
            clip: true // Only paint within it's borders
            Behavior on opacity { FadeAnimator {} }
            delegate: StationSelectorDelegate {
                id: delegate
                width: ListView.view.width
                searchString: _searchString
                onClicked: {
                    searchPage.selected(model.URI, model.name)
                    console.debug("Station selected: " + model.name + " (" + model.URI + ")")
                    pageStack.pop()
                }
            }
            model: StationsSearch {
                id: search
            }

            VerticalScrollDecorator {}
        }
    }
}
