import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

p = mdb.models['Model-A'].parts['Part-1']
f = p.faces
e = p.edges
# Delete mesh
pickedRegions = f.getSequenceFromMask(mask=('[#3f8000ff #4ffe00 ]',), )
p.deleteMesh(regions=pickedRegions)

# Specifymesh
pickedEdges = e.getSequenceFromMask(mask=(
    '[#7fffffff #e9a9b66a #ffffffff #c002f ]',), )
p.seedEdgeBySize(edges=pickedEdges, size=2.63669, deviationFactor=0.1,
                 minSizeFactor=0.1, constraint=FINER)

# Generate mesh
pickedRegions = f.getSequenceFromMask(mask=('[#4 ]',), )
p.generateMesh(regions=pickedRegions)