
# Gordotron

## Overview

Gordotron is a custom Discord bot designed to manage server activities, track member participation in voice channels, and provide fun and interactive features for specific users. It is built using the `discord.py` library and is intended for use in a highly customized Discord server environment.

## Features

### 1. Thread Management
- **Auto-Archiving Threads:** Automatically edits newly created threads to be archived after 1 hour instead of the default 7 days.

### 2. Member Management
- **On Member Join:** New members are automatically added to tracking files (`time.txt` and `subscriptions.txt`) for leaderboard and subscription purposes.
- **On Member Remove:** Members who leave the server are removed from the tracking files.

### 3. Voice Channel Tracking
- **Time Tracking:** Logs when members join or leave voice channels, calculating and updating the total time spent in voice channels. This data is used to maintain a leaderboard.
- **Brandon Waiting Room:** Special handling for a user named Brandon, with dynamic voice channel renaming and server-wide notifications when Brandon joins or leaves specific channels.

### 4. Message Handling
- **Subscriptions:** Users can subscribe to be notified when specific members join voice channels using the `!subscribe` command.
- **Jackson Curse:** Implements special rules and restrictions for a user named Jackson, including message token management and conditional curses.
- **Media Responses:** The bot sends specific images in response to keywords like "schwab" or "jojo" in messages.
- **Leaderboard Display:** Displays a leaderboard of users based on their voice channel activity using the `!leaderboard` command.
- **Message Token Management:** Tracks and restricts the number of messages a user named Jackson can send, modifying token usage based on various conditions.
- **Ari Message Responses:** Randomly replies to messages from a user named Ari with specific phrases or emojis.
- **Message Stealing:** Randomly deletes a user’s message and re-sends it as the bot’s own.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ItsCazzz/Gordotron.git
    cd Gordotron
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables by creating a `.env` file with the following content:

    ```env
    BOT_TOKEN=your_discord_bot_token
    JACKSON_SECRET_MESSAGE=your_secret_message
    ```

## Usage

After setting up the environment variables and installing the dependencies, run the bot using:

```bash
python Gordotron.py
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please contact the project maintainer at [theggjokerexe@gmail.com](mailto:theggjokerexe@gmail.com).
