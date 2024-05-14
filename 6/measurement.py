import RPi.GPIO as rp
import time as tm
import matplotlib.pyplot as plt
import numpy as np

def dectobin( dec ):
    bi = bin( dec )[2:].zfill(8)
    bi = [int( i ) for i in list( bi )]
    return bi

def adc( dac ):
    l = 0
    r = 255
    m = 0

    while l < r:
        m = ( l + r ) // 2

        bi = dectobin( m )

        for i in range( 8 ):
            rp.output( dac[i], bi[i] )

        tm.sleep( 0.01 )
        
        cmp = rp.input( comp )

        if cmp == 0:
            l = m + 1
        else:
            r = m
    
    print( m )

    return l

def adcv( dac ):
    return adc( dac ) * 3.3 / 255

def vol( leds, volts ):
    
    i = ( volts / 3.3 ) // (1 / 8)
    i = int( i )

    rp.output( leds[:8 - i], 0 )
    rp.output( leds[8 - i:], 1 )



dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]

comp = 14
troyka = 13

rp.setmode( rp.BCM )

rp.setup( dac, rp.OUT )
rp.setup( comp, rp.IN )
rp.setup( leds, rp.OUT )
rp.setup( troyka, rp.OUT, initial=1 )

def do_plot( ):
    n = adc( dac )

    listn = []

    while n < 243:
        n = adc( dac )
        listn.append( n )
        print( n )

    rp.output( troyka, 0 )

    while n >= 1:
        n = adc( dac )
        listn.append( n )
        print( n )
    
    return listn
    

tstart = tm.time( )

listn = do_plot()

tend = tm.time( )

dt = ( tend - tstart ) / len( listn )

listv = [ i * 3.3 / 255 for i in listn ]

listt = [ i * dt for i in range( len( listv ) ) ]

plt.plot( listt, listv )

plt.ylabel( 'U, В' )

plt.xlabel( 't, сек' )

f = open( 'data.txt', 'w' )

for i in listn:
    f.write( str( i ) + '\n' )

f.close()

f = open( 'settings.txt', 'w' )

f.write( 'Шаг дискретизации ' + str( dt ) + 'сек ' +
         'Шаг квантования ' + str( 1 / 255 ) + 'В\n' )

f.close( )

plt.savefig( 'plt.png' )