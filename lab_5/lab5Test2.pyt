import arcpy
import os
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "GarageBuildingIntersection"
        self.alias = "GarageBuildingIntersection"
        self.tools = [GarageBuildingIntersection]
class GarageBuildingIntersection(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab5 Toolbox"
        self.description = "Determines which buildings on TAMU's campus are near garages."
        self.canRunInBackground = False
        self.category = "Building Tools"
    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="CampusGDB",
            datatype="DEWorkspace",  # Corrected type
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="BufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        return [param0, param1, param2, param3, param4, param5]
    def execute(self, parameters, messages):
        """The source code of the tool."""
        folder_path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText + ".gdb"  # Ensure .gdb extension
        gdb_path = os.path.join(folder_path, gdb_name)
        # Ensure GDB exists
        if not arcpy.Exists(gdb_path):
            arcpy.CreateFileGDB_management(folder_path, gdb_name)
        else:
            print(f"Geodatabase {gdb_name} already exists. Skipping creation.")
        # Extract CSV data
        csv_path = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText
        garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)
        # Convert to Feature Class
        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = os.path.join(gdb_path, garage_layer_name)
        # Copy Campus Buildings
        campus = parameters[4].valueAsText
        buildings_campus = os.path.join(campus, "Structures")
        buildings = os.path.join(gdb_path, "Buildings")
        arcpy.Copy_management(buildings_campus, buildings)
        # Reprojection
        spatial_ref = arcpy.Describe(buildings).spatialReference
        garage_reprojected = os.path.join(gdb_path, "Garage_Points_reprojected")
        arcpy.Project_management(garage_points, garage_reprojected, spatial_ref)
        # Buffering
        buffer_distance = parameters[5].valueAsText
        garage_buffered = os.path.join(gdb_path, "Garage_Points_buffered")
        arcpy.Buffer_analysis(garage_reprojected, garage_buffered, buffer_distance)
        # Intersection
        garage_building_intersection = os.path.join(gdb_path, "Garage_Buildings_Intersection")
        arcpy.Intersect_analysis([garage_buffered, buildings], garage_building_intersection, "ALL")
        # Export CSV
        output_csv_path = os.path.join(folder_path, "nearbyBuildings.csv")
        arcpy.TableToTable_conversion(garage_building_intersection + ".dbf", folder_path, "nearbyBuildings.csv")
        print(f"Process completed. Output saved to {output_csv_path}")
        return None