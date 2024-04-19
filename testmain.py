from atrox3d.simplegit.__main__ import main
import sys
print(sys.argv)
sys.argv.extend('branch updatemaster'.split())
main()