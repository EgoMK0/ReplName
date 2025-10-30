# Discord Bypass Bot

## Overview
A powerful Discord bot that bypasses URL shorteners and link protectors with advanced features including AI analysis, caching, rate limiting, and auto-bypass functionality. Supports 50+ popular services like Linkvertise, Boost.ink, and many more.

## Project Architecture

### Main Components
- **bot.py** - Main Discord bot with slash commands, modals, views, and event handlers
- **ai_service.py** - OpenAI integration for script safety analysis and error troubleshooting
- **cache_manager.py** - TTL-based caching system to improve performance
- **rate_limiter.py** - Request rate limiting to prevent API abuse
- **hwid_service.py** - Hardware ID verification and registration
- **user_activity.py** - User activity tracking and blacklist management

### Data Storage
The bot uses JSON files for persistent storage:
- `autobypass_channels.json` - Channels with auto-bypass enabled
- `bypass_stats.json` - Bot statistics and usage metrics
- `log_channels.json` - Logging channel configuration
- `hwid_data.json` - Hardware ID registration data
- `user_activity.json` - User activity logs and blacklist

## Features

### Core Functionality
- **Link Bypassing**: Bypass 50+ URL shortener services using ace-bypass.com API
- **Auto-Bypass**: Automatically bypass links posted in designated channels
- **Smart Caching**: 30-minute TTL cache to reduce API calls and improve response time
- **Rate Limiting**: 10 requests per 60 seconds per user to prevent abuse

### Admin Features
- **Channel Management**: Set auto-bypass channels and log channels
- **User Blacklist**: Block users or HWIDs from using the bot
- **Statistics Tracking**: Detailed stats on bypasses, cache hits, and service usage
- **Configuration**: Easy API key management via Discord commands

### User Features
- **Slash Commands**: Modern Discord slash command interface
- **Interactive Buttons**: Copy buttons for easy access to results
- **Private Results**: All bypass results are ephemeral (only visible to requester)
- **Mobile Friendly**: Large files sent as downloadable attachments

## Setup Instructions

### Required Environment Variables
Create a `.env` file with the following:
```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
BYPASS_API_KEY=your_ace_bypass_api_key_here
OPENAI_API_KEY=your_openai_api_key_here_optional
BOT_OWNER_ID=your_discord_user_id_here
```

### Getting API Keys
1. **Discord Bot Token**: 
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to "Bot" section and create a bot
   - Copy the token
   - Enable "Message Content Intent" under Privileged Gateway Intents

2. **Bypass API Key**:
   - Visit [ace-bypass.com](https://ace-bypass.com)
   - Sign up and get your API key

3. **OpenAI API Key** (Optional):
   - Visit [OpenAI Platform](https://platform.openai.com)
   - Create an API key for AI-powered features

4. **Bot Owner ID**:
   - Enable Discord Developer Mode (Settings > Advanced > Developer Mode)
   - Right-click your profile and select "Copy User ID"

### Bot Invite Link
Use this template to invite the bot to your server:
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

## Available Commands

### User Commands
- `/bypass` - Open modal to bypass a link
- `/supported` - View all supported bypass services (paginated)
- `/stats` - View detailed bot statistics
- `/info` - Get information about the bot
- `/say` - Make the bot say a message
- `/embed` - Create a custom embed message

### Admin Commands (Manage Channels Permission)
- `/autobypass <channel>` - Enable auto-bypass in a channel
- `/disableautobypass` - Disable auto-bypass in the server
- `/panel` - Create a persistent bypass panel with a button

### Owner Commands (Bot Owner Only)
- `/config` - Configure API keys via Discord modal
- `/setlogs <channel>` - Set the bypass logs channel
- `/blacklist <action> [user] [hwid]` - Manage user/HWID blacklist

## Supported Services
The bot supports 50+ bypass services including:
- Linkvertise
- Boost.ink
- Rekonise
- Codex
- Trigon
- And many more!

Use `/supported` command to view the complete list with pagination.

## Auto-Bypass Feature
When enabled in a channel:
1. User posts a link in the designated channel
2. Bot automatically deletes the message
3. Bot bypasses the link
4. Bot sends the result via DM to the user
5. Confirmation message is sent in the channel (auto-deletes after 10s)

## Statistics Tracked
- Total bypasses (loadstrings vs URLs)
- Failed attempts
- Cache hit rate
- Top 5 most-used services
- Success rate percentage
- AI analyses performed

## Recent Changes
- **2025-10-30**: Initial bot deployment with full feature set

## User Preferences
- Cache TTL: 30 minutes
- Rate Limit: 10 requests per 60 seconds
- Default services per page: 15
- Auto-delete confirmation messages: 10 seconds

## Troubleshooting

### Bot Not Responding
1. Check that the bot is online
2. Verify bot has proper permissions in the server
3. Ensure slash commands are synced (happens automatically on startup)

### Auto-Bypass Not Working
1. Verify auto-bypass is enabled in the correct channel
2. Check bot has permission to delete messages
3. Ensure users have DMs enabled

### API Errors
1. Verify BYPASS_API_KEY is set correctly
2. Check API quota/limits on ace-bypass.com
3. Use `/config` command to update keys if needed

## Dependencies
- discord.py (2.6.4+) - Discord bot framework
- aiohttp - Async HTTP requests
- python-dotenv - Environment variable management
- openai - AI analysis features (optional)

## Project Status
**Status**: Production Ready
**Version**: 1.0.0
**Last Updated**: October 30, 2025
