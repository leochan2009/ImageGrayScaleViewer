cmake_minimum_required(VERSION 2.8.9)

project(ImageGrayScaleViewer)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/ImageGrayScaleViewer")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Longquan Chen (BWH/Harvard)")
set(EXTENSION_DESCRIPTION "Extension to view the gray scale of the image")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/ImageGrayScaleViewer.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/ImageGrayScaleViewer/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(ImageGrayScaleViewer)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
