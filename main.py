import os
import subprocess
import glob
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DOWNLOAD_DIR = "./downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.strip()

    if "tiktok.com" not in user_msg:
        await update.message.reply_text("Kirim link TikTok ya!")
        return

    await update.message.reply_text("⏳ Lagi proses link ini...")

    try:
        subprocess.run([
            "yt-dlp",
            "--no-watermark",
            "-o", f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            user_msg
        ], check=True)

        files = glob.glob(f"{DOWNLOAD_DIR}/*")
        if not files:
            await update.message.reply_text("❌ Gagal download.")
            return

        latest = max(files, key=os.path.getctime)
        ext = latest.split(".")[-1]

        with open(latest, "rb") as f:
            if ext in ["mp4", "webm", "mov"]:
                await update.message.reply_video(f, caption="✅ Done!")
            else:
                await update.message.reply_photo(f, caption="✅ Done!")

        os.remove(latest)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Agent jalan...")
    app.run_polling()
