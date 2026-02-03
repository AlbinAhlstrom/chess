import asyncio
import os
import sys

# Ensure backend can be imported
sys.path.append(os.getcwd())

from backend.database import init_db, async_session, User
from sqlalchemy import select

async def reproduce():
    # Initialize DB (creates tables if needed)
    print("Initializing DB...")
    await init_db()
    
    user_info = {
        "sub": "1234567890",
        "email": "test_reproduce@example.com",
        "name": "Test User",
        "picture": "https://example.com/pic.jpg"
    }
    
    print("Attempting to save user...")
    try:
        async with async_session() as session:
            async with session.begin():
                stmt = select(User).where(User.google_id == user_info["sub"])
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                if not user:
                    print("User not found, creating new...")
                    user = User(
                        google_id=user_info["sub"], 
                        email=user_info["email"], 
                        name=user_info["name"], 
                        picture=user_info.get("picture")
                    )
                    session.add(user)
                else:
                    print("User found, updating...")
                    user.name, user.picture = user_info["name"], user_info.get("picture")
                
                await session.flush()
                print("User saved successfully!")
                print(f"User ID: {user.id}")
                print(f"Default time: {user.default_time}")
                print(f"Username: {user.username}")
                
                # Simulate building the session dict
                user_dict = {
                    "id": str(user.google_id), 
                    "db_id": int(user.id), 
                    "name": str(user.name), 
                    "username": str(user.username) if user.username else None,
                    "email": str(user.email), 
                    "picture": user.picture,
                    "default_time": float(user.default_time),
                    "default_increment": float(user.default_increment),
                    "default_time_control_enabled": bool(user.default_time_control_enabled)
                }
                print(f"Session dict built: {user_dict}")
                
    except Exception as e:
        print(f"Error saving user to DB: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(reproduce())
