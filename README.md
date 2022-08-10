# IoTSpotter：Understanding IoT Security from a Market-Scale Perspective

## Introduction

IoTSpotter is a tool for automatically identifying mobile-IoT apps, IoT specific library, and potential vulnerabilities (i.e., third-party library vulnerabilities, cryptographic API misuse, and Janus vulnerabilities) in the wild based on natural language processing and deep learning. Based on IoTSpotter, we identify 37,783 mobile-IoT apps from google play and 19,939 IoT Specific third-party library package names, which are available in this repo. Moreover, based on the identification results, we discover 43,172 cryptographic violations that affect over 900 apps with more than a million installs each, 65 vulnerable libraries specific to IoT used by 40 apps containing 79 unique vulnerabilities mapped to CVEs, and 7,887 apps that is affected by the Janus vulnerability.

<p align="center"><img src="figure/iotspotter.PNG" alt="workflow" width="800"></p>

## Data Release

We provide the corpus and IoTSpotter identification results. Please don't distribute them. We will open source them to the public after the paper is published.

### 1. 37K mobile-IoT apps

The metadata of our identified 37K IoT apps is [here](https://drive.google.com/file/d/1Fq4sGUpEuU7EPnZuxMMCZdWlBXjDD8wN/view?usp=sharing). Each line of the metadata file is a json object, e.g.,
```json
{
  "title": "Doodle It - Pictionary for your Chromecast",
  "icon": "https://play-lh.googleusercontent.com/MBMHhCzEFKYmD1kE88NMMj-wFEcCqSJONGoMcayGjRExEjkvVp6wvKh08X828jHaVA",
  "screenshots": [
    "https://play-lh.googleusercontent.com/zyi_NuligVJYZmjHTTGH2nhfjcD6xVbt5zR_tuPqxmmdhhfe7aPiePe1dCCEV7mIB1Vt=w720-h310-rw",

  ],
  "video": "https://www.youtube.com/embed/sbhm4pjWKuU",
  "category": [
    "GAME_WORD"
  ],
  "score": "4.2",
  "histogram": {
    "1": null,
    "2": null,
    "3": null,
    "4": null,
    "5": null
  },
  "reviews": 84,
  "description": "Whit \"Doodle it\" you can challenge your friends and family in a fun and interactive game where everyone participates!\nThe rules are simple:\n• Split in two teams\n• Each turn, one draws a random word, the rest of the team has to guess it\n• The first team to reach 10 wins!\n\"Doodle it\" is like playing charades with pen and paper, using your tablet as the drawing board.\n\"Doodle it\" is the ideal game to add to your set for a fun game night.\n\"Doodle it\" will challenge your artistic skills and fast thinking trying to draw and guess the more than 1000 different words provided by the FULL package!!!\n\"Doodle it\" will provides a special KIDS package so kids can play and have fun!!!\n\"Doodle it\" will cast your drawings live to your TV! You draw on your tablet, the rest guess from the Chromecast!\n--\n• We are still working on improving the game and we will love to hear your feedback",
  "description_html": "Whit \"Doodle it\" you can challenge your friends and family in a fun and interactive game where everyone participates!<br/><br/>The rules are simple:<br/><br/>• Split in two teams<br/>• Each turn, one draws a random word, the rest of the team has to guess it<br/>• The first team to reach 10 wins!<br/><br/>\"Doodle it\" is like playing charades with pen and paper, using your tablet as the drawing board.<br/><br/>\"Doodle it\" is the ideal game to add to your set for a fun game night.<br/><br/>\"Doodle it\" will challenge your artistic skills and fast thinking trying to draw and guess the more than 1000 different words provided by the FULL package!!!<br/><br/>\"Doodle it\" will provides a special KIDS package so kids can play and have fun!!!<br/><br/>\"Doodle it\" will cast your drawings live to your TV! You draw on your tablet, the rest guess from the Chromecast!<br/><br/>--<br/>• We are still working on improving the game and we will love to hear your feedback",
  "recent_changes": null,
  "editors_choice": false,
  "price": "0",
  "free": true,
  "iap": true,
  "developer_id": "Hi%27ona+Studios",
  "updated": "April 3, 2020",
  "size": "3.0M",
  "installs": "10,000+",
  "current_version": "1.8.3",
  "required_android_version": "5.0 and up",
  "content_rating": [
    "Everyone"
  ],
  "iap_range": [
    "Everyone"
  ],
  "interactive_elements": null,
  "developer": "Hi'ona Studios",
  "developer_email": "hiona.studios@gmail.com",
  "developer_url": "https://www.reddit.com/r/doodle_it",
  "developer_address": "Råggatan 8, lght 1004\n18 59 Stockholm\nSweden",
  "app_id": "com.hiona.doodleit",
  "url": "https://play.google.com/store/apps/details?id=com.hiona.doodleit"
}
```
Since the total file size of all APKs of 37 mobile-IoT apps is more than 100GB, we recommand you to directly download them via [Androzoo](https://androzoo.uni.lu/). For the same APKs that we used for analysis, you can download them via Androzoo APIs with the [sha256 signatures](data/apk_androzoo_sha256/xin_sunil_shared_sha256_androzoo.csv). 

### 2. 19K IoT specific package names

Our differential analysis component identifies 19K 3rd-party library package names, which can be found [here](data/3rd_party_lib/filtered_package_names.txt). Each line of the file corresponds to one unique package name. Here, package names are the name of [JAVA packages](https://docs.oracle.com/javase/tutorial/java/concepts/package.html).

### 3. Datasets of mobile-IoT app classifiers

You can find our annotated datasets [here](data/dataset), where the `label` is 1 (IoT) and 0 (non-IoT). Part of the IoT app samples are from Wang'2019 USENIX Security paper, we obtained all their apps from this [link](http://seclab.soic.indiana.edu/xw48/iot_companion_appset.tar.gz). Then we removed the apps that were not in GPlay any more and obtained the rest apps for annotataion. And we provide the rest app list [here](data/artifacts/app_list.txt).

### 4. Mobile-IoT app classifiers

For the mobile-IoT app classifiers, you can find the BiLSTM classifier [here](data/classifiers/bilstm.h5) and download the BERT model via this [link](https://drive.google.com/file/d/1D080URvXGGYAcg6TKX4RxLUPorKppY0i/view?usp=sharing).

### 5. IoT products and name entity recognition (NER) model

You can download the NER dataset, script and model via this [link](https://drive.google.com/file/d/1HxqHFE-VnofdMNHWEyyjLXymRMzrzWfn/view?usp=sharing). After identifying the IoT products, we cluster them with [GSDMM model](https://github.com/rwalk/gsdmm-rust). You can find resulting clusters [here](data/artifacts/iot_product_clustering_results.zip), in which the non-empty files are unique clusters.

## Installation

We recommend `conda` to setup the environment and install the required packages. Conda installation instructions can be found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html). The following setup assumes Conda is installed and is running on Linux system (though Windows should work too).

First, create the conda environment,

`conda create -n iotspotter python=3.8`

and activate the conda enviroment:

`conda activate iotspotter`

Then, install the `pip` package manager and other packages:

`conda install pip`

`pip install -r requirement.txt`

## Mobile-IoT classifier

To train the BiLSTM classfier, you have to first download the pretrained word vectors from [Glove](https://nlp.stanford.edu/data/glove.6B.zip) and put the `glove.6B.300d.txt` file in this [folder](data/glove).

Commands to train the model:

`cd classification`

`python bilstm.py`

The resulting model will be `data/classifiers/bilstm_new_training.h5`.

To classify model, run the following commands:

`cd classification`

`python classification.py`

For the BERT model, we provide the script and instructions along with the classifier via this [link](https://drive.google.com/file/d/1D080URvXGGYAcg6TKX4RxLUPorKppY0i/view?usp=sharing).


### 6. IoT library vulnerability analysis

### 6. Cryptograph-API misuse analysis

