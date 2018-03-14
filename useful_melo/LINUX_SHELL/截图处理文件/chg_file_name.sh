#bin/sh
for item in `ls *.png`
do
   old_name=$item
   item=${item:0:10}
   alia=${item:8:9}
   echo $alia
   mv $old_name  $alia"日.png"
done