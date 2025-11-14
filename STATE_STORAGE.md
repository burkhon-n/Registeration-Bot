State storage configuration

The bot supports configurable state storage backends to make registration flows resilient across worker restarts.

How to configure

- Default: pickle file storage

  - Set in environment: STATE_STORAGE=pickle
  - Optional: STATE_PICKLE_PATH to override file path. Defaults to `bot_states.pkl` next to `bot.py`.
- Redis (recommended for production with multiple workers)

  - Set in environment: STATE_STORAGE=redis
  - Provide Redis URL: STATE_REDIS_URL=redis://user:pass@host:6379/0
- Fallback: in-memory (StateMemoryStorage)

  - If neither pickle nor redis storage is available or initialization fails, the bot falls back to in-memory storage and logs a warning. In-memory storage loses all states when a worker restarts.

Notes

- If you use cPanel/Passenger with multiple workers, prefer Redis to share state between workers.
- If Redis isn't available, pickle provides a simple persistent file-based storage, but be careful about concurrent access when multiple workers write the same file.
- After changing `STATE_STORAGE`, restart the application (touch tmp/restart.txt or restart Passenger).

Example

1. Export environment variables (bash/zsh):

```bash
export STATE_STORAGE=redis
export STATE_REDIS_URL=redis://localhost:6379/0
```

Or for pickle storage:

```bash
export STATE_STORAGE=pickle
export STATE_PICKLE_PATH=/home/user/repositories/Registeration-Bot/bot_states.pkl
```
