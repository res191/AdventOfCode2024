import numpy

def process_safety_reports(list):
	count = 0
	for report in list:
		if is_report_safe(report):
			count += 1
	return count

def is_report_safe(report):
	isAsc = numpy.sign(report[0] - report[1])
	for i in range(1, len(report)):
		diff = report[i - 1] - report[i]
		if (numpy.sign(diff) != isAsc) or abs(diff) > 3:
			return False
	return True