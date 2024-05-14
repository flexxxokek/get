import RPi.GPIO as rp
import time as tm

def dectobin( dec ):
    b = bin( dec )[2:]
    b = [int(i) for i in b.zfill(8)]
    return b

def adc( dac ):
    tm.sleep( 3 )
    rp.output( dac, 0 )

    for i in range( 255 ):
        bi = dectobin( i )

        bi.reverse()

        for j in range( len( bi ) ):
            rp.output( dac[j], bi[j] )

        tm.sleep(0.01)
        cmp = rp.input( comp )

        if cmp == 1:
            print( bi, 3.3 / 255 * i )
            return

dac = [ 6, 12, 5, 0, 1, 7, 11, 8 ]

comp = 14
troyka = 13

print( dectobin( 14 ) )

rp.setmode( rp.BCM )

rp.setup( dac, rp.OUT )

rp.setup( troyka, rp.OUT, initial=1 )

rp.setup( comp, rp.IN )

while True:
    adc( dac )

