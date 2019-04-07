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

function formatTime(timeInSeconds) {
    var minutes = timeInSeconds/60; // Convert to minutes
    var hours = Math.floor(minutes/60); // Convert to hours
    minutes = minutes - hours*60 // Remove the converted hours

    if(minutes < 10) { // Add leading zero if needed
        minutes = "0" + Math.round(minutes);
    }

    return hours + "H" + minutes;
}

function formatDelay(delayInSeconds) {
    return "+" + formatTime(delayInSeconds);
}

function mergeTimeDelay(time, delayInSeconds) {
    return new Date(time.getTime() + delayInSeconds*1000)
}

function filterId(id) {
    var filterRegex = /^(S[0-9]{4})|(ICE[0-9]{4})|(THA[0-9]{4})|(IC[0-9]{3,4})|(EUR[0-9]{4})|(TGV[0-9]{4})|(P[0-9]{3,4})|(L[0-9]{3,4})|(EXTRA[0-9]{5})|(BUS[0-9]{5})/;
    return filterRegex.exec(id)[0];
}
