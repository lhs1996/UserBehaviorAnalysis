# CSE 160 Project 
# June 1 2018 
# Huanshu Liu and Angel Chen 
# Buyer Behavior Analysis 
# Key Words: Regression Analysis, Data from Aliyun 
# Import linear regression modules 
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab
import csv 
import operator 
from numpy import arange,array,ones
from scipy import *
import pickle
import statsmodels.api as sm
from scipy import stats
# NON linear regression 
from sklearn.preprocessing import PolynomialFeatures 
from sklearn import linear_model 

# Read in the csv files 
# csv file names: user_actions.csv & user_demographics.csv 
def read_csv(path):
	"""
	Reads the CSV file at path, and returns a list of rows from the file.
	Parameters: path: path to a CSV file. 
	Returns: list of dictionaries: Each dictionary maps the columns of the CSV file
	to the values found in one row of the CSV file. 
	"""
	output = []
	csv_file = open(path)
	for row in csv.DictReader(csv_file):
		output.append(row)
	csv_file.close()    
	return output

def string_int(output_list): 
	"""
	To switch the type of output list's value
	Return with integer-type of values 
	"""
	int_lst = [] 
	for dictionary in output_list:
		# Eliminate the case of NULL 
		if "" not in dictionary.values(): 
			dictionary_with_ints = dict((k, int(v)) for k,v in dictionary.iteritems())
			int_lst.append(dictionary_with_ints)
	return int_lst 

def string_int_dict(dictionary):
	"""
	To convert string-type key and values in dictionaries into integer-type 
	"""
	for key in dictionary:
		if "" not in dictionary.values(): 
			dictionary_with_ints = dict((int(k), int(v)) for k,v in dictionary.iteritems())
	return dictionary_with_ints 


# Get a group of unique users from a large pool of dupliacted user_ids 
def get_user_set(output): 
	"""
	Input: Given the list of dictionaries
	Output: Return a set of users with the key 'user_id'
	"""
	user_set = set()
	for dictionary in output:
		user_set.add(dictionary['user_id'])
	return user_set
				 

# Notes action scores meaning: 
# Action_type = 0, means the buyers only browsed the web page
# Action_type = 1, means the buyers put the item into shopping carts 
# Action_type = 2, means the buyers did purchase the item 
# Action_type = 3, means the buyers saved the item into favorites 
# We are computing the total scoare of action_type 

def user_action_total(output): 
	"""
	Input: Output list of dictionaries 
	Output: Return a dictionary with the sum of action scores for every user
	""" 
	new_dict = {} 
	user_set = get_user_set(output)
	for user in user_set:
		new_dict[user] = sum(dicts['action_type'] for dicts in output if dicts['user_id'] == user)
	return new_dict 


# To get the gender information from each users 
# Gender = 0 means female 
# Gender = 1 means male 
# Gender = 2 means unknown 
def user_gender(output): 
  	"""
  	Input: output (a long list of dictionaries)
  	Output: a dictionary mapping all unique users to their gender information 
  	"""
  	new_dict = dict()
  	for dictionary in output:
		new_dict[dictionary['user_id']] = dictionary['gender']
  	return new_dict
	
# To get the age range information from each users 
# Age = 1 means less than 18 years old 
# Age = 2 means [18, 24]
# Age = 3 means [25, 29]
# Age = 4 means [30, 34]
# Age = 5 means [35, 39]
# Age = 6 means [40, 49]
# Age = 7, 8 means >= 50 
# Age = NULL, means unknown 

def user_age_range(output): 
  	"""
  	Input: output list 
  	Output: return a dictionary from user map to age range
  	"""
  	new_dict = dict()
  	for dictionary in output:
  		new_dict[dictionary['user_id']] = dictionary['age_range']
  	return new_dict


# From the big dataset, extract a single user's info
def get_one_user_info(output,user): 

  	"""
  	Input: output list, and a specific id of user 
  	Output: a list of dictionary that includes all actions from one specific user 
  	"""

 	new_list = []
  	for dictionary in output:
		if dictionary['user_id'] == user:
	  		new_list.append(dictionary)
  	return new_list

# For an user, we compare all categories and find out the one with the maximum action_score
def compare_cat(one_user_output):
  	"""
  	Input: getting output of a list of dictionaries for a specific user
  	Output: 
 	Return a number, (an integer of category ID) the category in which the user shopped the most 
  	Note that if action_score is 0 for a user, return None, there is no favorite shop for him.
  	"""

  	new_dict = dict()
  	for dictionary in one_user_output:
  		if dictionary['cat_id'] in new_dict:
  			new_dict[dictionary['cat_id']] += dictionary['action_type']
  		else:
  			new_dict[dictionary['cat_id']] = dictionary['action_type']

  	max_score = 0
  	max_cat = None
  	for key in new_dict.keys():
  		if max_score == None or new_dict[key] > max_score:
  			max_score = new_dict[key]
  			max_cat = key
  	if max_score == 0:
  		return None
  	return max_cat

# Find out the user's favorite category, the one with the higher action_score 
def user_cat(output): 
  	"""
  	Input: output list 
  	Output: if action_score = 0 for a user, return NONE, there is no favorite shop for him. 
  	Otherwise, return a dictionary mapping user_id to his favorite shops in seller_ID (an integer). 
  	"""
  	new_dict = dict()
  	user_set = get_user_set(output)
  	for user in user_set:
		list_of_the_user = get_one_user_info(output,user)
		# get the most favorible store 
		category = compare_cat(list_of_the_user)
		new_dict[user] = category
  	return new_dict

# ingedients for regression analysis: 
# user_cat
# user_gender
# user_age_range
# user_action_total
# To prepare for running regression models on the effect of age range on action types 
# Utilize this function for all three variables, age, gender, category 
def variable_to_action_total(variable_dict, user_action_total_dict): 
  	"""
  	Input: 
  	Two parameters: a dictionary from user mapping to the specific varibles, and a dictionary from user mapping to action_scores 
  	Output: return a dictionary map from variables to total action score
  	"""
	new_dict = dict()
	for key in variable_dict.keys():
		if user_action_total_dict.has_key(key) and variable_dict[key] != None:
		#if variable_dict[key] !=  None: 
			if variable_dict[key] in new_dict.keys(): 
				new_dict[variable_dict[key]] += user_action_total_dict[key]
			else: 
				new_dict[variable_dict[key]] = user_action_total_dict[key]
	return new_dict


# To create the a list for x-axis in regression model, and a list for y-axis 
# To prepare it for the later function linear_regression(nested_list)
def dictionary_to_two_lists(a_dictionary): 
	"""
	Input: get a dictionary 

	Output: return a nested list in which: 
	  list_x contains the keys of the dictionary,
	  list_y contains the values of the dictionary
	"""
	nested_list = [0,0]
	list_x = []
	list_y = []
	for key in a_dictionary.keys():
		list_x.append(key)
		list_y.append(a_dictionary[key])
	nested_list[0] = list_x
	nested_list[1] = list_y
	return nested_list

def write_to_csv(input_dict, descriptions): 
    """
    To convert a long dictionary into a new csv file 
    """ 
    with open(str(descriptions) + ".csv", 'wb') as myfile:
    	writer = csv.writer(myfile)
    	for key, value in input_dict.items():
    		writer.writerow([key, value])

def csv_to_dict(filename):
	"""
	To convert a csv back into a dictionary 
	"""
	with open(str(filename), "rb") as myfile: 
		reader = csv.reader(myfile)
		my_dict = dict(reader)
	return my_dict
 

def linear_regression(nested_list, descriptions, x_name, y_name):
	"""
	Input: Parameter: a nested list contains two lists: list_x and list_y 
	Output: Return None 
	print out the result from linear regression, in which b is the beta zero, intercept 
	and a is the estimated coefficient, indicating the effect of change in x values 
	"""

	lin_reg = LinearRegression()
	xvals = np.reshape(nested_list[0],(len(nested_list[0]),1))
	yvals = nested_list[1]
	lin_reg.fit(xvals,yvals)
	b = lin_reg.intercept_
	a = lin_reg.coef_[0]
	print "coeffienct: ", str(a), "intercept", str(b)

	X2 = sm.add_constant(xvals)
	est = sm.OLS(yvals, X2)
	est2 = est.fit() 
	print(est2.summary())

	scatterplot(nested_list[0], nested_list[1], descriptions, x_name, y_name)
	fitted_line(a, b, descriptions, nested_list, x_name, y_name)
	bar_chart(nested_list, descriptions, x_name, y_name)
	
	# Generate Latex table code 
	# for table in est2.summary().tables:
		# print(table.as_latex_tabular())

# To plot the fitted value 
# Plot for age distribution 
def bar_chart(nested_list, descriptions, x_name, y_name):
	plt.clf() 
	rect1 = nested_list[1]
	rect2 = nested_list[0]
	plt.bar(rect2, rect1, align = "center", alpha = 0.5)
	plt.ylabel(y_name)
	plt.xlabel(x_name)
	plt.title(descriptions) 
	plt.legend() 
	plt.savefig(str(descriptions) + "_bar.png") 
	plt.show() 

def fitted_line(slope, intercept, descriptions, nested_list, x_name, y_name):
	"""
	To plot the fiited line in a scatter plot 
	Return None 
	"""
	x = arange(0, 11)
	y = range(0, 15)
	xs = nested_list[0]
	ys = nested_list[1]
	linear_line = slope * x + intercept 
	plt.clf() 
	plt.xlabel(x_name)
	plt.ylabel(y_name)
	plt.legend() 
	plt.plot(xs, ys) 
	plt.savefig(str(descriptions) + "_fitted.png") 
	plt.show() 

# Visualization 
def scatterplot(xs, ys, descriptions, x_name, y_name):
	""" 
	Input: two lists of numbers as x and y variables 
	Ouput: a scatter plot 
	""" 
	plt.clf() 
	plt.title(str(descriptions))
	plt.ylim(-20000, 20000) 
	plt.xlim(-10, 10)
	plt.xlabel(x_name)
	plt.ylabel(y_name) 
	plt.scatter(xs, ys)
	plt.savefig(str(descriptions) + "_scatter.png") 
	plt.show()
  
def pie_chart(sizes, descriptions):
	"""
	Generate gender info into pie charts 
	"""
	plt.clf() 
	labels = 'female', "male"
	colors = ['yellowgreen', 'lightcoral']
  	plt.pie(sizes, autopct = '%1.1f%%', labels = labels, colors = colors, shadow = True, startangle = 90)
  	plt.title(str(descriptions))
 	plt.savefig(str(descriptions) + "_piechart.png")
 	plt.axis('equal')
  	plt.show()


def non_linear_regression(nested_list, descriptions, x_name, y_name): 
	"""
	Degree = 2 non-linear regression
	"""
	
	xvals = np.reshape(nested_list[0],(len(nested_list[0]),1))
	yvals = nested_list[1]
	regression = LinearRegression()
	regression.fit(xvals,yvals, 2)
	b = regression.intercept_
	a = regression.coef_[0]
	print "Non_linear coeffienct: ", str(a), "Non_linear intercept", str(b)

def main():
	print "Our project starts!"
	# We first perform the merging process with merge.py, and then start this main function  
	# user_list_1 = read_csv("user_log_format1.csv")
	# user_list_2 = read_csv("user_info_format1.csv")
	# user_lst = merge(user_list_1, user_list_2)
	# write_to_csv(input_dict, descriptions)

	user_lst = read_csv("merged.csv")
	user_lst = string_int(user_lst)
	unique_user = get_user_set(user_lst)
	print "How many users do we have in our data set? " + " We have " + str(len(unique_user)) + " unique users."
	# print "We start finding lists of action info."
	# user_to_action_score = user_action_total(user_lst)
	# action_csv = write_to_csv(user_to_action_score, "user_to_action")
	# print "GET DONE with action csv write-up! "

	# Since the process to compute action_score and favorite category are very slow
	# So we only compute them once and save the result into a seperate csv file 

	user_to_action_score = csv_to_dict("user_to_action.csv")
	user_to_action_score = string_int_dict(user_to_action_score)
	
	user_to_gender_info = user_gender(user_lst)	
	user_to_age_info = user_age_range(user_lst)

	user_to_favorite_category = csv_to_dict("user_to_favorite_category.csv")
	user_to_favorite_category = string_int_dict(user_to_favorite_category)

	print 
	print "Regression Results are as follows: " 
	print "Effect of age on users: " 
	reg1_dict = variable_to_action_total(user_to_age_info, user_to_action_score)
	reg1_dict_csv = write_to_csv(reg1_dict, "reg1_dict")
	reg1_lst = dictionary_to_two_lists(reg1_dict)
	reg1 = linear_regression(reg1_lst, "Age Effect", "Age", "Action_score")

	print "Effect of gender on users: " 
	reg2_dict = variable_to_action_total(user_to_gender_info, user_to_action_score)

	gender_ratio = [reg2_dict[0], reg2_dict[1]]
	pie_chart(gender_ratio, "Gender Distribution")

	reg2_lst = dictionary_to_two_lists(reg2_dict)
	reg2 = linear_regression(reg2_lst, "Gender Effect", "Gender", "Action_score")

	print "Effect of category on users: " 
	reg3_dict = variable_to_action_total(user_to_favorite_category, user_to_action_score)
	reg3_lst = dictionary_to_two_lists(reg3_dict)
	reg3 = linear_regression(reg3_lst, "category Effect", "Category", "Action_score")


	print "Non-linear regression results: "
	reg1_non_linear = non_linear_regression(reg1_lst, "Age non_linear_regression", "Age", "Action_score")


	print "Program is done; Thanks for reading through our project!"

if __name__ =="__main__": 
	main () 

			
	


		

			  

	  