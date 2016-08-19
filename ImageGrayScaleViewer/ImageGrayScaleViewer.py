import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# ImageGrayScaleViewer
#

class ImageGrayScaleViewer(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ImageGrayScaleViewer" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Longquan Chen (BWH/Harvard.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# ImageGrayScaleViewerWidget
#

class ImageGrayScaleViewerWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # Window value
    #
    self.imageWindowSliderWidget = ctk.ctkSliderWidget()
    self.imageWindowSliderWidget.singleStep = 0.1
    self.imageWindowSliderWidget.minimum = -100
    self.imageWindowSliderWidget.maximum = 100
    self.imageWindowSliderWidget.value = 0.5
    self.imageWindowSliderWidget.setToolTip("Set window value for the gray scale of the")
    parametersFormLayout.addRow("Image Window Position", self.imageWindowSliderWidget)

    #
    # Level value
    #
    self.imageLevelSliderWidget = ctk.ctkSliderWidget()
    self.imageLevelSliderWidget.singleStep = 0.1
    self.imageLevelSliderWidget.minimum = -100
    self.imageLevelSliderWidget.maximum = 100
    self.imageLevelSliderWidget.value = 0.5
    self.imageLevelSliderWidget.setToolTip("Set Level value for the gray scale of the")
    parametersFormLayout.addRow("Image Level Position", self.imageLevelSliderWidget)
    
    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)
    
    #
    # Get GrayScale Button
    #
    self.getScaleButton = qt.QPushButton("GetScaleInfo")
    self.getScaleButton.toolTip = "Get the scale information."
    self.getScaleButton.enabled = False
    parametersFormLayout.addRow(self.getScaleButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.getScaleButton.connect('clicked(bool)', self.onGetScaleButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode()
    self.getScaleButton.enabled = self.inputSelector.currentNode()
    if self.inputSelector.currentNode():
      imageData = self.inputSelector.currentNode().GetImageData()
      range = imageData.GetScalarRange()
      self.imageWindowSliderWidget.minimum = float(range[0])
      self.imageWindowSliderWidget.maximum = float(range[1])
      self.imageLevelSliderWidget.minimum = float(range[0])
      self.imageLevelSliderWidget.maximum = float(range[1])

  def onApplyButton(self):
    logic = ImageGrayScaleViewerLogic()
    imageWindow = self.imageWindowSliderWidget.value
    imageLevel = self.imageWindowSliderWidget.value
    displayNode = self.inputSelector.currentNode().GetVolumeDisplayNode()
    displayNode.SetWindowLevel(imageWindow, imageLevel)
  
  
  def onGetScaleButton(self):
    displayNode = self.inputSelector.currentNode().GetVolumeDisplayNode()
    imageData = self.inputSelector.currentNode().GetImageData()
    range = imageData.GetScalarRange()
    self.imageWindowSliderWidget.minimum = float(range[0])
    self.imageWindowSliderWidget.maximum = float(range[1])
    self.imageLevelSliderWidget.minimum = float(range[0])
    self.imageLevelSliderWidget.maximum = float(range[1])
    windowValue = displayNode.GetWindow()
    levelValue = displayNode.GetLevel()
    self.imageWindowSliderWidget.value = windowValue
    self.imageLevelSliderWidget.value = levelValue

#
# ImageGrayScaleViewerLogic
#

class ImageGrayScaleViewerLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() == None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    return True

  def run(self, inputVolume, imageWindow, imageLevel):
    """
    Run the actual algorithm
    """

    return True


class ImageGrayScaleViewerTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ImageGrayScaleViewer1()

  def test_ImageGrayScaleViewer1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = ImageGrayScaleViewerLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
