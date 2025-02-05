#!/usr/bin/env python
# coding: utf-8
# Created by Xiao Guo
'''
The script is about downloading pdfs from Commercial use subset, Non-commercial use subset, and Custom license subset.
Since we had difficulty in downloading pdfs, this scripts save title in each paper for the future usage.
'''

import os
import re
import sys
import json
import glob
import argparse
import numpy as np
import requests			# package to retrive the pdf
import scholarly
import csv

from pathlib import Path

def csv_file_gen(dataset_name, json_file_dir):
	'''
	generate csv file for each dataset.
	'''
	json_file_path = os.path.join(json_file_dir, dataset_name)
	csv_file_name = dataset_name+'_title.csv'

	csv_file = Path(csv_file_name)
	exist_flag = csv_file.exists()
	csv_file_handler = open(csv_file_name, mode='a')
	csv_writer = csv.writer(csv_file_handler, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	if not exist_flag:	# add title
		csv_writer.writerow(['ID', 'Json id', 'Title', 'URL'])
	return json_file_path, csv_file_handler, csv_writer

def json_to_title(json_file_path, debug=False):
	'''
	to get title based on each json file.
	to return list containing all titles.
	'''
	json_name_list = []		# json name
	file_title_list = []	# article title
	no_title_count = 0

	## take json files from dataset.
	for idx, json_file in enumerate(glob.glob(os.path.join(json_file_path,"*.json"))):
		json_name_list.append(json_file)
		if debug:
			if idx == 3: break

	## get title from each json.
	for file_idx, file_name_cur in enumerate(json_name_list):
		with open(file_name_cur) as json_file:
			pdf_dict = json.load(json_file)
			title_cur = pdf_dict['metadata']['title']
			if title_cur == "":
				no_title_count += 1
				title_cur == "dummy"
			file_title_list.append(title_cur)
	assert len(file_title_list) == len(json_name_list), print(f"file_title_list \
		with len {len(file_title_list)} does not match json_name_list with len {len(json_name_list)}.")
	print(f"{no_title_count} files do not corresponding titles.")
	return json_name_list, file_title_list


def dump_csv(json_name_list, file_title_list, csv_writer):
	'''
	to dump information into target csv file.
	'''
	for idx, info_list in enumerate(zip(json_name_list, file_title_list)):
		write_list = [idx]
		write_list.extend(list(info_list))
		csv_writer.writerow(write_list)

def retriving_title(dataset_name, json_file_dir, debug_mode):
	'''
	downloading pdf given dataset_name.
	route: dataset path ==> json file ==> title ==> url ==> csv.
	'''
	## creating csv file.
	json_file_path, csv_file_handler, csv_writer = csv_file_gen(dataset_name, json_file_dir)

	## take "title" out of json
	json_name_list, file_title_list = json_to_title(json_file_path, debug_mode)

	## inject information into csv file.
	dump_csv(json_name_list, file_title_list, csv_writer)

	print(f"titles in {dataset_name} have been recorded.")

def main(json_file_dir, debug_mode, dataset_name):
	if dataset_name == "All":
		dataset_name_list = ["comm_use_subset", "noncomm_use_subset", "pmc_custom_license"]
	else:
		dataset_name_list = [dataset_name]

	for dataset_name_cur in dataset_name_list:
		retriving_title(dataset_name_cur, json_file_dir, debug_mode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloading pdfs from three datasets in COVID_19.')
    parser.add_argument('-d', '--json_file_dir', default='/nas/vista-ssd02/users/xiaoguo/COVID_research/Dataset_COVID19/',
    					help="the directory that contains json files.")
    parser.add_argument('-de', '--debug_mode', action='store_true', help="debug mode.")
    parser.set_defaults(debug_mode=False)
    parser.add_argument('-data', '--dataset_name', default="All", 
    					choices=['All', "comm_use_subset", "noncomm_use_subset", "pmc_custom_license"],
    					help="to choose dataset from choices.")
    args = parser.parse_args()
    main(json_file_dir=args.json_file_dir, debug_mode=args.debug_mode, dataset_name=args.dataset_name)
