# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import re
import gettext
from gettext import gettext as _
gettext.textdomain('network-manager')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('network_manager')

from network_manager_lib import Window
from network_manager.AboutNetworkManagerDialog import AboutNetworkManagerDialog
from network_manager.PreferencesNetworkManagerDialog import PreferencesNetworkManagerDialog

# See network_manager_lib.Window.py for more details about how this class works
class NetworkManagerWindow(Window):
    __gtype_name__ = "NetworkManagerWindow"
    
    def read_file(self):
        while True:
                try:
                    openfile = open('/home/ernest/dump', "r")
                    break
                except:
                    pass
           #    print "Invalid file.  Please enter a correct file."
        summary = {}
        days={}
        months={}
        #package everything
        for line in openfile:
                str = re.split(';',line)
                if(str[0] == 'interface'):
                      summary['interface'] = str[1]
                if(str[0] == 'totalrx'):
                      summary['totalrx'] = str[1]
                if(str[0] == 'totaltx'):
                      summary['totaltx'] = str[1]
                if(str[0] == 'created'):
                      summary['created'] = str[1]
                if(str[0] == 'updated'):
                      summary['updated'] = str[1]
                if(str[0] == 'd'):
                      days[str[1]]={'date':str[2],'rx':str[3],'tx':str[4],'rx_kb':str[5],'tx_kb':str[6]}
                if(str[0] == 'm'):  
                	  months[str[1]]={'date':str[2],'rx':str[3],'tx':str[4],'rx_kb':str[5],'tx_kb':str[6]}
                	                  	  
        summary['days'] = days
		summary['months'] = months
        openfile.close()
        return summary
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(NetworkManagerWindow, self).finish_initializing(builder)
 
        # Code for other initialization actions should be added here.
        summary = self.read_file()
        self.AboutDialog = AboutNetworkManagerDialog
        self.PreferencesDialog = PreferencesNetworkManagerDialog
        self.ui.downloaded_label.set_text(summary['totalrx'])
        self.ui.sent_label.set_text(summary['totaltx'])
        self.ui.recorded_date.set_text(summary['created'])
        self.ui.last_updated_date.set_text(summary['updated'])
        
      #  days = summary['days']

       # for day,value in days.iteritems():
        #	print(value['date'])        	
           #  print(day[2])
             
      
