import csv

LEADERBOARD_FILENAME = 'scoreboard.csv'
SCORE_TRACKER_FILENAME = 'scores.csv'

# Constants
SCOREBOARD_LENGTH = 10
NAME_INDEX = 0
SCORE_INDEX = 1
TIME_INDEX = 2

class FileManager( ):
   def __init__( self, leaderboardFilename, scoreTrackerFilename ):
      self.leaderboardFilename = leaderboardFilename
      self.scoreTrackerFilename = scoreTrackerFilename
      self.leaderboard = [ ]

      with open( self.leaderboardFilename, 'r' ) as file:
         reader = csv.reader( file )
         for row in reader:
            if row != []:
               self.leaderboard.append( row )
         file.close( )
   
   def getLeaderboard( self ):
      return self.leaderboard

   def checkHighScore( self, newScore ):
      if len( self.leaderboard ) < SCOREBOARD_LENGTH or \
         newScore > int( self.leaderboard[ -1 ][ SCORE_INDEX ] ):
         # New highscore, take in name from player
         name = input( "Name: " )

         # Take off the last element and insert the new score
         if len( self.leaderboard ) >= SCOREBOARD_LENGTH:
            del self.leaderboard[ -1 ]
         self.leaderboard.append( [ name, newScore ] )
         
      # Sort the leaderboard by the SCORE_INDEX coloumn
      self.leaderboard = sorted( self.leaderboard, reverse=True, key=lambda x:int( x[ SCORE_INDEX ] ) )
      with open( self.leaderboardFilename, 'w' ) as file:
         writer = csv.writer( file )
         writer.writerows( self.leaderboard )
         
         file.close( )
         
   def recordScore( self, score, elapsedTime, time ):
      with open( self.scoreTrackerFilename, 'a' ) as file:
         writer = csv.writer( file )
         writer.writerow( [ score, elapsedTime, time ] )
         
         file.close( )
         