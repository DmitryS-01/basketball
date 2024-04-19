from config import *
from telegram import *
from database import *


users_table_creation()


if __name__ == "__main__":
    asyncio.run(main())
