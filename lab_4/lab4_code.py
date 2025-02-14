
# create a gbd and garage feature
import arcpy

arcpy.env.workspace = r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4\codes_env'
folder_path = r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4'
gbd_name = 'Test.gbd'
gbd_path = folder_path + '\\' + gbd_name
arcpy.CreateFileGDB_management(folder_path, gbd_name)

csv_path = r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4\garages.csv'
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gbd_path)
garage_points = gbd_path + '\\' + garage_layer_name

# open campus gbd, copy building feature to our gbd
campus = r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4\Campus.gbd'
buildings_campus = campus +'\Structures'
buildings = gbd_path + '\\' + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)

# re-projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gbd_path + '\Garage_Points_reprojected', spatial_ref)

# buffer the garages
garageBuffered = arcpy.Buffer_analysis(gbd_path + '\Garage_Points_reprojected', gbd_path +'\Garage_Points_buffered', 150)

# intersect our buffer with the buildings
arcpy.Intersect_analysis([garageBuffered, buildings], gbd_path + '\Garage_Building_Intersection', 'ALL')

arcpy.TableToTable_conversion(gbd_path + '\Garage_Building_Intersection.dbf', 'C:\GEOG676\long-online-GEOG676-spring2025\lab_4', 'nearbyBuildings.csv')