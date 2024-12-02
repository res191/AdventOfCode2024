import numpy

def process_safety_reports(list, damper=False):
	count = 0
	for report in list:
		if is_report_safe(report):
			count += 1
		elif (damper):
			report_copy1 = report.copy()
			del report_copy1[scan_report(report_copy1).index(False)]
			if is_report_safe(report_copy1):
				count += 1
				continue

			report_copy2 = report.copy()
			del report_copy2[scan_report(report_copy2).index(False) + 1]
			if is_report_safe(report_copy2):
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

# Scan a report and return which elements failed
def scan_report(report):
	report_summary = list()
	isAsc = numpy.sign(report[0] - report[len(report) - 1])

	for i in range(1, len(report)):
		diff = report[i - 1] - report[i]
		if (numpy.sign(diff) != isAsc) or abs(diff) > 3:
			report_summary.append(False)
		else:
			report_summary.append(True)
	return report_summary