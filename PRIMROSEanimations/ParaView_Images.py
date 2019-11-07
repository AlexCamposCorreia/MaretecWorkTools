# trace generated using paraview version 5.7.0-RC4
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'PVD Reader'
pRIMROSELagrangianpvd = PVDReader(FileName='G:\\Aplica\\05275-PRIMROSE-Lagrangian\\PRIMROSE-Lagrangian_out\\PRIMROSE-Lagrangian.pvd')
pRIMROSELagrangianpvd.PointArrays = ['id', 'source', 'velocity', 'state']

# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [552, 893]

# show data in view
pRIMROSELagrangianpvdDisplay = Show(pRIMROSELagrangianpvd, renderView1)

# trace defaults for the display properties.
pRIMROSELagrangianpvdDisplay.Representation = 'Surface'
pRIMROSELagrangianpvdDisplay.ColorArrayName = [None, '']
pRIMROSELagrangianpvdDisplay.OSPRayScaleArray = 'id'
pRIMROSELagrangianpvdDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
pRIMROSELagrangianpvdDisplay.SelectOrientationVectors = 'None'
pRIMROSELagrangianpvdDisplay.ScaleFactor = 0.49700127200424904
pRIMROSELagrangianpvdDisplay.SelectScaleArray = 'None'
pRIMROSELagrangianpvdDisplay.GlyphType = 'Arrow'
pRIMROSELagrangianpvdDisplay.GlyphTableIndexArray = 'None'
pRIMROSELagrangianpvdDisplay.GaussianRadius = 0.02485006360021245
pRIMROSELagrangianpvdDisplay.SetScaleArray = ['POINTS', 'id']
pRIMROSELagrangianpvdDisplay.ScaleTransferFunction = 'PiecewiseFunction'
pRIMROSELagrangianpvdDisplay.OpacityArray = ['POINTS', 'id']
pRIMROSELagrangianpvdDisplay.OpacityTransferFunction = 'PiecewiseFunction'
pRIMROSELagrangianpvdDisplay.DataAxesGrid = 'GridAxesRepresentation'
pRIMROSELagrangianpvdDisplay.PolarAxes = 'PolarAxesRepresentation'
pRIMROSELagrangianpvdDisplay.ScalarOpacityUnitDistance = 0.21705644320348882

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
pRIMROSELagrangianpvdDisplay.ScaleTransferFunction.Points = [1.0, 0.0, 0.5, 0.0, 16606.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
pRIMROSELagrangianpvdDisplay.OpacityTransferFunction.Points = [1.0, 0.0, 0.5, 0.0, 16606.0, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera()

#changing interaction mode based on data extents
renderView1.CameraPosition = [-8.624672377228157, 39.37913116579504, 10000.0]
renderView1.CameraFocalPoint = [-8.624672377228157, 39.37913116579504, 0.0]

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(pRIMROSELagrangianpvdDisplay, ('POINTS', 'state'))

# rescale color and/or opacity maps used to include current data range
pRIMROSELagrangianpvdDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
pRIMROSELagrangianpvdDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'state'
stateLUT = GetColorTransferFunction('state')

# get opacity transfer function/opacity map for 'state'
statePWF = GetOpacityTransferFunction('state')

# set scalar coloring
ColorBy(pRIMROSELagrangianpvdDisplay, ('POINTS', 'source'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(stateLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
pRIMROSELagrangianpvdDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
pRIMROSELagrangianpvdDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'source'
sourceLUT = GetColorTransferFunction('source')

# get opacity transfer function/opacity map for 'source'
sourcePWF = GetOpacityTransferFunction('source')

# hide color bar/color legend
pRIMROSELagrangianpvdDisplay.SetScalarBarVisibility(renderView1, False)

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 0

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [-8.624672377228157, 39.37913116579504, 10000.0]
renderView1.CameraFocalPoint = [-8.624672377228157, 39.37913116579504, 0.0]
renderView1.CameraParallelScale = 3.0594216681365682

# save animation
SaveAnimation('G:/Aplica/05275-PRIMROSE-Lagrangian/Work/PRIMROSEanimations/input/anim.png', renderView1, ImageResolution=[552, 893],
    FrameWindow=[0, 143])

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [-8.624672377228157, 39.37913116579504, 10000.0]
renderView1.CameraFocalPoint = [-8.624672377228157, 39.37913116579504, 0.0]
renderView1.CameraParallelScale = 3.0594216681365682

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).