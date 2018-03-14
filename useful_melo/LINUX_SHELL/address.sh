#!/bin/sh
sed -i 's/,/chey/' address.csv
sed -i 's/,/，/g' address.csv
sed -i 's/chey/,/' address.csv
