dir="images"

for file in $dir/*
do
    echo $file
    date=$(exiftool -time:DateTimeOriginal -d '%Y%m%d%H%M.%S' -s3 "$file")
    if [[ -z $date ]]; then
        date="202403271938"
    fi
    echo $date
    touch -mat $date "$file"
    adb push "$file" /sdcard/Download/
done