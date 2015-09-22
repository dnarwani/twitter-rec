# import codecs
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
#
# filename = "/home/dhiraj/mo.csv"
# filename2 = "/home/dhiraj/mo_edit.csv"
#
# with open(filename2, 'w') as myFile:
#     for line in codecs.open(filename, 'r', 'utf8'):
#             data = line.strip('\n').split(",")
#             if data[1] == '' or data[2] == '':
#                 x = 1
#
#             if (data[1] != '' and data[1] != '?') and (data[2] != '' and data[2] != '?') and (data[3] != '' and data[3] != '?') and (data[0] != '' and data[0] != '?'):
#                 years = range(int(str(data[1]).encode('utf-8')), int(str(data[2]).encode('utf-8'))+1)
#                 age = 0
#                 found = 0
#                 for year in years:
#                     if not found:
#                         if year  >= 1880 and year <= 1910:
#                             cohort1 = 1
#                             found = 1
#                         else:
#                             cohort1 = 0
#
#                         if year >= 1911 and year <= 1940:
#                             cohort2 = 1
#                             found = 1
#                         else:
#                             cohort2 = 0
#
#                         if year >= 1941 and year <= 1970:
#                             cohort3 = 1
#                             found = 1
#                         else:
#                             cohort3 = 0
#
#                         if year >= 1971 and year <= 2015:
#                             cohort4 = 1
#                             found = 1
#                         else:
#                             cohort4 = 0
#
#                     if year == int(data[2]):
#                         died = 1
#                     else:
#                         died = 0
#
#                     if data[4] == '':
#                         pre_activity = 0
#                     else:
#                         pre_activity = 1
#                     myFile.write(str(year) + "," + data[0] + "," + data[3] + "," + str(died) + "," + str(age) + "," + str(cohort1) + "," + str(cohort2) + "," + str(cohort3) +
#                                  "," + str(cohort4) + "," + str(pre_activity) + "\n")
#                     age += 1
#             else:
#                 x = 1


from recsys.evaluation.ranking import AveragePrecision

gt = [1197, 999, 729, 1676, 2222, 336, 498, 3730, 3455, 252, 1183]
test = [729, 2222, 83, 264, 1148, 1054, 801, 199, 2546, 1703]

model = AveragePrecision()
model.load(gt, test)
print model.compute()
