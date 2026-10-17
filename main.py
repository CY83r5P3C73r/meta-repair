import exiftool
import os

directory = "images/"
files = [directory + f for f in os.listdir(directory)]
print(files)
with exiftool.ExifToolHelper() as et:
    for img in files:
        metadata = et.get_metadata(img)
        for d in metadata:
            print(d["SourceFile"])
            try:
                print(d["File:FileModifyDate"])
            except:
                print("No date found")
            print()
            
            # et.execute("-FileModifyDate=2000:01:01 10:00:00", img)
