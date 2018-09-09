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

import "../UC"

TopMenu {
    MenuItem {
        text: "About"
        onClicked: {
            console.log("About clicked!")
        }
    }

    MenuItem {
        text: "Vehicle"
        onClicked: {
            console.log("Vehicle clicked!")
        }
    }

    MenuItem {
        text: "Liveboard"
        onClicked: {
            console.log("Liveboard clicked!")
        }
    }
}
