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

n_groups = 11


vdis_D = ['> 5M','1M - 5M','500K - 1M','100K - 500K','50K - 100K','10K - 50K','5K - 10K','1K - 5K','500 - 1K', '100 - 500', '< 100']
v1 = [20+96+96, 648, 548, 2156, 1574, 5399, 2892, 7604, 3014, 6084, 6089]
v2 = [22+97+81, 558, 462, 1668, 1199, 4099, 2183, 5878, 2417, 5155, 5693]
v3 = [10+36+39, 228, 164, 696, 487, 1859, 964, 2755, 1229, 2749, 3313]
vuln = [3+9+21, 116, 114, 562, 413, 1429, 784, 1928, 668, 1140, 700]
percent = [0.13865546218487396, 17.083946980854197, 19.587628865979383, 24.955595026642985, 25.352977286678946, 25.600143317807238, 26.168224299065418, 24.488759049917437, 21.41025641025641, 17.87113967706537, 10.847667751433441]

print(len(vdis_D), len(v1), len(v2), len(v3), len(vuln), len(percent))

# vdis_lo = [vdis_no[i] + vdis_lo[i] for i in range(len(vdis_lo))]

fig, ax = plt.subplots(figsize=(4,3))
# fig, ax = plt.subplots()
rcParams['axes.unicode_minus']=False

index = np.arange(n_groups)
bar_width = 0.4



opacity = 1
error_config = {'ecolor':'grey',    # error-bars colour
                'linewidth':2}

p4 = plt.bar(index+ bar_width, v1, bar_width,
                 alpha=opacity,
                 color=[(182/256,177/256,47/256)],#'white',
                 #yerr=without_tsx_yerr,
                 edgecolor='black',
                 #hatch = 'xxxx',
                 zorder=3)

p2 = plt.bar(index+ bar_width, v2, bar_width,
                 alpha=opacity,
                 # color=[(251/256,112/256,32/256)],#'silver',
                 color='orange',
                 #yerr=without_tsx_yerr,
                 edgecolor='black',
                 #hatch = '\\\\\\\\\\',
                 # hatch = 'xxxxxxxxxx',
                 zorder=3)

p1 = plt.bar(index+ bar_width, v3, bar_width,
                 alpha=opacity,

                 color=[(28/256,111/256,169/256)],#'gray',

                 #yerr=without_tsx_yerr,
                 edgecolor='black',
                 #hatch = '\\\\\\\\\\',
                 # hatch = 'xxxxxx',
                 zorder=3)
p0 = plt.bar(index + 2 * bar_width, vuln, bar_width,
                 alpha=opacity,

                 color=[(251/256,112/256,32/256)],
                 # color='orange',
                 # yerr=without_tsx_yerr,
                 edgecolor='black',
                 # hatch = '\\\\\\\\\\',
                 # hatch = 'xxxxxx',
                 zorder=3
             )

for i, rect in enumerate(p4):
        print(rect, i)
        height = rect.get_height()
        # ax.annotate('{}'.format('%.2f' % (vdis_lo[i]*100/vdis_al[i])), xy=(rect.get_x() + rect.get_width() / 2, height),
        ax.annotate(v1[i], xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=5
                    )

for i, rect in enumerate(p0):
        print(rect, i)
        height = rect.get_height()
        x = rect.get_x() + rect.get_width()/2
        if vuln[i] > 100:
            x = rect.get_x() + rect.get_width() * 0.6
        elif vuln[i] > 1000:
            x = rect.get_x() + rect.get_width() * 0.75
        # ax.annotate('{}'.format('%.2f' % (vdis_lo[i]*100/vdis_al[i])), xy=(rect.get_x() + rect.get_width() / 2, height),
        ax.annotate(vuln[i], xy=(x, height),
                xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=5
                    )

# ax.set_yscale("log", nonpositive='clip')

ax.set_xlim(-bar_width,len(index)+bar_width)
ax.set_xticks(index + 1.5 * bar_width)


ax.set_ylim([0,8000])
ax.set_yticks([0, 1500, 3000, 4500, 6000, 7500])
yTickMarks = ('0', '1500', '3000', '4500', '6000', '7500')
ytickNames = ax.set_yticklabels(yTickMarks,color="Black",fontsize=8)

xTickMarks = vdis_D

xtickNames = ax.set_xticklabels(xTickMarks,color="Black",rotation=45,fontsize=8,ha='right' )

ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
# ax.
legend1 = plt.legend([p4[0],p2[0],p1[0], p0[0]], ['V1 Scheme', 'V2 Scheme', 'V3 Scheme', 'Vulnerable'], loc=2, fontsize=6)
# ax.
# legend2 = plt.legend([p4[0]], ['Location Perm.'], loc =2, ncol=3)#, fontsize=18)

ax.add_artist(legend1)
# ax.add_artist(legend2)

ax.set_ylabel('# Apps',fontsize=8)

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

plt.savefig("vulnApkSign.pdf", format='pdf', dpi=500)
plt.show()