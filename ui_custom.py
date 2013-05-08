from PyQt4 import QtCore, QtGui
class QuadStreakerPushButton( QtGui.QPushButton ):

        #   
        #  SIGNALS
        #   
        handle_click_event = QtCore.pyqtSignal( dict )

        def __init__( self, cls_name ):
            super( QuadStreakerPushButton, self ).__init__( cls_name )
            self.clicked.connect(  self.clickHandler )
        
        def clickHandler( self ):
            event_name = str(self.objectName()).replace( 'btn', '' )
            self.handle_click_event.emit( { 'event' : event_name } )

