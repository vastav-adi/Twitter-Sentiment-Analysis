# import packages
import os
import pandas as pd

# start date and end date input (format : 2018-01-30)
start_date = 'XXXX-XX-XX'
end_date = 'XXXX-XX-XX'

# the search term
search_terms = ["'india politics'", "'india prime minister'", "'india chief minister'", "'india pm'", "'india cm'",
               "'india elections'", "'india vote party'", "'india bjp'", "'india inc'", "'india bsp'", "'india tmc'",
               "'india cpi'", "'india ncp'", "'india aam aadmi party'", "'india aiadmk'", "'india aifb'",
               "'india ainrc'", "'india aiudf'", "'india ajsu'", "'india asom gana parishad'", "'india aipfp'",
               "'india bjd'", "'india bpf'", "'india gfp'", "'india hspdp'", "'india inld'", "'india iuml'", 
               "'india jknc'", "'india jknpp'", "'india jkpdp'", "'india janta dal'", "'india jharkhand vikas morcha'",
               "'india kjp'", "'india kerala congress'", "'india ljp'", "'india mns'", "'india mgp'", "'india mnf'",
               "'india npf'", "'india congress'", "'india npp'", "'india ndpp'", "'india dmdk'", 
               "'india people democratic alliance'", "'india rjd'", "'india rld'", "'india rlsp'", "'india samajwadi party'",
               "'india akali dal'", "'india shiv sena'", "'india trs'", "'india tdp'", "'india united democratic party'",
               "'india ysrc'", "'india aimim'", "'india dmk'", "'india upa'", "'india nda'","'india pattali makkal'",
               "'india jharkhand mukti morcha'","'india mizoram people conference'", "'india mizoram people conference'",
               "'india people party arunachal'", "'india revolutionary socialist party'","'india sikkim democratic front'",
               "'india sikkim krantikari morcha'","'india marxist forward bloc'"]

# issuing queries for each term in the list

for i in range(0, len(search_terms)):

	term = search_terms[i]
	# constructing the query
	query = "python Exporter.py --since " + start_date + " "
	query = query + "--until " 
	query = query + end_date + " "
	query = query + "--toptweets "
	query = query + "--querysearch " 
	query = query + term

	# firing the query
	os.system(query)

	# moving and renaming the output file
	oname = 'data_fetch/out' + str(i+1) + '.csv'
	os.rename('output_got.csv', oname)

# merging all the csv files into one
fdata = pd.read_csv('data_fetch/out1.csv', delimiter = '|', error_bad_lines=False)
for i in range(1, len(search_terms)):
	oname = 'data_fetch/out' + str(i+1) + '.csv'
	data_l = pd.read_csv(oname, delimiter = '|', error_bad_lines=False)
	fdata = fdata.append(data_l)

# writing the final csv to disk
fdata = fdata.drop_duplicates()
fdata.to_csv('final_output.csv', sep = '|', index=False)
