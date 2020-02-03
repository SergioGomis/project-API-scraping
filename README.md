![Starbucks](https://github.com/SergioGomis/project-API-scraping/blob/master/src/starbucks-logo-small.png)

This repo is a project for developing skills at the Data Analytics bootcamp of Ironhack Madrid by creating a functional python console program.

In this python project i:
- Took [this](https://www.kaggle.com/starbucks/store-locations) dataset from kaggle.com containing all the addresses of the Starbucks Stores worldwide.
- Made some web-scraping for completing the dataset.
- Worked with the pyPdf lib for constructing PDF files.
- Used the Google Static Maps API to obtain map images with marked locations.
- Used the Sendgrid lib & API for sending e-mails with attachments.


In order to run this program you should provide a .env file on root repository folder containing both API keys for Google Static Maps API and Sendgrid API. Also, a valid MAIL_SENDER e-mail address must be contained on it to be used when sending reports.

.env file:
```bash
SENDGRID_API_KEY=XXXXXX
MAPS_API_KEY=XXXXXX
MAIL_SENDER=user@domain.com
```

Command structure:
```bash
usage: main.py [-h] [-email EMAIL] [-s] [-v] city

positional arguments:
  city         City you want to find Starbucks on

optional arguments:
  -h, --help     show this help message and exit
  -email EMAIL   E-mail who will receive the pdf-report (required)
  -s, --stats    Show some statistics highlights from the dataset.
  -v, --version  show the program version and exit
```

Usage examples:
```bash
python3 main.py -email user@domain.com -s Alicante
```
```bash
python3 main.py -email user@domain.com Madrid
```
