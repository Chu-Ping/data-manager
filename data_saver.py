import sys
from database import Database

if __name__ == "__main__":
    db = Database()

    if '--base' in sys.argv:
        db.create_base(sys.argv[1])
    else:
        arg = []
        for key in list(db.metadata.keys())[1:]:
            arg.append( input(key + ": ") )
        db.create([sys.argv[1]] + arg, sys.argv[1])


