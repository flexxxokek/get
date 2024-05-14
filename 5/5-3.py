import RPi.GPIO as rp
import time as tm

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
    
    print( m * 3.3 / 255 )

    return l * 3.3 / 255

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
rp.setup( troyka, rp.OUT, initial=1 )
rp.setup( comp, rp.IN )
rp.setup( leds, rp.OUT )



while True:
    volt = adc( dac )
    vol( leds, volt )
    
