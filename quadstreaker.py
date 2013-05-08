# -*- coding: utf-8 -*-
"""
/***************************************************************************
 quadstreaker
                                 A QGIS plugin
 some sticks and stones for quality control
                              -------------------
        begin                : 2013-04-08
        copyright            : (C) 2013 by quadstreaker/pugetworks
        email                : info@pugetworks.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from quadstreakerdialog import quadstreakerDialog, QuadStreakerPushButton

#
#
#  Stored Procedure Errors
#
#
class STORED_PROC( object ):

    ERRORS =  {
        -99 : 'Server Error' ,
        -69 : 'Not Found' ,
        -67 : 'Quad Not Found' ,
        -66 : 'Hood Not Found' ,
        -64 : 'SuperQuad Not Found' ,
        -65 : 'City Not Found' ,
        -63 : 'SuperCity Not Found ' ,
        -62 : 'County Not Found' ,
        -61 : 'State Not Found' ,
        -60 : 'Country Not Found' 
    }

#
#
#  Thread Class Quad/SuperQuad Creation
#
#

class StoredProcWorkerThread( QThread ):
    #
    #  SIGNALS
    #
    finished = pyqtSignal()
    import_error = pyqtSignal( str )
    general_error = pyqtSignal( str )
    log_message = pyqtSignal( str )
    refresh = pyqtSignal()

    def __init__( self, parentThread, vlayer_uri_string, statement, fetch='fetchone' ):
        QThread.__init__( self, parentThread )
        self.statement = statement
        self.vlayer_uri_string = vlayer_uri_string
        self.fetch = fetch

    def run( self ):
        self.running = True
        success = self.doWork()
        self.finished.emit()

    def doWork( self ):
        try:
            import psycopg2
        except ImportError:
            self.import_error.emit( "psycopg2 is not installed" )

        try:
            q_ds = QgsDataSourceURI( self.vlayer_uri_string )
            conn = psycopg2.connect( str( q_ds.connectionInfo() ) )
            crs = conn.cursor()
            self.log_message.emit( "executing [ %s ]" % self.statement )
            crs.execute( self.statement )
            response = None
            if hasattr( crs, self.fetch ):
                response = getattr( crs, self.fetch )()
            else:
                self.log_message.emit( "[ ERROR ]: the cursor object could not find the fetch method = %s" % self.fetch )
            conn.commit()

            #
            # delete the cursor, connection to postgis
            #
            crs.close()
            conn.close()
            del crs, conn

            #
            #
            #  0 response indicates nothing created
            #
            #
            message = ''
            fail = False
            if not response:
                message = '[ ERROR ]: reponse is NONE or NULL...never created'
                fail = True
            elif response[0] >= 0:
                message = 'superquads created = %s' % str( response[0] )
            else:
                message = '[ ERROR ]: createSuperQuad returned = %s' % str( response[0] )
                fail = True
        
            self.log_message.emit( message )
            if fail: 
                reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                return
            self.refresh.emit()
        except Exception, e:
            self.general_error.emit( str(e) )
            return False
        return True

    def stop( self ):
        self.running = False
        pass

    def cleanUp( self):
        pass

        
class quadstreaker:

    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        # refernce to map canvas
        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/quadstreaker"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/quadstreaker_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # create the dialog (after translation) and keep reference
        self.dlg = quadstreakerDialog()

        # the identify tool will emit a QgsPoint on every click
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        # create a list to hold our selected feature ids
        self.selectList = []
        # current layer ref (set in handleLayerChange)
        self.cLayer = None
        # current layer dataProvider ref (set in handleLayerChange)
        self.provider = None
        # database connection
        self.conn = None
        self.crs = None

        #
        #
        #  thread pool
        #
        #
        self.worker_threads = []



    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/quadstreaker/icon.png"),
            u"quadstreaker", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&QuadStreaker QuadQC", self.action)

        #
        # EVENT/SIGNAL handlers
        #
        #
        # connect to the currentLayerChanged signal of QgsInterface
        #
        # (e.g. old way )
        # result = QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.handleLayerChange)
        #
        self.iface.currentLayerChanged.connect( self.handleLayerChange )

        #
        # connect to the btn click signals
        # ** we have to add extra information here because NOTHING gets tranmitted about event to handler **
        #
        for k,v in self.dlg.ui.__dict__.items():
            if isinstance( v, QuadStreakerPushButton ):
                button = getattr( self.dlg.ui, str(v.objectName()), None ) 
                if not button:
                    self.logMessage( "[ ERROR ]: button %s cannot be found" % str( v.objectName() ) )
                    continue
                button.handle_click_event.connect( self.btnDelegateClickHandler )


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&QuadStreaker QuadQC", self.action)
        self.iface.removeToolBarIcon(self.action)

    def getDataSourceProviderType( self, vectorLayer ):
        return str(vectorLayer.dataProvider().name())

    def findLayerByDataSourceTableName( self, vector_layer_name ):
        for lyr in self.canvas.layers():
            if lyr.type() == QgsMapLayer.VectorLayer and self.getDataSourceProviderType( lyr ) == 'postgres':
                uri_string = lyr.dataProvider().dataSourceUri()
                ds = QgsDataSourceURI( uri_string )
                if str( ds.table() ) == vector_layer_name:
                    return lyr
        return None
        
    def getDataSourceTableName( self, vectorLayer ):
        if vectorLayer.type() == QgsMapLayer.VectorLayer and self.getDataSourceProviderType( self.cLayer ) == 'postgres':
            uri_string = vectorLayer.dataProvider().dataSourceUri()
            ds = QgsDataSourceURI( uri_string )
            return str( ds.table() )
        else:
            self.logMessage( "[ ERROR ]: The following layer is NOT a vector laye OR is does not have postgres backend = %s" % str( vectorLayer ) )

    def createProcConnection( self, vlayer_uri_string ):
        try:
            import psycopg2
        except ImportError:
            QMessageBox.critical( self.iface.mainWindow(),"Info", "The module psycopg2 is a dependency for this plugin...please install it" )
        q_ds = QgsDataSourceURI( vlayer_uri_string )
        conn = psycopg2.connect( str( q_ds.connectionInfo() ) )
        return conn

    def setActiveLayer(self, new_layer):
        self.iface.setActiveLayer( new_layer )

    def handleLayerChange(self, layer):

        #
        # clear all layer selections
        #
        self.deselectAll()

        #
        #  update the active layer
        #
        self.cLayer = self.canvas.currentLayer()
        if self.cLayer and self.cLayer.type() == QgsMapLayer.VectorLayer:
            self.provider = self.cLayer.dataProvider()
            #
            # disconnect the selected features function from the  map vector layer selectionChanged event
            #
            # QObject.disconnect( self.cLayer, SIGNAL("selectionChanged()"), self.getSelectedFeatures )
            #
            #
            #  if not already connected to signal this throws TypeError
            #
            #
            try:
                self.cLayer.selectionChanged.disconnect( self.getSelectedFeatures )
            except TypeError,e:
                pass
            #
            # connect to the custom get selected features function to the map vector layer selectionChanged event
            #
            # QObject.connect( self.cLayer, SIGNAL("selectionChanged()"), self.getSelectedFeatures )
            self.cLayer.selectionChanged.connect( self.getSelectedFeatures )

        #
        # update dialog
        #
        self.dlg.clearGlobals()


    def getSelectedFeatures(self):
        #
        #  reset selection list and dialog globals
        #
        self.selectList = []
        self.dlg.clearGlobals()
        if self.cLayer and self.cLayer.type() == QgsMapLayer.VectorLayer:
            self.selectList = [ featID for featID in self.cLayer.selectedFeaturesIds() ]
            if self.selectList:
                self.updateDialogGlobals()
        else:
            pass


    def updateDialogGlobals(self):
        #
        #  update the selected layer name
        #
        self.dlg.setGlobalLayerType( str( self.cLayer.name() ).upper() )

        #
        #  get a feature count and update #
        #
        self.dlg.setGlobalNumObjects( str( len( self.selectList ) ) )


    def deselectAll( self ):
        for lyr in self.canvas.layers():
            #
            #  
            #  An ENUM for layer types:
            #    VectorLayer   
            #    RasterLayer     
            #    PluginLayer     
            #
            #
            if lyr.type() == QgsMapLayer.VectorLayer:
                if lyr.selectedFeatureCount() > 0:
                    lyr.setSelectedFeatures( [] )
        
    def verifySelectedNumber( self ):
	self.logMessage( "qc selection number..." )
        if self.cLayer.type() == QgsMapLayer.VectorLayer:
            if self.cLayer.selectedFeatureCount() >= 10:
                reply = QMessageBox.question( self.iface.mainWindow(),"Message", 
                "You have 10 or more features selected. Are you sure you want to continue?", QMessageBox.Yes, QMessageBox.No )

                if reply == QMessageBox.Yes:
                    return True
                else:
                    return False
            return True

    def verifyCrossGeometry( self, string_type ):
	self.logMessage( "qc geometry crossing across boundary %s..." % string_type.lower() )
        if self.cLayer.type() == QgsMapLayer.VectorLayer:
            parent_ids = []
            parent_column = self.provider.fieldNameIndex( 'parent_id' )
            if not parent_column: self.logMessage( "[ ERROR ]: **** no fieldNameIndex was found with name 'parent_id' " )
            for fid in self.selectList:
                feat = QgsFeature()
                if not self.provider.featureAtId( fid, feat, True, [ parent_column ] ):
                    self.logMessage( "[ ERROR ]: **** the feature with id [ %s ] does not exist ***" % str( fid ) )
                    return False
                feat_map = feat.attributeMap()
                for k,v in feat_map.items():
                    value = str( v.toString() )
                    if value not in parent_ids:
                        if len( parent_ids ) > 0:
                            reply = QMessageBox.information( self.iface.mainWindow(), 
                            "Info", "Some of the selected features are across %s boundaries and cannot be worked on" % string_type )
                            return False
                        parent_ids.append( value )

            return True
                

    def verifyAdjacentFeatures( self ):
        self.logMessage( "qc adjacent features" )
        if self.cLayer.type() == QgsMapLayer.VectorLayer:
            adjacent_features = set()
            master_set = set( self.selectList )
            for fid in master_set:
                compare_feature = QgsFeature()
                if not self.provider.featureAtId( fid, compare_feature ):
                    self.logMessage( "[ ERROR ]: **** the feature with id [ %s ] does not exist ***" % str( fid ) )
                    return False
                compare_set = master_set - set( [ ( fid ) ] )
                while compare_set:
                    temp_feature = QgsFeature()
                    temp_id = compare_set.pop()
                    if not self.provider.featureAtId( temp_id , temp_feature ):
                        self.logMessage( "[ ERROR ]: **** the feature with id [ %s ] does not exist ***" % str( temp_id ) )
                        return False
                    intersect_geom = compare_feature.geometry().intersection( temp_feature.geometry() )
                    if not intersect_geom.isGeosEmpty() and intersect_geom.type() != QGis.Point:
                        adjacent_features.add( temp_id )
            if not adjacent_features:
                reply = QMessageBox.information( self.iface.mainWindow(), 
                "Info", "None of the selected features were adjacent" )
                return False
            if master_set.difference( adjacent_features ):
                reply = QMessageBox.information( self.iface.mainWindow(), 
                "Info", "The following selected features are not adjacent %s" % str( list(master_set.difference( adjacent_features )) ) )
                return False

            return True
             

    #
    #
    #  BTN listeners/handlers
    #
    #
    def btnDelegateClickHandler( self, kwargs ):
        '''
            this function runs QC for each button event type
            and does any event setup. It then calls
            this class's functions by the same name as the event_name
        '''
        event_name = str( kwargs.get( 'event', '' ) )

        #
        # split, move and createhood have extra inputs
        # here we get them
        #
        txt_value = ''
        if event_name in [ 'Split', 'Move', 'CreateHood' ]:
            txt_edit_name = 'txt'
            if event_name:
                txt_edit_name += event_name
            txt_object = self.dlg.ui.__dict__.get( txt_edit_name, None )
            if txt_object:
                txt_value = str( txt_object.toPlainText() )


        if event_name == 'Add':
            #
            # clear all layer selections
            #
            self.deselectAll()

            #
            #
            #  if not already connected to signal this throws TypeError
            #
            #
            try:
                self.clickTool.canvasClicked.disconnect( self.createQuads )
            except TypeError,e:
                pass
            #
            # connect to the selectFature custom function to the map canvas click event
            #
            self.clickTool.canvasClicked.connect( self.createQuads )

            #
            # make the clickTool active
            #
            self.canvas.setMapTool(self.clickTool)
        elif event_name == 'CreateCity':
            if self.qcSelection( select_type='exact_single' ):
                getattr( self, event_name )()
        elif event_name == 'CreateHood':
            if self.qcSelection( select_type='exact_single' ):
                getattr( self, event_name )( **{ 'txt_value' : txt_value } )
        elif event_name == 'MergeSuperCity':
            if self.qcSelection() and self.verifyCrossGeometry('County') and self.verifyAdjacentFeatures() and self.verifySelectedNumber() :
                getattr( self, event_name )()
        elif event_name == 'Split':
            if self.qcSelection() and self.verifyCrossGeometry('SuperCity') and self.verifyAdjacentFeatures() and self.verifySelectedNumber() :
                getattr( self, event_name )( **{ 'txt_value' : txt_value } )
        elif event_name ==  'Move':
            if len( self.selectList ) == 1:
                if self.qcSelection( select_type='exact_single' ):
                    getattr( self, event_name )( **{ 'txt_value' : txt_value } )
            else:
                if self.getDataSourceTableName( self.cLayer ) == 'layer_super_cities':
                    if self.qcSelection() and self.verifyCrossGeometry('County') and self.verifyAdjacentFeatures() and self.verifySelectedNumber():
                        getattr( self, event_name )( **{ 'txt_value' : txt_value } )
                else: 
                    getattr( self, event_name )( **{ 'txt_value' : txt_value } )
        elif event_name == 'Add2Water':
            if len( self.selectList ) == 1:
                if self.qcSelection( select_type='exact_single' ):
                    getattr( self, event_name )()
            else:
                if self.qcSelection():
                    getattr( self, event_name )()
        elif event_name == 'UpdateGeom':
            if self.qcSelection( select_type='exact_single' ):
                    getattr( self, event_name )()

    def transformPoint( self, point, srcSRID, destSRID ):

        crsSrc = QgsCoordinateReferenceSystem(srcSRID) 
        crsDest = QgsCoordinateReferenceSystem(destSRID)
        xform = QgsCoordinateTransform(crsSrc, crsDest)
        pnt_transformed = xform.transform( point )

        # inverse transformation: dest -> src
        # pnt_4326 = xform.transform( pnt_3857, QgsCoordinateTransform.ReverseTransform)
        return pnt_transformed

    def logMessage(self, message ):
        QgsMessageLog.logMessage( str(message), 'QuadStreaker' )

    def createConnection( self ):
        #
        #  get connection for calling stored proc
        #
        if self.cLayer.type() != QgsMapLayer.VectorLayer: 
            QMessageBox.information( self.iface.mainWindow(), "Info", "You must have a vector layer selected to run quadstreaker commands" )
            return
    
        #
        #
        #  if the selected TOC layer provider type is POSTGRES
        #  then we are all cool creating connection from layer provider information
        #  if the selected TOC layer provider type is OGR ( meaning shapefile )
        #  then the ayer in the TOC is a shapefile and we need to create 
        #  a connection from another layer such as Layer_Quads for CreateHood function
        #
        #
        self.conn = None
        if self.getDataSourceProviderType( self.cLayer ) == 'postgres':
            vlayer_uri = self.cLayer.dataProvider().dataSourceUri()
            self.conn = self.createProcConnection( vlayer_uri )
        elif self.getDataSourceProviderType( self.cLayer ) == 'ogr':
            quad_layer = self.findLayerByDataSourceTableName( 'layer_quads' )
            if quad_layer:
                vlayer_uri = quad_layer.dataProvider().dataSourceUri()
                self.conn = self.createProcConnection( vlayer_uri )
            else:
                self.logMessage( "[ ERROR ]: layer not visible (checked) or not found when searching for layer = 'layer_quads'" )

        #
        #
        #  check connection information
        #
        #
        if not self.conn:
            QMessageBox.critical( self.iface.mainWindow(),"Info", "The stored procedure could not be called because no DB connection established" )
            return
        self.crs = self.conn.cursor()

    def deleteConnection( self ):
        #
        # close the cursor, connection to postgis
        #
        self.crs.close()
        self.conn.close()
        #del self.crs, self.conn
        
    def qcSelection(self, select_type=None):
	self.logMessage( "qc feature selection..." )
        if not select_type:
            if not self.selectList or len( self.selectList ) == 1:
                QMessageBox.information( self.iface.mainWindow(),"Info", "You need to have MORE THAN ONE feature selected to run this function" )
                return False
        elif select_type == 'exact_single':
            if not self.selectList or len( self.selectList ) > 1:
                QMessageBox.information( self.iface.mainWindow(),"Info", "You need to have EXACTLY ONE feature selected to run this function" )
                return False
        return True

    def continueCityOrSuperCity( self, list_feats ):
        '''
            list_feats is a list of 2 tuples from 
            postgres where the first element is a SuperCity record
            and the second element is a City record 
            both with the following index structure:
                0 =  id
                1 =  name
                2 =  type
                3 =  distance
        '''
        supercity = 0
        city = 1
        id = 0
        name = 1
        typeof = 2
        distance = 3

        #
        # 
        #  check what came back
        #  sometimes no city might come back
        #  and then we need to exlude city button
        #  and vice versa
        #
        #
        qmsg = QMessageBox()
        btn_cancel = qmsg.addButton( "Cancel", QMessageBox.NoRole )
        qmsg.setDefaultButton( btn_cancel )
        message_text = ''
        if list_feats[supercity] is None and list_feats[city] is None: # Neither
            self.logMessage( "[ ERROR ]: Both SuperCity and City cannot be None" )
            return None
        elif list_feats[supercity] is None: # No SuperCity
            message_text = "Make this SuperQuad a member of %s?" % ( list_feats[city][name] ) 
            btn_city = qmsg.addButton( "%s : %s" % ( list_feats[city][typeof], list_feats[city][name] ), QMessageBox.YesRole )
        elif list_feats[city] is None: # No city
            message_text = "Make this SuperQuad a memer of %s?" % ( list_feats[supercity][name] ) 
            btn_supercity = qmsg.addButton( "%s : %s" % ( list_feats[supercity][typeof], list_feats[supercity][name] ), QMessageBox.ApplyRole )
        else: # both 
            message_text = "Which feature would you like this SuperQuad to become a member of %s or %s?" % ( list_feats[supercity][name], list_feats[city][name] ) 
            btn_city = qmsg.addButton( "%s : %s" % ( list_feats[city][typeof], list_feats[city][name] ), QMessageBox.YesRole )
            btn_supercity = qmsg.addButton( "%s : %s" % ( list_feats[supercity][typeof], list_feats[supercity][name] ), QMessageBox.ApplyRole )
        qmsg.setIcon( QMessageBox.Question )
        qmsg.setText( message_text )
        reply = qmsg.exec_()  # blocks until button clicked

        #
        #
        #  the reply is the index
        #  order of the added buttons
        #  0 = cancel, 1 = yes role, 2 = apply role
        #
        #
        if reply == 0: # cancel
            return None
        elif reply == 1: # yes role
            return list_feats[city]
        elif reply == 2: # apply role
            return list_feats[supercity]
        else:
            return None

    def continueQuadOrSuperQuad( self ):
        qmsg = QMessageBox()
        qmsg.setText( "Use this point to create a Quad or SuperQuad?" )
        qmsg.setIcon( QMessageBox.Question )
        btn_cancel = qmsg.addButton( "Cancel", QMessageBox.NoRole )
        btn_quad = qmsg.addButton( "Quad", QMessageBox.YesRole )
        btn_superquad = qmsg.addButton( "SuperQuad", QMessageBox.ApplyRole )
        qmsg.setDefaultButton( btn_cancel )
        reply = qmsg.exec_()  # blocks until button clicked
        #
        #
        #  the reply is the index
        #  order of the added buttons
        #  0 = cancel, 1 = quad, 2 = super
        #
        #
        if reply == 0: # cancel
            return None
        elif reply == 1: # quad
            return "createQuad"
        elif reply == 2: # superquad
            return "createSuperQuad"
        else:
            return None

    def createQuads(self, point, button):
        #
        # this is how we get our point information
        #
        # e.g.: self.dlg.setTextBrowser( str(point.x()) + " , " +str(point.y()) )
        #
        quad_action = self.continueQuadOrSuperQuad()
        self.point = point
        if quad_action:
            getattr( self, 'Add' )( quad_action )
        else:
            #
            # disconnect to the selectFature custom function to the map canvas click event
            #
            # QObject.disconnect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.createSuperQuad)
            #
            self.clickTool.canvasClicked.disconnect( self.createQuads )

            #
            # activate the multiselect freehand tool
            #
            self.iface.actionSelectFreehand().trigger()

    #
    #
    #  UTIL CALLS STORED PROCEDURES
    #
    #
    def callStoredProcedure( self, sql_statement, fetch='fetchone', **kwargs ):
        self.logMessage( 'executing [ %s ]' % sql_statement )
        self.crs.execute( sql_statement )
        response = None
        if hasattr( self.crs, fetch ):
            response = getattr( self.crs, fetch )()
        else:
            self.log_message.emit( "[ ERROR ]: the cursor object could not find the fetch method = %s" % fetch )
        self.conn.commit()

        return response

    def responseMessage( self, stored_proc_call, response, format_type='int' ):
        message = ''
        fail = False
        if format_type == 'int': # stored proc return type yeilds int ERRORS

            if not response:
                fail = True
                message = '[ ERROR ]: response is NULL'
            elif response[0] >= 0:
                message = '%s successfully returned = %s' % ( stored_proc_call, str( response[0] ) )   

                #
                # clear all layer selections
                #
                self.deselectAll()
            else:
                fail = True
                message = '[ ERROR ]: %s failed with code = [ %s ]' % ( stored_proc_call, STORED_PROC.ERRORS.get( response[0], 'None' ) )

        else: # stored proc return type yeilds Boolean
            
            if not response:
                fail = True
                message = '[ ERROR ]: response is NULL'
            elif response[0] == True:
                message = '%s successfully returned = %s' % ( stored_proc_call, str( response[0] ) )   

                #
                # clear all layer selections
                #
                self.deselectAll()
            else:
                fail = True
                message = '[ ERROR ]: %s failed with code = [ %s ]' % ( stored_proc_call, str( response[0] ) )
        
        return ( message, fail )

    #
    #
    #   STORED PROCEDURE SETUP
    #
    #
    def Add( self, stored_proc_type ):
            self.createConnection() 

            if stored_proc_type == 'createQuad':
                pnt_4326 = self.transformPoint( self.point, 3857, 4326 )
                statement = "SELECT * from splitSuperQuad( 'SRID=%s;%s' )" % ( str(self.cLayer.crs().authid()).split(':')[1] , pnt_4326.wellKnownText() )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'splitSuperQuad', response )
                self.logMessage( message )
                if fail: 
                    reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                    return
                
                #
                #
                #  refresh map
                #
                #
                self.canvas.refresh()
            elif stored_proc_type == 'createSuperQuad':
                pnt_4326 = self.transformPoint( self.point, 3857, 4326 )
                
                #
                #
                #  get closest SuperCity and City for user to choose from
                #
                #
                choices = []
                statement = """SELECT sc.id, sc.name, 'SuperCity' as my_type, ST_Distance( sc.geom, st_geomfromewkt( 'SRID=%s;%s' ) )
                AS distance FROM layer_super_cities sc WHERE
                ST_DWithin( sc.geom, st_geomfromewkt( 'SRID=%s;%s' ), 0.05 ) AND sc.active = True order by distance asc LIMIT 1;""" % ( str(self.cLayer.crs().authid()).split(':')[1] , 
                pnt_4326.wellKnownText(), str(self.cLayer.crs().authid()).split(':')[1] , pnt_4326.wellKnownText() )
                response = self.callStoredProcedure( statement )
                if response:
                    choices.append( response )
                else:
                    choices.append( None )

                statement = """SELECT c.id, c.name, 'City' as my_type, ST_Distance( c.geom, st_geomfromewkt( 'SRID=%s;%s' ) )
                AS distance FROM layer_cities c WHERE
                ST_DWithin( c.geom, st_geomfromewkt( 'SRID=%s;%s' ), 0.05 ) order by distance asc LIMIT 1;""" % ( str(self.cLayer.crs().authid()).split(':')[1] , 
                pnt_4326.wellKnownText(), str(self.cLayer.crs().authid()).split(':')[1] , pnt_4326.wellKnownText() )
                response = self.callStoredProcedure( statement )
                if not response:
                    self.logMessage( '[ ERROR ]: no city returned from point location' )
                if response:
                    choices.append( response )
                else:
                    choices.append( None )

                #
                #
                #    choices is a list of 2 tuples from 
                #    postgres where the first element is a SuperCity record
                #    and the second element is a City record 
                #    both with the following index structure:
                #        0 =  id
                #        1 =  name
                #        2 =  type
                #        3 =  distance
                #
                #
                pick = self.continueCityOrSuperCity( choices )
                if not pick:
                    self.logMessage( 'No choice was made' )
                    self.deleteConnection()
                    return # exit
                #
                #
                # spin off another thread to handle creation
                #
                #
                statement = ''
                self.logMessage( "PICK: %s" % pick[2] )
                if pick[2] == 'SuperCity':
                    statement = "SELECT * from createSuperQuadInSuperCity( 'SRID=%s;%s' , %i )" % ( str(self.cLayer.crs().authid()).split(':')[1] , pnt_4326.wellKnownText(), pick[0] )
                elif pick[2] == 'City':
                    statement = "SELECT * from createSuperQuadInCity( 'SRID=%s;%s' , %i )" % ( str(self.cLayer.crs().authid()).split(':')[1] , pnt_4326.wellKnownText(), pick[0] )
                vlayer_uri = self.cLayer.dataProvider().dataSourceUri()
                workerThread = StoredProcWorkerThread( self.iface.mainWindow(), vlayer_uri, statement, fetch='fetchone' )
                workerThread.log_message.connect( self.logMessage ) # to log to QMessageBox
                workerThread.general_error.connect( self.logMessage )
                workerThread.import_error.connect( self.logMessage )
                workerThread.finished.connect( workerThread.quit )
                workerThread.refresh.connect( self.canvas.refresh )
                workerThread.start()
                self.worker_threads.append( workerThread )

                #
                # clear all layer selections
                #
                self.deselectAll()

            self.deleteConnection()

    def CreateHood( self, **kwargs ):
            self.createConnection()

            #
            # check that the provider is SHAPEFILE
            #
            if self.getDataSourceProviderType( self.cLayer ) != 'ogr':
                QMessageBox.information( self.iface.mainWindow(), "Info", "To run this function you need to select a Shapefile layer"  )

            message = ''
            txt_value = kwargs.get( 'txt_value', 'Hood Unknown' )
            if self.getDataSourceProviderType( self.cLayer ) == 'ogr':
                #
                #  previous to this we QC that this function only takes one selected feature
                #  so we can be sure that we access it here
                #
                feature = QgsFeature()
                if not self.provider.featureAtId( self.selectList[0], feature ):
                    self.logMessage( "**** The shapefile feature with the following ID cannot be found %s ****" % str( self.selectList[0] ) )

                wkt = feature.geometry().exportToWkt()  
                srid = str(self.cLayer.crs().authid()).split(':')[1]

                statement = "SELECT createHood( 'SRID=%s;%s', '%s' );" % ( srid, wkt, txt_value )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'createHood', response )
                self.logMessage( message )
                if fail: 
                    reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                    return

                #
                # refresh the map canvas
                #
                self.canvas.refresh()

            self.deleteConnection()

    def CreateCity( self ):
            self.createConnection()

            message = ''
            if self.getDataSourceTableName( self.cLayer ) == 'layer_super_cities':
                statement = "SELECT createCity( %s );" % ( int( self.selectList[0] ) )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'createCity', response )
                self.logMessage( message )
                if fail: 
                    reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                    return
            else:
                QMessageBox.information( self.iface.mainWindow(), "Info", "Invalid Layer Selection"  )

            self.deleteConnection()

    def MergeSuperCity( self ):
            self.createConnection()

            message = ''
            if self.getDataSourceTableName( self.cLayer ) == 'layer_super_cities':
                statement = "SELECT mergeSuperCities( ARRAY%s );" % ( map( lambda i: int( i ), self.selectList ) )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'mergeSuperCities', response )
                self.logMessage( message )
                if fail: 
                    reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                    return
            else:
                QMessageBox.information( self.iface.mainWindow(), "Info", "Invalid Layer Selection"  )

            #
            # refresh the map canvas
            #
            self.canvas.refresh()
        
            self.deleteConnection()

    def UpdateGeom( self ):
            self.createConnection()

            message = ''
            fail = False
            if self.getDataSourceTableName( self.cLayer ) == 'layer_super_cities':
                statement = "select updateSuperCityGeom(%i);" % int( self.selectList[0] )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'updateSuperCityGeom', response, format_type='bool' )
            elif self.getDataSourceTableName( self.cLayer ) == 'layer_counties':
                statement = "select updateCountyGeom(%i);" % int( self.selectList[0] )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'updateCountyGeom', response, format_type='bool' )
            elif self.getDataSourceTableName( self.cLayer ) == 'layer_states':
                statement = "select updateStateGeom(%i);" % int( self.selectList[0] )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'updateStateGeom', response, format_type='bool' )
            elif self.getDataSourceTableName( self.cLayer ) == 'layer_countries':
                statement = "select updateCountryGeom(%i);" % int( self.selectList[0] )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'updateCountryGeom', response, format_type='bool' )
            else:
                message = 'Invalid layer selection -- the functionality to handle this layer type does not exist yet'
                QMessageBox.information( self.iface.mainWindow(), "Info", message  )
        
            self.logMessage( message )
            if fail: 
                reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                return
                
            #
            # refresh the map canvas
            #
            self.canvas.refresh()

            self.deleteConnection()

    def Split( self , **kwargs ):

            self.createConnection()

            message = ''
            fail = False
            if self.getDataSourceTableName( self.cLayer ) == 'layer_super_quads':
                txt_value = ( kwargs.get( 'txt_value', 'None' ) ).strip()
                statement = "select SplitSuperCity( ARRAY%s, '%s' );" % ( map( lambda i: int( i ), self.selectList ), txt_value )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'SplitSuperCity', response )
            else:
                message = 'Invalid layer selection -- the functionality to handle this layer type does not exist yet'
                QMessageBox.information( self.iface.mainWindow(), "Info", message  )

            self.logMessage( message )
            if fail: 
                reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                return

            #
            # refresh the map canvas
            #
            self.canvas.refresh()

            self.deleteConnection()

    def Add2Water( self ):
            self.createConnection()

            message = ''
            fail = False
            if self.getDataSourceTableName( self.cLayer )  == 'layer_super_quads':
                statement = "SELECT moveSuperQuads2Water( ARRAY%s );" % ( map( lambda i: int( i ), self.selectList ) )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'moveSuperQuads2Water', response, format_type='bool' )
            elif self.getDataSourceTableName( self.cLayer ) == 'layer_quads':
                statement = "SELECT moveQuads2Water( ARRAY%s );" % ( map( lambda i: int( i ), self.selectList ) )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'moveQuads2Water', response, format_type='bool' )
            else:
                message = 'Invalid layer selection -- the functionality to handle this layer type does not exist yet'
                QMessageBox.information( self.iface.mainWindow(), "Info", message  )
            
            self.logMessage( message )
            if fail: 
                reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                return

            #
            # refresh the map canvas
            #
            self.canvas.refresh()
        
            self.deleteConnection()

    def Move( self, **kwargs ):
            self.createConnection()

            message = ''
            fail = False
            txt_value = kwargs.get( 'txt_value', 'None' )
            if self.getDataSourceTableName( self.cLayer )  == 'layer_super_quads':
                statement = "SELECT moveSuperQuads( ARRAY%s, %s );" % ( map( lambda i: int( i ), self.selectList ), int( txt_value ) )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'moveSuperQuads', response, format_type='bool' )
            elif self.getDataSourceTableName( self.cLayer ) == 'layer_quads':
                statement = "SELECT parent_id FROM layer_quads WHERE id = ANY ( ARRAY%s ) GROUP BY parent_id" % ( map( lambda i: int( i ), self.selectList ) )
                hoods = self.callStoredProcedure( statement, fetch='fetchall' )
                if not hoods:
                    self.logMessage( '[ ERROR ]: No hoods returned from call last SQL statement' )
                hood_list = [ i[0] for i in hoods if i[0] not in [ 1136, None ] ]

                statement = "SELECT moveQuads( ARRAY%s, %s );" % ( map( lambda i: int( i ), self.selectList ), int( txt_value ) )
                response = self.callStoredProcedure( statement )
                if not response:
                    self.logMessage( '[ ERROR ]: moveQuads returned = %s' % str( response ) )
                hood_list.append( int( txt_value ) )

                statement = "SELECT updateHoodsGeom( ARRAY%s );" % ( hood_list )
                response = self.callStoredProcedure( statement )
                message, fail = self.responseMessage( 'updateHoodsGeom', response, format_type='bool' )
            else:
                message = 'Invalid layer selection -- the functionality to handle this layer type does not exist yet'
                QMessageBox.information( self.iface.mainWindow(), "Info", message  )
            
            self.logMessage( message )
            if fail: 
                reply = QMessageBox.critical( self.iface.mainWindow(), "Critical", message )
                return


            #
            # refresh the map canvas
            #
            self.canvas.refresh()
            

            self.deleteConnection()

    def run(self):

        #
        # show the dialog
        #
        self.dlg.show()

        #
        # set the active layer
        #
        if not self.canvas.currentLayer() and len( self.canvas.layers() ) > 0:
            self.setActiveLayer( self.canvas.layers()[0] )
        else:
            QMessageBox.information( self.iface.mainWindow(),"Info", "You need to add a layer to the TOC for this to work dude" )

        #
        # activate the multiselect freehand tool
        #
        self.iface.actionSelectFreehand().trigger()

        #
        # run main dialog
        #
        result = self.dlg.exec_()
        if result == 0: # someone clicked the exit X 
            for wthread in self.worker_threads:
                thread_name = ' '.join( str( wthread ).split( ' ' )[1:] )
                QgsMessageLog.logMessage( "thread <%s isRunning = %s" % ( thread_name, str( wthread.isRunning() ) ), 'QuadStreaker' )
                if not wthread.isFinished():
                    QgsMessageLog.logMessage( "terminating thread <%s" % ( str( thread_name ) ), 'QuadStreaker' )
                    wthread.terminate()
                     
            #
            # disconnect to the selectFature custom function to the map canvas click event
            #
            # QObject.disconnect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.createSuperQuad)
            #
            #
            #  if not already connected to signal this throws TypeError
            #
            #
            try:
                self.clickTool.canvasClicked.disconnect( self.createQuads )
            except TypeError,e:
                pass
