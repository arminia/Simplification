from __future__ import division
from decimal import Decimal
import arcpy
from arcpy import env
import math
import os.path
import time

import arcpy.management as DM
import arcpy.cartography as CA


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Progressive Simplification"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = "This method runs faster than POINT_REMOVE and BENT_SIMPLIFY by combining the latter methods together and resulting in simplified map smmother than the first method but coarser than the second one."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="DEShapefile",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="K",
            name="sinuosity_field1",
            datatype="Double",
            parameterType="Required",
            direction="Input")


         #Second parameter
        param2 = arcpy.Parameter(
            displayName="Threshold",
            name="sinuosity_field",
            datatype="Double",
            parameterType="Optional",
            direction="Input")

        
        # param1.value = "sinuosity"

        # Third parameter
        param3 = arcpy.Parameter(
            displayName="Output Features",
            name="out_features",
            datatype="DEShapefile",
            parameterType="Optional",
            direction="Output")


        # param2.parameterDependencies = [param0.name]
        # param2.schema.clone = True

        params = [param0, param1, param2, param3]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):

        t1= time.time() #Setting time
        
        env.workspace =  os.getcwd() #Setting the workspace

        #Initialization
        
        inFeatures = parameters[0].valueAsText 

        k = int(parameters[1].valueAsText)

        
            

        outFeatureClass = parameters[3].valueAsText

        # Fetching the map and the layer
        
        mxd_dir = env.workspace + "\Experiments\Simplify.mxd"  # name of the map

        mxd = arcpy.mapping.MapDocument(mxd_dir)

        for df in arcpy.mapping.ListDataFrames(mxd):

                df.rotation = 0

        
        #Normalization
        
        norm = 1200000

        scale = df.scale

        if (scale < 5000):
            scale = 1

        if (scale > 1250000):
            scale = 500000000

        # Tolerance input check

        if (parameters[2].ValueAsText is not None):
            tolerance_Q = float(parameters[2].valueAsText)
        else:
            tolerance_Q = scale / norm

        # PREPROCESSING STAGE STARTS

        step = int(norm / k)

        newpath = env.workspace + "/Experiments/datastructure/maps" + str(k)

        if not os.path.exists(newpath):
            os.makedirs(newpath)
            
        for i in range(1, norm, step):

            tolerance_P = i / norm

            M_P = newpath + "/BS" + str(i)

            if (os.path.isfile(M_P + ".shp") == True):
                break

            CA.SimplifyLine(inFeatures,
                            M_P,
                            "BEND_SIMPLIFY",
                            tolerance_P,
                            "FLAG_ERRORS",
                            "No_KEEP",
                            "NO_CHECK")


        # PREPROCESSING STAGE ENDS

        if (tolerance_Q > 0 and tolerance_Q < 1):

            querydir = env.workspace + "/Experiments/Prog_output" + str(k)

            if not os.path.exists(querydir):
                os.makedirs(querydir)
            
            simplifiedFeatures = outFeatureClass

            if (outFeatureClass is None):
                simplifiedFeatures = querydir + "/newMap" + str(int(tolerance_Q * norm))

            if (os.path.isfile(simplifiedFeatures + ".shp") == True):

                print "The Simplified Map in this scale already exists."

                layer = arcpy.mapping.Layer(simplifiedFeatures + ".shp")

                arcpy.mapping.AddLayer(df, layer, "BOTTOM")

                arcpy.RefreshActiveView()

                arcpy.RefreshTOC()

                # extract it and show it in TOC

            else:

                for i in range(int(tolerance_Q * norm) - step, int(tolerance_Q * norm)):

                    M_Q =  newpath + "BS" + str(i) + ".shp"
                    if (os.path.isfile(M_Q) == True):
                        
                        offset = tolerance_Q * norm - i

                        CA.SimplifyLine(M_Q,
                                        simplifiedFeatures,
                                        "POINT_REMOVE",
                                        offset / norm,
                                        "FLAG_ERRORS",
                                        "No_KEEP",
                                        "NO_CHECK")

        else:

            print "The scale is out of the restricted range!"

        t3= time.time()
        print "Processing Time: "+str(format((t2-t1),'.3f')) + " and query time: " + str (format((t3-t1),'.3f'))

        return
