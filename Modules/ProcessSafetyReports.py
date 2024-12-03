import numpy
import re

def process_safety_reports(list, damper=False):
	count = 0
	for report in list:
		if is_report_safe(report):
			count += 1
		elif (damper):
			badInd = get_first_bad_element(report)

			if is_report_safe(report[0:badInd-1]+report[badInd:]):
				count += 1
			elif is_report_safe(report[0:badInd]+report[badInd+1:]):
				count+=1

	return count

def is_report_safe(report):
	isAsc = numpy.sign(report[0] - report[len(report) - 1])
	if (isAsc == 0): # indicates first and last element are a duplicate
		return False

	for i in range(1, len(report)):
		diff = report[i - 1] - report[i]
		if (numpy.sign(diff) != isAsc) or abs(diff) > 3:
			return False
	return True

def get_first_bad_element(report):
	report_summary = list()
	isAsc = numpy.sign(report[0] - next(i for i in report if i != report[0]))

	for i in range(1, len(report)):
		diff = report[i - 1] - report[i]
		if (numpy.sign(diff) != isAsc) or abs(diff) > 3:
			return i

	return numpy.nan

# Scan a report and return which elements failed
def scan_report(report):
	report_summary = list()
	isAsc = numpy.sign(report[0] - next(i for i in report if i != report[0]))

	for i in range(1, len(report)):
		diff = report[i - 1] - report[i]
		if (numpy.sign(diff) != isAsc) or abs(diff) > 3:
			report_summary.append(False)
		else:
			report_summary.append(True)
	return report_summary

def compute_value(list):
	sum = 0
	for item in list:
		numbers = re.findall('\d{1,3}', item)
		if (len(numbers) != 2):
			print('Error processing',  item)
		sum+=int(numbers[0])*int(numbers[1])
	return sum