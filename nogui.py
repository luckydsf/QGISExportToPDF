
import sys
import os
import shutil
import datetime
from dotenv import load_dotenv

load_dotenv() 

from pypdf import PdfWriter

from qgis.core import (
     QgsProcessingFeedback,
     QgsProcessingContext,
     QgsApplication, 
     QgsProject
)
#1. paths stored in .env
QGZ_PATH = os.getenv("QGZ_PATH") # path to qgis map folder
WEB_PATH = os.getenv("WEB_PATH") # path to website pdf output folder
QGIS_PATH = os.getenv("QGIS_PATH") # Path to QGIS folder
PYTHON_PLUGINS = os.getenv("PYTHON_PLUGINS") # Path to 'processing' folder
PDF_PATH = QGZ_PATH # path to pdf output folder


# 2. Add QGIS paths to sys.path so Python can find 'processing'
sys.path.append(QGIS_PATH + r"\python")
sys.path.append(PYTHON_PLUGINS)

# 3. Initialize QGIS Resources
QgsApplication.setPrefixPath(QGIS_PATH, True)
qgs = QgsApplication([], False) # False = Standalone (no GUI)
qgs.initQgis()

import processing
from processing.core.Processing import Processing
Processing.initialize()

project = QgsProject.instance()


# convert layout in QGIS map document to pdf
def makePDF(section):

    output =  os.path.join(QGZ_PATH, section + '.pdf')
    web_output =  os.path.join(WEB_PATH, section + '.pdf')
    
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
        
    #merger = PdfMerger()
    merger = PdfWriter()
    for y in sections:
        pdf = os.path.join(PDF_PATH, y + '.pdf')
        # print('pdf: ' + str(pdf))
        merger.append(pdf)
    
    mergeFile = os.path.join(PDF_PATH, "Fire_Severity_Maps.pdf")
    merger.write(mergeFile)
    merger.close()
    
    # copy to website pdf folder
    webFile = os.path.join(WEB_PATH, "Fire_Severity_Maps.pdf")
    shutil.copyfile(mergeFile, webFile)
    


def main():
    # read QGIS map document
    isproject = project.read(os.path.join(QGZ_PATH,'FireMap.qgz'))
    if not isproject:
        print('ERROR: Failed to load FireMap.qgz')
        return

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


if __name__ == "__main__":
    main()
    #run 'python-qgis-ltr nogui.py' from osgeo4W shell to make execute this script