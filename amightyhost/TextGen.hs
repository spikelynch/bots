module TextGen (
  TextGen
  ,runTextGen
  ,word
  ,choose
  ,list
  ,perhaps
  ,rep
  ,randrep
  ,smartjoin
  ,upcase
  ,loadOptions
  ) where

import Control.Applicative
import Control.Monad (liftM, ap, forM_)
import Data.List (intercalate)
import Data.Char (toUpper)
import qualified Data.Text as T
import qualified Data.Text.IO as Tio
import System.Random


newtype TextGen s a = TextGen { runTextGen :: s -> ( a, s ) }

instance (RandomGen s) => Monad (TextGen s) where
  return x = TextGen $ \s -> ( x, s )
  (TextGen h) >>= f = TextGen $ \s -> let ( a, newTextGen ) = h s
                                          (TextGen g) = f a
                                      in g newTextGen
                                     
                                     

instance (RandomGen s) => Functor (TextGen s) where
  fmap = liftM
  
instance (RandomGen s) => Applicative (TextGen s) where
  pure = return
  (<*>) = ap    

-- Note that word returns a list of strings 

word :: (RandomGen g) => [Char] -> TextGen g [[Char]]
word a = return [ a ]

                              
choose :: (RandomGen g) => [ TextGen g a ] -> TextGen g a
choose options = TextGen $ \s -> let ( i, s' ) = randomR (0, (length options) - 1 ) s
                                     (TextGen optf) = options !! i
                                 in optf s'
                                   
-- needed: choose n (to get multiple items from the same list without
-- repeats

list :: (RandomGen g) => [ TextGen g [ a ] ] -> TextGen g [ a ]
list []     = TextGen $ \s -> ( [], s )
list (o:os) = TextGen $ \s -> let (TextGen ofn) = o
                                  (TextGen osfn) = list os
                                  ( a, s' ) = ofn s
                                  ( as, ss' ) = osfn s'
                              in ( a ++ as, ss' )

--rep: Repeat a TextGen n times

rep :: (RandomGen g) => Int -> TextGen g [ a ] -> TextGen g [ a ]
rep n s = list $ take n $ repeat s

-- randrep : Repeat a Textgen (min, max) times

randrep :: (RandomGen g) => (Int, Int) -> TextGen g [ a ] -> TextGen g [ a ] 
randrep (min, max) s1 = TextGen $ \s -> let ( n, s' ) = randomR (min, max) s
                                            (TextGen s2f) = rep n s1
                                        in s2f s'
                                           
-- perhaps: 
perhaps :: (RandomGen g) => (Int, Int) -> TextGen g [ a ] -> TextGen g [ a ]
perhaps (n, m) s1 = TextGen $ \s -> let ( n1, s' ) = randomR (0, m) s
                                        (TextGen s2f) = if n1 > n then list [] else s1
                                        in s2f s' 

loadOptions :: (RandomGen g) => [Char] -> IO (TextGen g [[Char]])
loadOptions fname = do
  contents <- fmap T.lines (Tio.readFile fname)
  return $ choose $ map ( word . T.unpack ) contents
  

smartjoin :: [ [Char] ] -> [Char]
smartjoin ws = smartjoin_r $ undupe ws

undupe :: [[Char]] -> [[Char]]
undupe (w:x:ys) = if w == "," && x == "," then undupe(x:ys) else w:undupe(x:ys)
undupe (ws)     = ws

smartjoin_r :: [[Char]] -> [Char]
smartjoin_r (w:x:ys) = case x of
  "-" -> w ++ "-" ++ smartjoin_r(ys)
  "," -> case ys of
    [] -> w ++ "."
    otherwise -> w ++ ", " ++ smartjoin_r(ys)
  otherwise -> w ++ " " ++ smartjoin_r(x:ys)
smartjoin_r (w:xs) = case xs of
  [] -> w ++ "."
  otherwise -> w ++ " " ++ smartjoin_r(xs)
smartjoin_r [] = []



upcase :: [Char] -> [Char]
upcase (x:xs) = (toUpper x):xs
upcase []     = []
