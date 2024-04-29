# Discord Bot

This is a Discord bot developed in Python using the discord.py library. The bot provides moderation commands and a quiz feature, as well as a help command to guide users through its functionalities.

## Features

### Moderation Commands

- **Kick**: Kicks a user from the server with an optional reason provided by the moderator.
- **Ban**: Bans a user from the server with an optional reason provided by the moderator.

### Quiz Feature

- **Quiz**: Starts a quiz session where the bot fetches random questions from an external Django API. Users can attempt the quiz and get instant feedback on their answers.

### Help Command

- **Help**: Displays information about all available bot commands, assisting users in utilizing the bot's functionalities effectively.

## Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/your_username/discord-bot.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Django API:
   
   - Navigate to the Django project directory containing `manage.py`.
   - Run the following command to start the Django development server:

     ```bash
     python manage.py runserver
     ```

4. Configure the bot:

    - Replace `YOUR_BOT_TOKEN` in the code with your Discord bot token.
    - Ensure your Discord bot has necessary permissions in the server to perform moderation actions.

5. Run the bot:

    ```bash
    python bot.py
    ```

## Docker Setup

You can also run the bot and Django API in Docker containers. Ensure Docker is installed on your system.

1. Build the Docker image:

    ```bash
    docker build -t discord-bot .
    ```

2. Run the Docker container:

    ```bash
    docker run -d --name discord-bot discord-bot
    ```

## Usage

Once the bot is running and added to your Discord server, you can use the following commands:

- `>help`: Display a list of available commands and their descriptions.
- `>kick <user> [reason]`: Kick a user from the server.
- `>ban <user> [reason]`: Ban a user from the server.
- `>punch <user>`: Punch a user.
- `>strike <user1> <user2>`: Strike a user.
- `>info`: Send information about the server, including server ID, member count, and server icon.
- `>quiz`: Start a quiz session with random questions fetched from the Django API.


## Organization

You can view how the project have been organized with the following jira calendar: https://yapsonstudio.atlassian.net/jira/core/projects/PB/calendar?atlOrigin=eyJpIjoiMGQ4YzZjMDNlZjllNGNiZmI2YjljMjE1OTY4ODEyMDkiLCJwIjoiaiJ9

## Credits

- This bot uses the discord.py library: https://github.com/Rapptz/discord.py
- Quiz questions are fetched from a Django API.
- The bot's functionalities are inspired by the Discord bot tutorial playlist by thenewboston: https://youtube.com/playlist?list=PL6gx4Cwl9DGAHdJdtEl0-XiRfPRAvpbSz&si=SX2jzad8vrC5mWkR
- The bot's functionalities are also inspired by the Discord bot tutorial by Very Academy: https://python.plainenglish.io/build-discord-quizbot-with-python-and-deploy-1-44dec1250a37

## License

This project is licensed under the [MIT License](LICENSE).
