All final output csv files are in generated_files directory
All scripts and required dataset are in the the SCRIPTS directory

Following libraries required to run code:
pip install pandas warnings os numpy statsmodels
#statsmodels for statstical testing module
#also requirements.txt is inlcuded in zip
#To run all scripts, we need to run only assign2.sh, which generates all required csv files.
chmod +x assign.sh
./assign2.sh

#to run Q1
./percent-india.sh
#to run Q2
./gender-india.sh
# to run Q3
./geography-india.sh
# to run Q4 part(a)
./3-to-2-ratio.sh
# to run Q4 part(b)
./2-to-1-ratio.sh
# to run Q5
./age-india.sh
# to run Q6
./literacy-india.sh
# to run Q7
./region-india.sh
#to tun Q8
./age-gender.sh
# to run Q9
./literacy-gender.sh

#----------------
