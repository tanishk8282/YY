import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token from BotFather
TELEGRAM_BOT_TOKEN = '8129685312:AAHRsV0JW4WpMVYPg3KnS2sLh0RrNRTGuY0'

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the TeraBox Video Downloader bot! Send me a TeraBox video link to download."
    )

# Function to handle video link messages
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    video_url = update.message.text

    if not video_url.startswith("https://www.terabox.com"):
        await update.message.reply_text("Please send a valid TeraBox video link.")
        return
    
    await update.message.reply_text("Processing your video link, please wait...")

    # Assume get_terabox_video_url is a function that processes the TeraBox URL
    video_download_url = get_terabox_video_url(video_url)
    
    if not video_download_url:
        await update.message.reply_text("Failed to retrieve video. Please check the link and try again.")
        return
    
    # Download the video
    try:
        video_response = requests.get(video_download_url, stream=True)
        video_filename = "video.mp4"

        # Save the video to a temporary file
        with open(video_filename, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        
        # Send the video file to the user
        with open(video_filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file)
        
        # Clean up the downloaded file
        os.remove(video_filename)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Function to extract the download URL from TeraBox (Dummy function)
def get_terabox_video_url(terabox_url):
    # Replace with actual logic to fetch video URL from TeraBox
    # TeraBox might need a special API, or you might need to scrape the video URL
    # Example of dummy URL
    return "https://download-link-to-video.com/video.mp4"

async def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Start the Bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
