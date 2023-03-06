from importlib.util import find_spec
checkPackageInstalled = 'pygame'
if find_spec( checkPackageInstalled ) is None:
   print( f'Python extension {checkPackageInstalled} must be installed to run this program. Install it with:\npip install {checkPackageInstalled}' )
   exit( )
import pygame
from math import floor
import random

CLOCK_RATE = 15

# SETTINGS
CYCLIC_BORDER = False
STARTING_LENGTH = 1

# Dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
FRAME_WIDTH = 400
FRAME_HEIGHT = 400
BORDER_SIZE = 20
BLOCKS_IN_ROW = 22
BLOCKS_IN_COL = BLOCKS_IN_ROW
GRID_SIZE = 20

# Positions
FRAME_OFFSET_X = 40
FRAME_OFFSET_Y = 120

STARTING_X = 1
STARTING_Y = 1

# Colors
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
RED = ( 255, 0, 0 )
GREEN = ( 0, 255, 0 )
BLUE = ( 0, 0, 255 )
CYAN = ( 0, 255, 255 )
YELLOW = ( 255, 255, 0 )
PURPLE = ( 255, 0, 255 )
BACKGROUND_COLOR = CYAN
SNAKE_COLOR = RED
APPLE_COLOR = YELLOW

# Directions
UP = ( 0, -1 )
RIGHT = ( 1, 0 )
DOWN = ( 0, 1 )
LEFT = ( -1, 0 )
STARTING_DIRECTION = DOWN

# States
GAME = 0
GAME_OVER = 1
MENU = 2

# Global variables
blockList = [ ]
coloredBlocks = [ ( floor( GRID_SIZE/2 ), floor( GRID_SIZE/2 ) ) ]
snakeLength = 3
apple = ( 5, 5 )
programState = GAME

class Button:
   def __init__( self, screen, text, width, height, pos ):
      centerPos = ( pos[ 0 ] - width/2, pos[ 1 ] - height/2 )
      self.topRect = pygame.Rect( centerPos, ( width, height ) )
      self.topColor = BLACK
      
      # text
      font = pygame.font.Font( 'freesansbold.ttf', 32 )
      self.textSurface = font.render( text, True, WHITE )
      self.textRect = self.textSurface.get_rect( )
      self.screen = screen

   def draw( self ):
      pygame.draw.rect( self.screen, self.topColor, self.topRect, border_radius=4 )
      self.screen.blit( self.textSurface, self.topRect )

   def checkClick( self ):
      mouseX, mouseY = pygame.mouse.get_pos( )
      correctedMousePos = ( mouseX - FRAME_OFFSET_X - BORDER_SIZE, mouseY - FRAME_OFFSET_Y - BORDER_SIZE )

      return self.topRect.collidepoint( correctedMousePos )

class Text:
   def __init__( self, screen, text, font, fontSize, color, bg_color, pos ):
      font = pygame.font.Font( font, fontSize )
      self.textSurface = font.render( text, True, color )
      self.textRect = self.textSurface.get_rect( )
      self.textRect.center = pos
      self.screen = screen

   def draw( self ):
      self.screen.blit( self.textSurface, self.textRect )

def addTuples( tuple1, tuple2 ):
   if CYCLIC_BORDER:
      return ( ( tuple1[ 0 ] + tuple2[ 0 ] ) % GRID_SIZE, ( tuple1[ 1 ] + tuple2[ 1 ] ) % GRID_SIZE )
   else:
      return ( ( tuple1[ 0 ] + tuple2[ 0 ] ), ( tuple1[ 1 ] + tuple2[ 1 ] ) )

def initBlocks( surface ):
   for row in range( BLOCKS_IN_ROW ):
      blockList.append( [ ] )
      
      for col in range( BLOCKS_IN_COL ):
         block = pygame.Surface( ( FRAME_WIDTH/BLOCKS_IN_COL, FRAME_HEIGHT/BLOCKS_IN_ROW ) )
         block.fill( BACKGROUND_COLOR )
         surface.blit( block, ( col*20+1, row*20+1 ) )
         blockList[ row ].append( block )

def colorBlock( gameSurface, color, coordinates ):
   global blockList
   x, y = coordinates
   
   blockList[ x ][ y ].fill( color )
   gameSurface.blit( blockList[ x ][ y ], ( x*20+1, y*20+1 ) )

def moveSnake( gameSurface, direction ):
   global apple
   global snakeLength
   global coloredBlocks
   if len( coloredBlocks ) == 0:
      return
   
   # Add a block in the direction of motion
   nextBlock = addTuples( coloredBlocks[ -1 ], direction )
   ( x, y ) = nextBlock
   if nextBlock in coloredBlocks or x < 0 or x > GRID_SIZE-1 or y < 0 or y > GRID_SIZE-1:
      # Snake ran into itself or into border
      gameOver( gameSurface )
      return -1

   if nextBlock == apple:
      # Snake found the apple, re-randomize and add 1 to length
      randomBlock = ( random.randint( 0, GRID_SIZE-1 ), random.randint( 0, GRID_SIZE-1 ) )
      while randomBlock in coloredBlocks or randomBlock == apple:
         randomBlock = ( random.randint( 0, GRID_SIZE-1 ), random.randint( 0, GRID_SIZE-1 ) )
         
      snakeLength += 1
      apple = randomBlock

   coloredBlocks.append( addTuples( coloredBlocks[ -1 ], direction ) )
   
   # Erase the trailing blocks to maintain the length
   while len( coloredBlocks ) > snakeLength:
      del coloredBlocks[ 0 ]
      
   colorBlock( gameSurface, APPLE_COLOR, apple )
   
   global blockList
   for blockPos in coloredBlocks:
      colorBlock( gameSurface, SNAKE_COLOR, blockPos )

   return 0

def displayScore( screen ):
   global snakeLength
   
   score = Text( screen, str( snakeLength ), 'freesansbold.ttf', 64, WHITE, BLACK, ( SCREEN_WIDTH/2, 60 ) )
   score.draw( )

def gameOver( gameSurface ):
   global programState
   programState = GAME_OVER
   
   # font = pygame.font.Font( 'freesansbold.ttf', 32 )
   # text = font.render( 'Game Over', True, WHITE, BLACK )
   # textRec = text.get_rect( )
   # textRec.center = ( FRAME_WIDTH/2, FRAME_HEIGHT/2 - 30 )
   # gameSurface.blit( text, textRec )
   
   global replayButton
   replayButton = Button( gameSurface, 'Play Again', 170, 35, ( FRAME_WIDTH/2, FRAME_HEIGHT/2 ) )
   replayButton.draw( )

def resetGame( ):
   global programState
   global snakeLength
   global coloredBlocks
   global apple
   global direction
   
   programState = GAME
   snakeLength = STARTING_LENGTH
   # Initialize snake
   coloredBlocks = [ ( 1, 1 ) ]
   direction = STARTING_DIRECTION
   apple = ( random.randint( 3, GRID_SIZE-1 ), random.randint( 3, GRID_SIZE-1 ) )

def main( ):
   pygame.init( )
   
   screen = pygame.display.set_mode( [ SCREEN_WIDTH, SCREEN_HEIGHT ] )
   pygame.display.set_caption( 'Snake' )
   
   # Define the surfaces that will be placed on the screen
   borderSurface = pygame.Surface( ( FRAME_WIDTH+BORDER_SIZE, FRAME_HEIGHT+BORDER_SIZE ) )
   gameSurface = pygame.Surface( ( FRAME_WIDTH, FRAME_HEIGHT ) )
   
   # Initialize 2D block array
   initBlocks( gameSurface )
   
   # INitialize game variables
   resetGame( )
   
   clock = pygame.time.Clock( )
   
   global replayButton
   global direction
   numIterations = 0
   loop = True
   while loop:
      prevDirection = direction
      for event in pygame.event.get( ):
         # Process events before updating screen
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
               if prevDirection != DOWN:
                  direction = UP
                  
            elif event.key == pygame.K_RIGHT:
               if prevDirection != LEFT:
                  direction = RIGHT

            elif event.key == pygame.K_DOWN:
               if prevDirection != UP:
                  direction = DOWN

            elif event.key == pygame.K_LEFT:
               if prevDirection != RIGHT:
                  direction = LEFT
         
         elif event.type == pygame.MOUSEBUTTONDOWN:
            if programState == GAME_OVER and replayButton.checkClick( ):
               resetGame( )

         elif event.type == pygame.QUIT:
            loop = False
   

      if programState == GAME:
         # Fill the screen
         screen.fill( BLACK )
         # Fill the background (border) with white
         borderSurface.fill( WHITE )
         # Fill the inner surface
         gameSurface.fill( BACKGROUND_COLOR )

         moveSnake( gameSurface, direction )

         displayScore( screen )

         # Display the changes made
         borderSurface.blit( gameSurface, ( BORDER_SIZE/2, BORDER_SIZE/2 ) )
         screen.blit( borderSurface, ( FRAME_OFFSET_X, FRAME_OFFSET_Y ) )
      
      elif programState == GAME_OVER:
         loop = loop

      pygame.display.update( )
      clock.tick( CLOCK_RATE )
      numIterations += 1

   
   pygame.quit( )
   
if __name__ == '__main__':
   main( )