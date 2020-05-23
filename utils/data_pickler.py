import pickle
import json
import os

class Pickler():    
    
    def __init__(self, file="data/ydistricts_new_data.json"):
        self.file = file
        self.pickle_file = file.split('.')[0] + '.pickle'
    
    def toPickle(self):
        if not os.path.exists(self.pickle_file) or not os.stat(self.pickle_file).st_size:
            with open(self.pickle_file, "wb") as ph, open(self.file) as fh:
                print('Pickling...')
                posts_content = json.load(fh)
                pickle.dump(posts_content, ph, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            print("Pickle file is already there!")
            
    def unPickle(self):
        print("Unpickling...")
        with open(self.pickle_file, "rb") as fh:
            return pickle.load(fh)