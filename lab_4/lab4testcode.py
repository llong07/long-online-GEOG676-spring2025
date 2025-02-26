import arcpy #create geodatabase and input garage features

arcpy.env.workspace = r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4'
folder_path = r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4'
gdb_name = 'c2-campus.gdb'
gdb_path = folder_path + '\\' + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_path = r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4\garages.csv'
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

campus = r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4\0Campus.gdb'
buildings_campus = campus + '\Structures'
buildings = gdb_path + '\\' + 'Buildings'

#Previous code copied building features into our database from the campus database

arcpy.Copy_management(buildings_campus, buildings)

#re-projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

#buffer garages
garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_points_reprojected', gdb_path + '\Garage_Points_buffered', 150)

#intersect buffer with buildings
arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')

arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf', r'C:\GEOG676\long-online-GEOG676-spring2025\lab_4', '4nearbyBuildings.csv')