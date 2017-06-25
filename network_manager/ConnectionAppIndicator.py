'''
Created on 12 May 2012

@author: ernest
'''
import subprocess
import sys

from network_manager import NetworkManagerWindow

from gi.repository import GObject, Gtk # pylint: disable=E0611

from gi.repository import AppIndicator3 as AppIndicator



class ConnectionAppIndicator():
    '''
    classdocs
    '''

    def check_connection(self):
        interface = "wlan0"
        status = "down"
        try:
                result = subprocess.check_output('ip addr | grep "' + interface + '"', stderr=subprocess.STDOUT, shell=True)
                if(interface == "wlan0"):
                    if(result.find('state UP') > 0):
                        status = "up"
                else:
                    status = "up" 
        except Exception: 
                pass
         
        self.update_icon(status)
        return True

            
            
    def __init__(self):
        self.ind = AppIndicator.Indicator.new("Connection Manager", "", AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_icon_theme_path("/home/ernest")
        self.ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)

        self.menu_setup()
        self.ind.set_menu(self.menu)
        GObject.timeout_add (1000, self.check_connection)

    
    def menuitem_view_stats(self, widget):
        subprocess.check_output('vnstat -i wlan0 --dumpdb > /home/ernest/dump', stderr=subprocess.STDOUT, shell=True)
        window = NetworkManagerWindow.NetworkManagerWindow()
        window.show()
        
    def menu_setup(self):
        self.menu = Gtk.Menu()
        self.view_stats_item = Gtk.MenuItem("View stats")
        self.view_stats_item.connect("activate", self.menuitem_view_stats)
        self.view_stats_item.show()
        self.menu.append(self.view_stats_item)
 
        self.quit_item = Gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)        
        self.quit_item.show()
        self.menu.append(self.quit_item)
     
     
    def update_icon(self, status):
        if status == "down":
            self.ind.set_icon("app-icon-red")
        else:
            self.ind.set_icon("app-icon")
            
            
    def quit(self, widget):
        sys.exit(0)
        
    def main(self):
        Gtk.main()         

if __name__ == "__main__":
    indicator = ConnectionAppIndicator()
    indicator.main()
