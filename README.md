<a name="readme-top"></a>
# 📚 Table of Contents
- [ℹ About The Project](#about)
- [👨‍💻Built with](#db)
- [🔑Setup](#setup)
- [📊 Visualization](#viz)
- [🌲 Project tree](#tree)
- [📄 License](#license)

<a name="about"></a>
<!-- ABOUT THE PROJECT -->
# ℹ️ About The Project
This project addresses limitations in the ZeppLife iOS app for my Xiaomi scale data. Since the official app lacked needed features, I built a custom weight tracking solution.

<span style="font-weight: bold; text-decoration: underline;">Key Features:</span>
- Telegram bot (Python) for convenient data entry from any device
- Add and delete weight entries seamlessly
- Infrastructure managed via Terraform (IaC approach)
- BigQuery integration for scalable data storage

<br>
The Terraform setup ensures consistent, reproducible infrastructure including BigQuery datasets and tables. Future releases will expand bot capabilities based on user needs.

<p align="right">
(<a href="#readme-top"> back to top</a>)</p>

# 👨‍💻 Built with

| Technology | Usage |
| ---------- | ------|
| <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>  | Used as the main programming language to write Telegram Bot.|
| <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> | Messaging app used as the interface for interacting with the  system. |
| <img src="https://img.shields.io/badge/Google Big Query-%234285F4?style=for-the-badge&logo=googlebigquery&logoColor=white"/>| Data Storage |
| <img src="https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white"/>| Infrastructure as code tool for managing and provisioning cloud resources. |
<p align="right">
(<a href="#readme-top"> back to top</a>)</p>

<a name="setup"></a>
# 🔑 Setup

## Telegram Bot Setup

1. Write to [Bot Father](https://web.telegram.org/k/#@BotFather) on Telegram

<img src="https://github.com/PKuziola/weight-tracker/blob/master/images/image_1.png?raw=true"/>

2. Tap Start Button, list of commands will appear. You can use them later to enhance your bot, for example change bot picture, description etc.

3. Run following command

```
/newbot
#You will be asked to provide name and username
#Note that username has to finish with "_bot"
```

4. Having successfully provided required details you will receive token to access Bot via Telegram API.

<img src="https://github.com/PKuziola/weight-tracker/blob/master/images/image_2.png?raw=true"/>

<p align="right">
(<a href="#readme-top"> back to top</a>)</p>

## Get Telegram UserID

1. Write to [Userinfobot](https://web.telegram.org/k/#@userinfobot) on Telegram

<img src="https://github.com/PKuziola/weight-tracker/blob/master/images/image_3.jpg?raw=true"/>

2. Tap Start Button. Bot will reply and give UserID.

<img src="https://github.com/PKuziola/weight-tracker/blob/master/images/image_4.png?raw=true"/>

<p align="right">
(<a href="#readme-top"> back to top</a>)</p>

## Env Variables

List of variables to fill out is in .env_sample file

```
TOKEN=<Token received from BotFather>
BOT_USERNAME=<Bot username set during conversation with BotFather>
TELEGRAM_USER_ID=<UserID received from userinfobot>
DATASET_NAME=<Dataset name in Google BigQuery>
TABLE_NAME=<Table name to store weight entries>
```

<p align="right">
(<a href="#readme-top"> back to top</a>)</p>

## Terraform Variables

```
#/infrastructure/terraform.tfvars

project_id = <Google Cloud Project ID>
credentials_file = <Service Account .json key file path>
region = "europe-central2"

#/infrastructure/main.tf
dataset_id=   #line4 - should be the same as one listed in Env Variables
table_id=     #line15- should be the same as one listed in Env Variables

```

<p align="right">
(<a href="#readme-top"> back to top</a>)</p>

## Google Cloud Setup

### 1. Service Account with following roles:

- ROLE: roles/bigquery.admin
- ROLE: roles/bigquery.dataEditor

### 2. Enable Cloud Resource Manager API in your project

### 3. Download Service Account Key in .json format and put it in main repository directory

### 4. Terraform Deployment

```
cd .\infrastructure\
terraform init
terraform plan
terraform apply
```

<p align="right">
(<a href="#readme-top"> back to top</a>)</p>

## Run Locally

```
cd .\telegram-bot\
python bot.py

#In the future, the plan is for the bot to run 24/7 as a containerized app on Cloud Run
```

<p align="right">
(<a href="#readme-top"> back to top</a>)</p>
