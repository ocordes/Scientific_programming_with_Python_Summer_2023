import sys

from rpn_sim import RpnAstroFiles

# main

rpn = RpnAstroFiles()

rpn(sys.argv[1:-1], sys.argv[-1])
