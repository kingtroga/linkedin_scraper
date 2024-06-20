# LinkedIn Automation with Selenium

This Python script automates interactions with LinkedIn Sales Navigator using Selenium WebDriver. It can log into LinkedIn, navigate through lists of prospects, send messages, and manage contacts based on specific criteria.

## Demo

A video demonstration of the script's functionality is available (https://youtu.be/y9hNWIZXM_s).

## Features

Login Automation: Logs you into LinkedIn Sales Navigator automatically using your provided credentials.
Navigation: Seamlessly navigates to specific LinkedIn Sales Navigator pages and prospect lists.
Interaction Automation: Sends personalized messages to prospects, manages your contact lists (including saving, removing, and emailing contacts), and handles message history efficiently.
Proxy Support: Provides the option to use proxy settings for secure browsing.
Robust Error Handling: Implements comprehensive error handling to gracefully address various scenarios encountered during automation.

## Installation

1. Clone the Repository (if applicable)

If the script is hosted on a version control platform like Git, you can clone the repository using the following commands:

git clone `<repository-url>`
cd `<repository-directory>`

2. Install Dependencies

Make sure you have Python and pip (Python's package installer) installed on your system. You can usually find installation instructions online for your specific operating system.

Once Python and pip are set up, install the script's required dependencies using the following command in your terminal:

pip install -r requirements.txt

3. Secure Credential Setup

Important Security Note: Storing login credentials directly in environment variables is not recommended for production use. It can pose a security risk if your code is accessed by unauthorized parties. Consider using a secure credential management solution for a more robust approach.

For demonstration purposes only, here's how to set environment variables (replace with your actual credentials):

export LINKEDIN_USERNAME='your_linkedin_username'
export LINKEDIN_PASSWORD='your_linkedin_password'

## Usage

Disclaimer: This script is intended for educational purposes only. Automating actions that violate LinkedIn's terms of service is not recommended.

Once you've completed the installation steps, simply run the script using the following command in your terminal:

python main.py

Follow the prompts and logs displayed in the terminal to monitor the script's progress as it automates interactions on LinkedIn Sales Navigator based on the programmed logic.

## Contributing

We welcome contributions to this project! If you'd like to contribute, please fork the repository (if applicable) and submit a pull request.

## License

This project is licensed under the MIT License. Refer to the LICENSE file for details.
