import exiftool
import shutil as sh
from datetime import datetime
import re
import os

directory = "images/"
files = [directory + f for f in os.listdir(directory)]
with exiftool.ExifToolHelper() as et:
    fails = 0
    for img in files:
        try:
            data = et.get_metadata(img)[0]
        except:
            print("No metadata extracted")
            continue

        filename = data["SourceFile"]
        print(filename)
        
        date = None
        try:
            if "WA" in filename:
                # find the date in the filename
                date = re.findall("[0-9]{8}", filename)[0]

                # and format date as "YYYY:MM:DD HH:MM:SS"
                date = f"{date[:4]}:{date[4:6]}:{date[6:]} 00:00:00"
            else:
                date = re.findall(r"(?:\d{8}_\d{6}|\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})[_.-]", filename)[0]
                # here we also have the time
                if date[8] == "_":
                    date = f"{date[:4]}:{date[4:6]}:{date[6:8]} {date[9:11]}:{date[11:13]}:{date[13:15]}"
                else:
                    date = f"{date[:4]}:{date[5:7]}:{date[8:10]} {date[11:13]}:{date[14:16]}:{date[17:19]}"
            
            #date = "2020:08:14 00:00:00"

            format_date = "%Y:%m:%d %H:%M:%S"
            maxi = datetime.now()
            mini = datetime.strptime("2010:01:01 00:00:00", format_date)
            date_obj = datetime.strptime(date, format_date)

            if date_obj > maxi or date_obj < mini:
                print("Date out of range")
                fails += 1
                continue
            
            print(date)
            if img[-3:] == "mp4":
                et.execute("-m", "-overwrite_original", f"-CreateDate={date}", img)
            else:
                et.execute("-overwrite_original", f"-DateTimeOriginal={date}", img)
        except IndexError:
            print("Date not found in filename")
            fails += 1
        
        if date:
            # move the file
            sh.move(img, "repaired/")

    print()    
    print(f"{fails} files failed to be repaired")
            
