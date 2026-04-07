# Spam Call Detection Agent

LiveKit voice agent that answers unknown calls, stalls the caller for 12 seconds, classifies the transcript as spam or legitimate, and sends you a Telegram alert with evidence.

## Stack

- **LiveKit Agents** - Voice call runtime
- **Sarvam `saaras:v3`** - Speech-to-text (STT)
- **OpenAI `gpt-5.4`** - Real-time conversation (stalling)
- **OpenAI `gpt-4o-mini`** - Spam classification
- **Sarvam `bulbul:v3`** - Text-to-speech (TTS)
- **Telegram Bot API** - Spam alerts with evidence

## How It Works

1. **Call comes in** - Agent answers with "Hello, this line is open. How can I help you?"
2. **Stall phase (12s)** - Agent keeps the caller talking with short filler responses
3. **Call ends** - After 12 seconds, the agent disconnects
4. **Classification** - Full transcript is sent to GPT-4o-mini for spam classification
5. **Telegram alert** - You receive a formatted message with:
   - Spam/Legitimate verdict
   - Confidence score
   - Reason
   - Exact transcript lines that indicate spam (highlighted)
   - Full transcript for reference

## Files

- `agent.py` - LiveKit worker entrypoint with spam detection pipeline
- `spam_classifier.py` - OpenAI-based transcript classifier with evidence extraction
- `telegram_notifier.py` - Telegram alert sender with formatted messages
- `agent_config.toml` - Runtime settings for STT, LLM, TTS, voice, and spam detection
- `agent_instructions.md` - Prompt for the stalling voice agent

## Local Setup

1. Install dependencies:

```bash
uv sync
```

2. Create your env file:

```bash
cp .env.example .env
```

3. Fill in credentials (see below for Telegram setup).

4. Start the worker:

```bash
uv run python agent.py start
```

## Telegram Setup

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`, follow prompts, copy the **bot token**
3. Start a chat with your new bot and send it any message
4. Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` to find your `chat_id` (it's a number like `123456789`)
5. Add both to your `.env`:

```
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...
TELEGRAM_CHAT_ID=123456789
```

## Environment Variables

```
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
SARVAM_API_KEY=your_sarvam_api_key
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

## Configuration

- `agent_config.toml` - Tune STT, LLM, TTS, voice behavior, and spam detection settings
  - `[spam_detection].call_duration_seconds` - How long to keep the caller talking (default: 12)
  - `[spam_detection].classification_model` - Model for classification (default: gpt-4o-mini)
- `agent_instructions.md` - Change the stalling agent behavior

## Telephony Setup

To receive actual phone calls, you need to route them into LiveKit. The most common approach:

**Twilio SIP Trunking:**
1. Set up a Twilio phone number
2. Configure Twilio SIP trunk to point to your LiveKit SIP URI
3. LiveKit will create a room for each incoming call and your agent joins it

See [LiveKit SIP docs](https://docs.livekit.io/sip/) for detailed setup.

## Docker

```bash
docker build -t spam-detection-agent .
```
