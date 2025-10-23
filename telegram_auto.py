from telethon import TelegramClient, events
import asyncio
from datetime import datetime
import pytz

# === Replace with your own credentials ===
API_ID = 21124114                 # from https://my.telegram.org
API_HASH = "8a042086b7d56600e9dd38b1f7952d5d"  # from https://my.telegram.org

# === Customize ===
AUTO_REPLY_TEXT = (
    "Hi 👋\n\nThanks for your message! "
    "I'm currently away and will reply soon."
)

# Off-hours logic (Warsaw time)
TIMEZONE = pytz.timezone("Europe/Warsaw")
START_HOUR = 17  # reply only from 12:00 ...
END_HOUR = 8     # ... until 08:00 next day

client = TelegramClient("session_name", API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()

    # Safety: skip any non-user sender (e.g. channels, groups)
    if not hasattr(sender, "bot"):
        return

    # Ignore bots, yourself, groups, and channels
    if sender.bot or sender.is_self or event.is_group or event.is_channel:
        return

    # Off-hours check
    from datetime import datetime
    now = datetime.now(TIMEZONE)
    hour = now.hour
    off_hours = (hour >= START_HOUR) or (hour < END_HOUR)
    if not off_hours:
        return

    # Send auto reply
    try:
        await event.reply(AUTO_REPLY_TEXT)
        print(f"Auto-replied to {sender.first_name or sender.username}")
    except Exception as e:
        print("Reply error:", e)


async def main():
    print("Connecting to Telegram...")
    await client.start()  # handles phone number, code, and password automatically
    print("Signed in successfully ✅")
    print("Auto-reply running... Press Ctrl+C to stop.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
