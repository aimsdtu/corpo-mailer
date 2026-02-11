"""Test script for user service"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.api.models.user import UserCreate, UserCreateOAuth, PasswordUpdate
from app.api.services.userservice import UserService
from app.db.session import get_database, close_database


async def test_user_service():
    """Test user service operations"""
    print("🔄 Connecting to database...")
    db = await get_database()
    service = UserService(db)
    
    print("\n" + "="*50)
    print("TEST 1: Create Normal User")
    print("="*50)
    
    try:
        user_create = UserCreate(
            registered_email="test.student@gmail.com",
            name="Test Student",
            hashed_password="hashedpassword123",  # In production, this comes pre-hashed from frontend
            pfp="https://example.com/avatar.jpg",
            email_provider="custom",
            access_level="user",
            designation="student",
            age=21,
            gender="male",
            dtu_id_number="2K21/CO/001",
            dtu_email="test.student@dtu.ac.in",
            course_and_year_of_study="B.Tech CSE - 3rd Year"
        )
        
        created_user = service.create_user(user_create)
        print(f"✅ User created successfully!")
        print(f"   UUID: {created_user.uuid}")
        print(f"   Email: {created_user.registered_email}")
        print(f"   Name: {created_user.name}")
        print(f"   Metadata: {created_user.metadata}")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return
    
    print("\n" + "="*50)
    print("TEST 2: Get User by Email")
    print("="*50)
    
    try:
        user = service.get_user_by_email("test.student@gmail.com")
        if user:
            print(f"✅ User found!")
            print(f"   UUID: {user.uuid}")
            print(f"   Name: {user.name}")
        else:
            print("❌ User not found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("TEST 3: Get User by DTU Email (from metadata)")
    print("="*50)
    
    try:
        user = service.get_user_by_dtu_email("test.student@dtu.ac.in")
        if user:
            print(f"✅ User found by DTU email!")
            print(f"   UUID: {user.uuid}")
            print(f"   Name: {user.name}")
        else:
            print("❌ User not found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("TEST 4: Create OAuth User")
    print("="*50)
    
    try:
        oauth_user_create = UserCreateOAuth(
            registered_email="oauth.student@gmail.com",
            name="OAuth Student",
            pfp="https://lh3.googleusercontent.com/...",
            oauth_provider="google",
            oauth_id="google_123456789",
            email_provider="google",
            access_level="user",
            designation="student",
            age=22,
            gender="female",
            dtu_id_number="2K21/CO/002",
            dtu_email="oauth.student@dtu.ac.in",
            course_and_year_of_study="B.Tech CSE - 4th Year"
        )
        
        oauth_user = service.create_user_oauth(oauth_user_create)
        print(f"✅ OAuth user created successfully!")
        print(f"   UUID: {oauth_user.uuid}")
        print(f"   OAuth Provider: {oauth_user.oauth_provider}")
        print(f"   OAuth ID: {oauth_user.oauth_id}")
        
    except Exception as e:
        print(f"❌ Error creating OAuth user: {e}")
    
    print("\n" + "="*50)
    print("TEST 5: Get All Users")
    print("="*50)
    
    try:
        all_users = service.get_all_users()
        print(f"✅ Found {len(all_users)} users:")
        for user in all_users:
            print(f"   - {user.name} ({user.registered_email})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("TEST 6: Get Users by Designation")
    print("="*50)
    
    try:
        students = service.get_users_by_designation("student")
        print(f"✅ Found {len(students)} students:")
        for student in students:
            designation = student.metadata.get('designation')
            print(f"   - {student.name} (Designation: {designation})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("TEST 7: Check Email Exists")
    print("="*50)
    
    try:
        exists = service.check_email_exists("test.student@gmail.com")
        print(f"✅ Email exists: {exists}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("TEST 8: Count Users")
    print("="*50)
    
    try:
        count = service.count_users()
        print(f"✅ Total users: {count}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("🧹 Cleaning up test data...")
    print("="*50)
    
    # Clean up - delete test users
    try:
        service.delete_user(created_user.uuid)
        service.delete_user(oauth_user.uuid)
        print("✅ Test data cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup error: {e}")
    
    await close_database()
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(test_user_service())