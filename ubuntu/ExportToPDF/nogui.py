
import sys
import os
import shutil
import datetime

from PyPDF2 import PdfMerger

from qgis.core import (
     QgsProcessingFeedback,
     QgsProcessingContext,
     QgsApplication, 
     QgsProject, 
     QgsLayoutExporter
)

# path to qgis map folder
qgz_path = '/usr/share/pyshared/exportToPDF'
# path to pdf output folder
pdf_path = qgz_path
# path to website pdf output folder
web_path = '/var/www/firealertmap/pdf'
# path to PyGIS qgis-ltr packages folder
prefix_path = '/usr'
# path to PyGIS qgis-ltr plugins folder
plugins = '/usr/share/qgis/python/plugins'

# convert layout in QGIS map document to pdf
def makePDF(section):
    
    output =  os.path.join(qgz_path, section + '.pdf')
    web_output =  os.path.join(web_path, section + '.pdf')
    
    #print('section: ' + section)
    
    params = {
    'LAYOUT':section,
    'LAYERS':None,
    'DPI':None,
    'FORCE_VECTOR':False,
    'GEOREFERENCE':True,
    'INCLUDE_METADATA':True,
    'DISABLE_TILED':False,
    'SIMPLIFY':False,
    'TEXT_FORMAT':0,
    'SEPARATE_LAYERS':False,
    'OUTPUT':output
    }

    
    feedback = QgsProcessingFeedback()
    context = QgsProcessingContext()
    context.setProject(project)
    
    result = processing.run("native:printlayouttopdf", params, context=context, feedback=feedback)
    
    # copy to website pdf folder
    shutil.copyfile(output, web_output)
    #print('result: ' + str(result))

# merge pdf sections maps into one pdf file 
def mergePDF(sections):
        
    merger = PdfMerger()
    for y in sections:
        pdf = os.path.join(pdf_path, y + '.pdf')
        # print('pdf: ' + str(pdf))
        merger.append(pdf)
    
    mergeFile = os.path.join(pdf_path, "Fire_Severity_Maps.pdf")
    merger.write(mergeFile)
    merger.close()
    
    # copy to website pdf folder
    webFile = os.path.join(web_path, "Fire_Severity_Maps.pdf")
    shutil.copyfile(mergeFile, webFile)
    
# set no GUI setting
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# use qgis-ltr packages to export to pdf
QgsApplication.setPrefixPath(prefix_path, True)
qgs = QgsApplication([], False)
qgs.initQgis()

# reference to qgis-ltr plugins for processing package/module
sys.path.append(plugins)

import processing
from processing.core.Processing import Processing
Processing.initialize()

# read QGIS map document
project = QgsProject()
isproject = project.read(os.path.join(qgz_path,'FireMap.qgz'))

# call pdf maker for each layout
layouts = ['Northern_California', 'Sacramento', 'Central_Valley']
for y in layouts:
    makePDF(y)
   
# merge pdf section files into one pdf    
mergePDF(layouts)

# exit
QgsProject.instance().clear()
QgsApplication.exitQgis()
print(str(datetime.datetime.now()))