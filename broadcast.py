"""Broadcast a message to all registered users.

Usage examples:
    python broadcast.py               # send default final message (asks confirmation)
    python broadcast.py -m "Custom text" --yes
    python broadcast.py --dry-run      # show how many users would receive it

Options:
    -m / --message   Override message text
    --dry-run        Do not send, just list/count users
    --yes            Skip interactive confirmation
    --limit N        Only send to first N users (testing)
    --chunk-size N   Concurrent send chunk size (default 20)
    --delay S        Delay (seconds) between chunks (default 0.5)

The script uses AsyncTeleBot directly. Ensure TELEGRAM_BOT_TOKEN env var is set
or present in .env (loaded via config.py) before running.
"""

import asyncio
import argparse
import logging
from logging.handlers import RotatingFileHandler
import os
from typing import List

import config  # loads environment variables
from database import SessionLocal, init_db
from models.User import User
from telebot.async_telebot import AsyncTeleBot
from telebot.apihelper import ApiTelegramException


# ---------------------------------------------------------------------------
# Logging setup (reuse logs directory pattern from main.py)
# ---------------------------------------------------------------------------
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.INFO)

_file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, 'broadcast.log'),
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding='utf-8'
)
_file_handler.setLevel(logging.INFO)

_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
for h in (_console_handler, _file_handler):
    h.setFormatter(_formatter)

logging.basicConfig(level=logging.INFO, handlers=[_console_handler, _file_handler])
logger = logging.getLogger("broadcast")


DEFAULT_MESSAGE = (
    "Tanlovimiz o’z nihoyasiga yetdi! Ishtirokingiz uchun tashakkur😊🙏🏻"
)


def get_all_user_ids(limit: int | None = None) -> List[int]:
    """Fetch all unique telegram user IDs from database."""
    db = SessionLocal()
    try:
        query = db.query(User.telegram_id)
        if limit:
            query = query.limit(limit)
        ids = [row[0] for row in query.all() if row[0] is not None]
        # Remove duplicates defensively (should be unique already)
        unique_ids = list(dict.fromkeys(ids))
        return unique_ids
    finally:
        db.close()


async def send_chunk(bot: AsyncTeleBot, user_ids: List[int], text: str) -> tuple[int, int]:
    """Send a message to a chunk of user IDs concurrently.

    Returns (success_count, failure_count)
    """
    tasks = []
    for uid in user_ids:
        tasks.append(_send_single(bot, uid, text))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    success = sum(1 for r in results if r is True)
    failures = len(results) - success
    return success, failures


async def _send_single(bot: AsyncTeleBot, user_id: int, text: str) -> bool:
    try:
        await bot.send_message(user_id, text)
        logger.info(f"Sent to {user_id}")
        return True
    except ApiTelegramException as e:
        # Common errors: bot blocked, user deactivated, chat not found
        logger.warning(f"Telegram API error for {user_id}: {e!r}")
    except Exception as e:  # noqa: BLE001
        logger.error(f"Unexpected error sending to {user_id}: {e}")
    return False


async def broadcast(message: str, dry_run: bool, limit: int | None,
                     chunk_size: int, delay: float) -> None:
    """Broadcast logic."""
    # Ensure DB tables exist (especially if running standalone)
    try:
        init_db()
    except Exception as e:  # noqa: BLE001
        logger.warning(f"Database initialization warning: {e}")

    user_ids = get_all_user_ids(limit)
    total = len(user_ids)
    if total == 0:
        logger.info("No users found. Exiting.")
        return

    logger.info(f"Found {total} user(s) to broadcast.")
    logger.info(f"Message preview: {message}")

    if dry_run:
        logger.info("Dry run enabled - not sending.")
        # Optionally list first few IDs
        preview = user_ids[:10]
        logger.info(f"First {len(preview)} IDs: {preview}")
        return

    bot = AsyncTeleBot(config.TOKEN)

    sent = 0
    failed = 0
    # Iterate in chunks
    for i in range(0, total, chunk_size):
        chunk = user_ids[i:i + chunk_size]
        success, failures = await send_chunk(bot, chunk, message)
        sent += success
        failed += failures
        logger.info(f"Progress: {sent} sent / {failed} failed / {total - (i + len(chunk))} remaining")
        if i + chunk_size < total:  # delay between chunks
            await asyncio.sleep(delay)

    logger.info("Broadcast complete")
    logger.info(f"Summary: Sent={sent}, Failed={failed}, Total={total}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Broadcast Telegram message to all users.")
    parser.add_argument('-m', '--message', help='Message text to send', default=DEFAULT_MESSAGE)
    parser.add_argument('--dry-run', action='store_true', help='Only show counts, do not send')
    parser.add_argument('--yes', action='store_true', help='Skip interactive confirmation')
    parser.add_argument('--limit', type=int, help='Send only to first N users (testing)')
    parser.add_argument('--chunk-size', type=int, default=20, help='Concurrent send chunk size')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between chunks in seconds')
    return parser.parse_args()


def confirm(message: str) -> bool:
    print("\nAbout to broadcast this message to all users:\n")
    print(message)
    print("\nType 'yes' to continue: ", end='')
    resp = input().strip().lower()
    return resp == 'yes'


def main():  # pragma: no cover - CLI entry point
    args = parse_args()
    if not args.yes and not args.dry_run:
        if not confirm(args.message):
            logger.info("Cancelled by user.")
            return
    asyncio.run(broadcast(
        message=args.message,
        dry_run=args.dry_run,
        limit=args.limit,
        chunk_size=args.chunk_size,
        delay=args.delay,
    ))


if __name__ == '__main__':
    main()
