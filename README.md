# Simplification
Some implementations of algorithms for map simplification. This toolbox (Progressive Simplification) is the combination of the two existing toolboxes in ArcGIS software (Point-Remove and Bend-Simplify) which runs faster after preprocessing the map. Here's how to use the toolbox when you aim to simplify your map easpecially if you deal with hydorogical analysis:

1. Open Simplify.mxd via ArcMap 10.x
2. Find the python toolbox named Progsimplify in your Catalog and open it.
3. Import your input <Shape File> (.shp) in the first field, insert the number of maps you want to store in the data structure (map precision) in the field associated with k. The larger k is, the longer you need to wait for map to be preprocessed. Threshold is derived from scale of the map, however you may set a number between zero and one. And output directory for the simplified map which is optional.
4. Cick ok to execute the toolbox. Once the process bar is shown completed, find the resulting map in the out directory.
  
 If you have any idea regarding improvement of the toolbox, do not hesitate to contact me: armin.autcs@gmail.com
