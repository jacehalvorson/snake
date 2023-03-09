from importlib import util

SCORE = 0
ELAPSED_TIME = 1
TIME = 2

class DataAnalysis:
   def __init__( self, scores_filename ):
      checkPackagesInstalled = [ 'matplotlib', 'pandas' ]
      for package in checkPackagesInstalled:
         if util.find_spec( package ) is None:
            print( f'You must have {package} installed for this feature. Install it with:\npip install {package}' )
            exit( )
      
      import pandas as pd
      
      self.dataframe = pd.read_csv( scores_filename )
      
   def showPlot( self, x, y ):
      import matplotlib.pyplot as plt

      parameterList = [ x, y ]
      for i in range( len( parameterList ) ):
         if parameterList[ i ] == SCORE:
            parameterList[ i ] = 'Score'
         if parameterList[ i ] == ELAPSED_TIME:
            parameterList[ i ] = 'Elapsed Time'
         if parameterList[ i ] == TIME:
            parameterList[ i ] = 'Time (CST)'

      self.dataframe.plot( x=parameterList[ 0 ], y=parameterList[ 1 ] )