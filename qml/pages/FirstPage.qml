import "../UC"

Page {
    PlatformFlickable {
        anchors.fill: parent
        PageHeader {
            anchors.top : parent.top
            menu : TopMenu {
                MenuItem {
                    text : "About"
                    onClicked : {
                        console.log("About clicked!")
                    }
                }
            }
        }
    }
}
