import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


env_path = os.path.join(os.getcwd(), "src/app/assets/.env")

# Load the environment variables
load_dotenv(env_path)

# Get the DATABASE_URL environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# print(env_path)
# print(DATABASE_URL)

# Create an engine for asynchronous communication with the database
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session maker for handling database sessions
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
