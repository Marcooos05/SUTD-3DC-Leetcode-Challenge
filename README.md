# LeetCode Leaderboard Automation Script
Telegram bot to facilitate SUTD Leetcode Challenge

Welcome to the LeetCode Leaderboard Automation Script repository! This is my first Telegram Bot project which automates the generation of a leaderboard for LeetCode users, specifically designed for 3DC Google Developer Club at Singapore University of Technology and Design. The script fetches user data from LeetCode, updates a leaderboard based on the number of leetcode questions completed in a given timeframe, then the script interacts with a Telegram bot to share the leaderboard with all club members.

![Screenshot 2024-01-30 145516](https://github.com/Marcooos05/SUTD-3DC-Leetcode-Challenge/assets/108853663/877bbb75-9a9e-4100-b128-a4c0cf035b69)

**^Example Leaderboard from Leetcode users of SUTD**

### Table of Contents
- Introduction
- Features
- Requirements
- Installation
- Usage
- License

## Introduction
This script is designed to automate the process of generating a leaderboard for LeetCode users in SUTD's 3DC Google Developer Club. It fetches user statistics from LeetCode.com, compiles them into a leaderboard, and updates the leaderboard in a specified format. Additionally, it integrates with a Telegram bot to automatically share the updated leaderboard with club members.

## Features
1. Automatically fetches user data from LeetCode.
2. Generates a leaderboard based on total problems solved within the month.
3. Outputs the leaderboard including all users who regiatered for the challenge.
4. Integrates with a Telegram bot to share the leaderboard.
5. Easy configuration and setup.

## Requirements
- Python 3.10 
- Libraries:
  - datetime (standard library, no installation required)
  - time (standard library, no installation required)
  - typing (standard library, no installation required)
  - requests (install using pip install requests)
  - BeautifulSoup (install using pip install beautifulsoup4)
  - telegram and telegram.ext from the python-telegram-bot library (install using pip install python-telegram-bot)

## Installation
1. Clone the repository
```
git clone https://github.com/Marcooos05/SUTD-3DC-Leetcode-Challenge.git
cd SUTD-3DC-Leetcode-Challenge
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage
1.  Use BotFather to generate a new telegram bot via telegram.
2.  Copy Bot_Username and Token into mainbot.py.
3.  Fill up all registered Leetcode Usernames in the 'filterednames.txt' file.
  - Alternatively, start the bot and use the command /register to register leetcode usernames.
4.  Run the python code to keep the Bot Online.
  - Alternatively, upload the code into a cloud server like DigitalOcean to keep the bot live.
5.  Use the Bot Commands to retrieve score of users and the leaderboard of the challenge.

## License
This project is licensed under the MIT License.
