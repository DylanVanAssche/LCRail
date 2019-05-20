# LCRail

LCRail is a Linked Connections client written in Qt 5 and Silica QML.

## Features

- **Stop search**: Search for your favorite stop in 4 different languages (Dutch, English, French and German).
- **Liveboard**: Show all the departing vehicle of a stop, directly streamed to your device.
- **Journey**: Plan your journey between 2 stops. The routes are streamed to your device.
- **Recalculating**: Never refresh your view! LCRail automatically updates and reroute your journey or liveboard.
- **Notifications**: Changes to your liveboard or journey? LCRail will notify you with a notification.

## Build instructions

In order to run LCRail you need to have a Sailfish OS device or use the Sailfish Emulator from the Sailfish IDE.
You can find the Sailfish IDE on [https://sailfishos.org/wiki/Application_Development](https://sailfishos.org/wiki/Application_Development)
You must have set up a device (with developer mode enabled) if you want to deploy it to a physical Sailfish OS device.

1. Open the `harbour-lcrail.pro` in the Sailfish IDE.
2. Check if the kit (`SailfishOS-3.0.2.8-armv7hl` for the Sony Xperia X), build mode (`debug` is fine) and that the deployment device (`Xperia X (ARM)` for the Sony Xperia X) are correct.
3. Open the `QRail/qrail.pro` file in the Sailfish IDE. The IDE will switch automatically to this project.
4. Switch the `deploy` mode to `Deploy as RPM package` in the Sailfish IDE.
5. Build QRail by clicking on the hammer build button.
6. Set the active project back to LCRail.
7. Switch the `deploy` mode to `Deploy as RPM package` in the Sailfish IDE.
9. Deploy LCRail by clicking on the run (green arrow) button.
