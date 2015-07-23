# hackathon-BSE-

## LinkedIn Scrapper Details

It scraps public profile of LinkedIn user and filter out the required 
information from it such as Education, Work Experience etc.

### Prerequisite and setup

- Python (2.7)
- MongoDB with pymongo
- BautifulSoup (bs4)
- Curl with pycurl

Before executing the scrapper, insure that `mongod` is running and
script is using appropriate port to connect it.

In MongoDB, you will need database named `hackathondb` and collections 
named as `linkedIn_raw_data` and `linkedIn_filtered_data`

### To execute the LinkedIn scrapper

You must execute scrapper with one command line argument which is
URL of some LinkedIn profile

#### Example
1. `python linkedIn_scrapper.py http://in.linkedin.com/in/ashgkwd`
1. `python linkedIn_scrapper.py https://in.linkedin.com/pub/suraj-gaikwad/98/453/728`
