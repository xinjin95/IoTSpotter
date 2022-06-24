# IoTSpotter
Understanding IoT Security from a Market-Scale Perspective

## About

Consumer IoT products and services are ubiquitous; yet, a proper characterization of consumer IoT security is infeasible without an understanding of what IoT products and services are currently on the market, i.e., without a market-scale perspective of IoT. This paper seeks to close this gap by developing the IoTSpotter framework for automatically constructing such a market-scale perspective of mobile-IoT apps, i.e., mobile apps that are used as companions or automation providers to IoT devices, and which form a critical, security-sensitive component of IoT systems. Using IoTSpotter, we identify 37,783 mobile-IoT apps from Google Play, the largest set of mobile-IoT apps so far (roughly 15x more than prior work). We then leverage this dataset to perform several security analyses, both to demonstrate the current state of mobile-IoT apps on the market, and IoTSpotter’s usefulness to future research that seeks to analyze a large majority of the mobile-IoT apps available on the market. We discover 43,172 cryptographic violations that affect over 900 apps with more than a million installs each, 65 vulnerable libraries specific to IoT used by 40 apps containing 79 unique vulnerabilities mapped to CVEs, and 7,887 apps that is affected by the Janus vulnerability. Finally, we perform a case study with 12 popular mobile-IoT apps to uncover the impact of their vulnerabilities in the IoT context, and discover impact in the area of functionality, authentication, and data leaks, which motivates the need for a deeper investigation of mobile-IoT apps.

## Data Release

For the apps that we obtained from Wang'2019 USENIX Security paper, we originally obtained all their apps from this [link](http://seclab.soic.indiana.edu/xw48/iot_companion_appset.tar.gz). Then we removed the apps that were not in GPlay any more and obtained the rest apps for annotataion. And we provide the rest app list [here](artifacts/app_list.txt).

For our identified 37K IoT apps, we put them into google drive because github has file size limitation. Please find them via this [link](https://drive.google.com/file/d/1Fq4sGUpEuU7EPnZuxMMCZdWlBXjDD8wN/view?usp=sharing) and don't distribute them. We will open source them to the public after the paper is published.
