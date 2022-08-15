#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: plot_vuln.py
@time: 1/23/22 4:40 PM
@desc:
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.1  # previous pdf hatch linewidth
mpl.rcParams['hatch.linewidth'] = 0.1  # previous svg hatch linewidth



fig = plt.figure()
ax = fig.add_subplot(111)

n_groups = 14


# vdis_D = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
# flaw_num = [1311,13297,2271,1931,71,293,2298,104,85,716,67,186,15573,283,0,0]
# app_num = [406,825,577,380,66,293,438,70,63,239,50,186,842,142,0,0]
vdis_D = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
flaw_num = [1311,13297,2271,1931,71,293,2298,104,85,716,67,186,15573,283]
app_num = [406,825,577,380,66,293,438,70,63,239,50,186,842,142]

print(len(vdis_D), len(flaw_num), len(app_num))

# vdis_lo = [vdis_no[i] + vdis_lo[i] for i in range(len(vdis_lo))]

fig, ax = plt.subplots(figsize=(4,3))
# fig, ax = plt.subplots()
rcParams['axes.unicode_minus']=False

index = np.arange(n_groups)
bar_width = 0.4



opacity = 1
error_config = {'ecolor':'grey',    # error-bars colour
                'linewidth':2}

# p4 = plt.bar(index+ bar_width, flaw_num, bar_width,
#                  alpha=opacity,
#                  color=[(182/256,177/256,47/256)],#'white',
#                  #yerr=without_tsx_yerr,
#                  edgecolor='black',
#                  #hatch = 'xxxx',
#                  zorder=3)

p2 = plt.bar(index+ bar_width, flaw_num, bar_width,
                 alpha=opacity,
                 # color=[(251/256,112/256,32/256)],#'silver',
                 color='orange',
                 #yerr=without_tsx_yerr,
                 edgecolor='black',
                 #hatch = '\\\\\\\\\\',
                 # hatch = 'xxxxxxxxxx',
                 zorder=3)

# p1 = plt.bar(index+ bar_width, v3, bar_width,
#                  alpha=opacity,
#
#                  color=[(28/256,111/256,169/256)],#'gray',
#
#                  #yerr=without_tsx_yerr,
#                  edgecolor='black',
#                  #hatch = '\\\\\\\\\\',
#                  # hatch = 'xxxxxx',
#                  zorder=3)

p0 = plt.bar(index + 2 * bar_width, app_num, bar_width,
                 alpha=opacity,

                 color=[(28/256,111/256,169/256)],
                 # color='orange',
                 # yerr=without_tsx_yerr,
                 edgecolor='black',
                 # hatch = '\\\\\\\\\\',
                 # hatch = 'xxxxxx',
                 zorder=3
             )

for i, rect in enumerate(p2):
        print(rect, i)
        height = rect.get_height()
        # ax.annotate('{}'.format('%.2f' % (vdis_lo[i]*100/vdis_al[i])), xy=(rect.get_x() + rect.get_width() / 2, height),
        ax.annotate(flaw_num[i], xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8
                    )

for i, rect in enumerate(p0):
        print(rect, i)
        height = rect.get_height()
        x = rect.get_x() + rect.get_width()/2
        if app_num[i] > 100:
            x = rect.get_x() + rect.get_width() * 0.75
        elif app_num[i] > 1000:
            x = rect.get_x() + rect.get_width() * 0.75
        # ax.annotate('{}'.format('%.2f' % (vdis_lo[i]*100/vdis_al[i])), xy=(rect.get_x() + rect.get_width() / 2, height),
        ax.annotate(app_num[i], xy=(x, height),
                xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8
                    )

ax.set_yscale("log", nonpositive='clip')

ax.set_xlim(-bar_width,len(index)+bar_width)
ax.set_xticks(index + 1.5 * bar_width)


# ax.set_ylim([0,15000])
# ax.set_yticks([0, 1000, 5000, 10000, 15000])
# yTickMarks = ('0', '1000', '5000', '10000', '15000')
# ytickNames = ax.set_yticklabels(color="Black",fontsize=8)
ax.tick_params(axis='y', labelsize=10)

xTickMarks = vdis_D

# xtickNames = ax.set_xticklabels(xTickMarks,color="Black",rotation=45,fontsize=8,ha='right' )
xtickNames = ax.set_xticklabels(xTickMarks,color="Black",fontsize=10,ha='right' )

ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
# ax.
legend1 = plt.legend([p2[0],p0[0]], ['# Flaws Per Rule', '# Violating Apps Per Rule'], loc=9, fontsize=9)
# ax.
# legend2 = plt.legend([p4[0]], ['Location Perm.'], loc =2, ncol=3)#, fontsize=18)

ax.add_artist(legend1)
# ax.add_artist(legend2)

ax.set_xlabel('Rule ID', fontsize=12)
ax.set_ylabel('Reported Numbers',fontsize=12)

rcParams.update({'font.size': 8})

ax.grid(axis="y")



# second y axis
# ax2 = ax.twinx()
# ax2.set_ylabel("Percentage", color="black")
#
# ax2_data = percent
#
# ax2.set_ylim([0, 40])
# ax2.set_yticks([1, 5, 10, 15, 20, 25, 30, 40])
#
#
# for i in range(ax2_data.__len__()):
#     if i == 4:
#         ax2.annotate("%d" % ax2_data[i], xy=(index[i] + bar_width, ax2_data[i] + 2), ha="center")
#     elif i == 11:
#         ax2.annotate("%d" % ax2_data[i], xy=(index[i] + bar_width, ax2_data[i] + 2), ha="center")
#     else:
#         ax2.annotate("%d" % ax2_data[i], xy=(index[i]+bar_width, ax2_data[i] + 3), ha="center")
# ax2_data = [a/2 + 20 for a in ax2_data]
# ax2.plot(index+bar_width, ax2_data, color="black", linewidth=1)
# ax2.set_yscale("log", nonpositive='clip')

rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True

fig.set_tight_layout(True)
#fig.set_size_inches(8, 5)

plt.savefig("CryptoGuard_flaws.pdf", format='pdf', dpi=500)
plt.show()