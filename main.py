from telegram import *
from database import *


if __name__ == "__main__":
    print('  ( ! )  Бот запущен')
    users_table_creation()
    asyncio.run(main())
