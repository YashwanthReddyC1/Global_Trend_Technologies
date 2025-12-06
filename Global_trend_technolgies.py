#!/usr/bin/env python3
"""
==============================================================================
GLOBAL TREND TECHNOLOGIES - API Integration Assignment
Using JSONPlaceholder API with Professional Interface
==============================================================================
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional, Any

# ============================================================================
# AUTO-INSTALL DEPENDENCIES
# ============================================================================

def install_requests_if_needed():
    """Automatically install requests library if not available"""
    try:
        import requests
        return requests
    except ImportError:
        print("\n📦 Installing required 'requests' library...")
        print("This is a one-time setup.")
        print("-" * 50)
        
        import subprocess
        import sys
        
        try:
            # Try to install requests
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            print("✅ Successfully installed 'requests' library!")
            print("-" * 50)
            
            # Now import it
            import requests
            return requests
        except Exception as e:
            print(f"\n❌ Failed to install requests: {e}")
            print("\n📝 Manual installation required:")
            print("1. Open terminal/command prompt")
            print("2. Run: pip install requests")
            print("3. Run this program again")
            print("\nPress Enter to exit...")
            input()
            sys.exit(1)

# Install requests automatically
requests = install_requests_if_needed()

# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE_URL = "https://jsonplaceholder.typicode.com"
REQUEST_TIMEOUT = 15
CACHE_TTL = 300  # 5 minutes
CACHE_FILE = "global_trend_cache.json"

# ============================================================================
# ERROR HANDLING SYSTEM
# ============================================================================

class ErrorHandler:
    """Handles all types of errors as per assignment requirements"""
    
    @staticmethod
    def handle(error_type: str, details: str = "") -> None:
        """Centralized error handling with user-friendly messages"""
        
        error_messages = {
            'network': f"❌ NETWORK FAILURE: Cannot connect to API\n   Details: {details}\n   Please check your internet connection.",
            'timeout': f"⏰ TIMEOUT: Request took too long (>15 seconds)\n   Server might be busy or unresponsive.",
            'http': f"🌐 HTTP ERROR: Server returned status {details}",
            'json': f"📄 INVALID RESPONSE: API returned non-JSON data\n   Data format is incorrect.",
            'malformed': f"⚠️ MALFORMED DATA: Missing or invalid data fields\n   Details: {details}",
            'invalid_input': f"🔍 INVALID INPUT: {details}\n   Please enter a valid value.",
            'not_found': f"🔎 NOT FOUND: {details}\n   This item doesn't exist in the database.",
            'cache': f"💾 CACHE ERROR: {details}\n   Starting with fresh data from API.",
        }
        
        message = error_messages.get(error_type, f"Unknown error: {details}")
        print(f"\n{message}")
        return None

# ============================================================================
# API CLIENT - Fetches data from JSONPlaceholder API
# ============================================================================

class APIClient:
    """Fetches data from JSONPlaceholder API with comprehensive error handling"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GlobalTrend-Technologies-API/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, endpoint: str) -> Optional[Any]:
        """Make HTTP request with comprehensive error handling"""
        url = f"{API_BASE_URL}/{endpoint}"
        
        try:
            print(f"\n🔍 Fetching: {url}")
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            
            # Check for HTTP errors
            if response.status_code != 200:
                ErrorHandler.handle('http', f"{response.status_code} for {endpoint}")
                return None
            
            # Parse JSON
            try:
                data = response.json()
                return data
            except json.JSONDecodeError:
                ErrorHandler.handle('json', f"Could not parse JSON from {endpoint}")
                return None
                
        except requests.exceptions.Timeout:
            ErrorHandler.handle('timeout', f"Request to {endpoint} timed out")
            return None
        except requests.exceptions.ConnectionError:
            ErrorHandler.handle('network', f"Failed to connect to {endpoint}")
            return None
        except Exception as e:
            ErrorHandler.handle('malformed', f"Unexpected error: {str(e)}")
            return None
    
    def get_posts(self) -> Optional[List[Dict]]:
        """Get all posts from API - Endpoint 1"""
        return self._make_request("posts")
    
    def get_users(self) -> Optional[List[Dict]]:
        """Get all users from API - Endpoint 2"""
        return self._make_request("users")
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """Get single post by ID"""
        result = self._make_request(f"posts/{post_id}")
        return result if isinstance(result, dict) else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get single user by ID"""
        result = self._make_request(f"users/{user_id}")
        return result if isinstance(result, dict) else None
    
    def get_comments_for_post(self, post_id: int) -> Optional[List[Dict]]:
        """Get comments for a post"""
        return self._make_request(f"posts/{post_id}/comments")

# ============================================================================
# CACHE SYSTEM - Implements data storage/caching
# ============================================================================

class CacheManager:
    """Manages data caching (memory + file) as per assignment requirements"""
    
    def __init__(self):
        self.cache = {
            'posts': {'data': None, 'timestamp': 0},
            'users': {'data': None, 'timestamp': 0},
            'individual_posts': {},  # post_id -> {data, timestamp}
            'individual_users': {}   # user_id -> {data, timestamp}
        }
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from file if it exists"""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    saved_cache = json.load(f)
                    # Merge with current cache
                    for key in ['posts', 'users']:
                        if key in saved_cache:
                            self.cache[key] = saved_cache[key]
                print(f"📂 Loaded cached data from {CACHE_FILE}")
            except Exception as e:
                print(f"⚠️ Could not load cache file: {e}")
                # Start with fresh cache
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            with open(CACHE_FILE, 'w') as f:
                json.dump({
                    'posts': self.cache['posts'],
                    'users': self.cache['users']
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save cache file: {e}")
    
    def _is_valid(self, timestamp: float) -> bool:
        """Check if cache is still within TTL"""
        return (time.time() - timestamp) < CACHE_TTL
    
    # Public methods for data access
    def get_posts(self) -> Optional[List[Dict]]:
        """Get cached posts if available and fresh"""
        cache_entry = self.cache['posts']
        if cache_entry['data'] and self._is_valid(cache_entry['timestamp']):
            print("📊 Returning posts from cache")
            return cache_entry['data']
        return None
    
    def get_users(self) -> Optional[List[Dict]]:
        """Get cached users if available and fresh"""
        cache_entry = self.cache['users']
        if cache_entry['data'] and self._is_valid(cache_entry['timestamp']):
            print("📊 Returning users from cache")
            return cache_entry['data']
        return None
    
    def get_post(self, post_id: int) -> Optional[Dict]:
        """Get cached individual post"""
        if str(post_id) in self.cache['individual_posts']:
            entry = self.cache['individual_posts'][str(post_id)]
            if self._is_valid(entry['timestamp']):
                return entry['data']
        return None
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get cached individual user"""
        if str(user_id) in self.cache['individual_users']:
            entry = self.cache['individual_users'][str(user_id)]
            if self._is_valid(entry['timestamp']):
                return entry['data']
        return None
    
    def save_posts(self, posts: List[Dict]):
        """Save posts to cache"""
        if posts:
            self.cache['posts'] = {'data': posts, 'timestamp': time.time()}
            self._save_cache()
    
    def save_users(self, users: List[Dict]):
        """Save users to cache"""
        if users:
            self.cache['users'] = {'data': users, 'timestamp': time.time()}
            self._save_cache()
    
    def save_post(self, post_id: int, post: Dict):
        """Save individual post to cache"""
        if post:
            self.cache['individual_posts'][str(post_id)] = {
                'data': post, 
                'timestamp': time.time()
            }
    
    def save_user(self, user_id: int, user: Dict):
        """Save individual user to cache"""
        if user:
            self.cache['individual_users'][str(user_id)] = {
                'data': user, 
                'timestamp': time.time()
            }
    
    def get_cache_info(self) -> Dict:
        """Get cache statistics"""
        posts_age = time.time() - self.cache['posts']['timestamp'] if self.cache['posts']['data'] else 0
        users_age = time.time() - self.cache['users']['timestamp'] if self.cache['users']['data'] else 0
        
        return {
            'posts_cached': self.cache['posts']['data'] is not None,
            'users_cached': self.cache['users']['data'] is not None,
            'individual_posts_cached': len(self.cache['individual_posts']),
            'individual_users_cached': len(self.cache['individual_users']),
            'posts_cache_age_sec': int(posts_age),
            'users_cache_age_sec': int(users_age),
            'cache_file': CACHE_FILE,
            'cache_ttl_sec': CACHE_TTL
        }

# ============================================================================
# FILTERING SYSTEM - Implements filtering options
# ============================================================================

class DataFilter:
    """Applies filters to data as per assignment requirements"""
    
    @staticmethod
    def filter_by_user_id(items: List[Dict], user_id: int) -> List[Dict]:
        """Filter items by user ID"""
        return [item for item in items if item.get('userId') == user_id]
    
    @staticmethod
    def filter_by_keyword(items: List[Dict], keyword: str, fields: List[str]) -> List[Dict]:
        """Filter items by keyword in specified fields"""
        if not keyword:
            return items
        
        keyword = keyword.lower()
        results = []
        
        for item in items:
            for field in fields:
                if field in item and keyword in str(item[field]).lower():
                    results.append(item)
                    break  # Don't add same item multiple times
        
        return results
    
    @staticmethod
    def filter_by_id_range(items: List[Dict], min_id: int, max_id: int) -> List[Dict]:
        """Filter items by ID range"""
        return [item for item in items if min_id <= item.get('id', 0) <= max_id]
    
    @staticmethod
    def apply_post_filters(posts: List[Dict], filters: Dict) -> List[Dict]:
        """Apply all filters to posts"""
        if not posts:
            return []
        
        filtered = posts
        
        # Apply user ID filter
        if 'user_id' in filters:
            filtered = DataFilter.filter_by_user_id(filtered, filters['user_id'])
        
        # Apply keyword filter
        if 'keyword' in filters:
            filtered = DataFilter.filter_by_keyword(filtered, filters['keyword'], ['title', 'body'])
        
        # Apply ID range filter
        if 'min_id' in filters and 'max_id' in filters:
            filtered = DataFilter.filter_by_id_range(filtered, filters['min_id'], filters['max_id'])
        
        return filtered
    
    @staticmethod
    def apply_user_filters(users: List[Dict], filters: Dict) -> List[Dict]:
        """Apply all filters to users"""
        if not users:
            return []
        
        filtered = users
        
        # Apply keyword filter
        if 'keyword' in filters:
            filtered = DataFilter.filter_by_keyword(filtered, filters['keyword'], ['name', 'email', 'username'])
        
        # Apply ID range filter
        if 'min_id' in filters and 'max_id' in filters:
            filtered = DataFilter.filter_by_id_range(filtered, filters['min_id'], filters['max_id'])
        
        return filtered

# ============================================================================
# MAIN APPLICATION - Coordinates all components
# ============================================================================

class Application:
    """Main application that coordinates all components"""
    
    def __init__(self):
        self.api = APIClient()
        self.cache = CacheManager()
        self.filter = DataFilter()
    
    def fetch_posts(self, force_fresh: bool = False) -> Optional[List[Dict]]:
        """Get posts (from cache if available)"""
        if not force_fresh:
            cached = self.cache.get_posts()
            if cached:
                return cached
        
        print("🌐 Fetching posts from API...")
        posts = self.api.get_posts()
        if posts:
            self.cache.save_posts(posts)
            print(f"✅ Fetched {len(posts)} posts")
        return posts
    
    def fetch_users(self, force_fresh: bool = False) -> Optional[List[Dict]]:
        """Get users (from cache if available)"""
        if not force_fresh:
            cached = self.cache.get_users()
            if cached:
                return cached
        
        print("🌐 Fetching users from API...")
        users = self.api.get_users()
        if users:
            self.cache.save_users(users)
            print(f"✅ Fetched {len(users)} users")
        return users
    
    def get_post_details(self, post_id: int) -> Optional[Dict]:
        """Get post details with caching"""
        cached = self.cache.get_post(post_id)
        if cached:
            return cached
        
        print(f"🔍 Fetching post {post_id} from API...")
        post = self.api.get_post_by_id(post_id)
        if post:
            self.cache.save_post(post_id, post)
        return post
    
    def get_user_details(self, user_id: int) -> Optional[Dict]:
        """Get user details with caching"""
        cached = self.cache.get_user(user_id)
        if cached:
            return cached
        
        print(f"🔍 Fetching user {user_id} from API...")
        user = self.api.get_user_by_id(user_id)
        if user:
            self.cache.save_user(user_id, user)
        return user
    
    def get_post_comments(self, post_id: int) -> Optional[List[Dict]]:
        """Get comments for a post"""
        return self.api.get_comments_for_post(post_id)
    
    def get_filtered_posts(self, filters: Dict) -> List[Dict]:
        """Get posts with filters applied"""
        posts = self.fetch_posts()
        if not posts:
            return []
        
        return self.filter.apply_post_filters(posts, filters)
    
    def get_filtered_users(self, filters: Dict) -> List[Dict]:
        """Get users with filters applied"""
        users = self.fetch_users()
        if not users:
            return []
        
        return self.filter.apply_user_filters(users, filters)

# ============================================================================
# USER INTERFACE - Command Line Interface
# ============================================================================

class UserInterface:
    """Handles all user interactions"""
    
    def __init__(self, app: Application):
        self.app = app
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title: str):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f" {title}")
        print("=" * 60)
    
    @staticmethod
    def print_section(title: str):
        """Print section separator"""
        print(f"\n{title}")
        print("-" * 40)
    
    def get_post_filters(self) -> Dict:
        """Get filter options for posts"""
        filters = {}
        
        self.print_section("🔍 FILTER OPTIONS FOR POSTS")
        print("1. Filter by User ID")
        print("2. Filter by Keyword (title/body)")
        print("3. Filter by ID Range")
        print("4. Show All Posts (no filter)")
        
        try:
            choice = input("\nChoose option (1-4): ").strip()
            
            if choice == "1":
                user_id = int(input("Enter User ID (1-10): "))
                if 1 <= user_id <= 10:
                    filters['user_id'] = user_id
                else:
                    ErrorHandler.handle('invalid_input', "User ID must be between 1-10")
            
            elif choice == "2":
                keyword = input("Enter keyword to search: ").strip()
                if keyword:
                    filters['keyword'] = keyword
            
            elif choice == "3":
                min_id = int(input("Enter minimum ID: "))
                max_id = int(input("Enter maximum ID: "))
                if min_id <= max_id:
                    filters['min_id'] = min_id
                    filters['max_id'] = max_id
                else:
                    ErrorHandler.handle('invalid_input', "Minimum ID must be less than maximum ID")
            
            elif choice != "4":
                ErrorHandler.handle('invalid_input', "Please choose 1-4")
        
        except ValueError:
            ErrorHandler.handle('invalid_input', "Please enter valid numbers")
        
        return filters
    
    def get_user_filters(self) -> Dict:
        """Get filter options for users"""
        filters = {}
        
        self.print_section("🔍 FILTER OPTIONS FOR USERS")
        print("1. Filter by Keyword (name/email/username)")
        print("2. Filter by ID Range")
        print("3. Show All Users (no filter)")
        
        try:
            choice = input("\nChoose option (1-3): ").strip()
            
            if choice == "1":
                keyword = input("Enter keyword to search: ").strip()
                if keyword:
                    filters['keyword'] = keyword
            
            elif choice == "2":
                min_id = int(input("Enter minimum ID: "))
                max_id = int(input("Enter maximum ID: "))
                if min_id <= max_id:
                    filters['min_id'] = min_id
                    filters['max_id'] = max_id
                else:
                    ErrorHandler.handle('invalid_input', "Minimum ID must be less than maximum ID")
            
            elif choice != "3":
                ErrorHandler.handle('invalid_input', "Please choose 1-3")
        
        except ValueError:
            ErrorHandler.handle('invalid_input', "Please enter valid numbers")
        
        return filters
    
    def display_posts(self, posts: List[Dict]):
        """Display posts in formatted table"""
        if not posts:
            print("\n📭 No posts found")
            return
        
        print(f"\n📋 FOUND {len(posts)} POSTS:")
        print("=" * 80)
        
        for i, post in enumerate(posts[:15], 1):  # Show first 15
            title = post.get('title', 'No Title')
            print(f"{i:3}. ID: {post.get('id', 'N/A'):<4} | "
                  f"User ID: {post.get('userId', 'N/A'):<3} | "
                  f"Title: {title[:50]}{'...' if len(title) > 50 else ''}")
        
        if len(posts) > 15:
            print(f"\n... and {len(posts) - 15} more posts")
    
    def display_users(self, users: List[Dict]):
        """Display users in formatted table"""
        if not users:
            print("\n📭 No users found")
            return
        
        print(f"\n📋 FOUND {len(users)} USERS:")
        print("=" * 70)
        
        for i, user in enumerate(users, 1):
            print(f"{i:3}. ID: {user.get('id', 'N/A'):<3} | "
                  f"Name: {user.get('name', 'No Name'):<20} | "
                  f"Email: {user.get('email', 'No Email')}")
    
    def list_posts(self):
        """List posts with filtering options"""
        self.print_header("📝 LIST POSTS")
        
        posts = self.app.fetch_posts()
        if not posts:
            print("❌ Could not fetch posts from API or cache")
            return
        
        filters = self.get_post_filters()
        filtered_posts = self.app.get_filtered_posts(filters)
        
        self.display_posts(filtered_posts)
        
        # Show filter summary
        if filters:
            self.print_section("📊 FILTER SUMMARY")
            for key, value in filters.items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
            print(f"  • Results: {len(filtered_posts)} of {len(posts)} posts")
    
    def list_users(self):
        """List users with filtering options"""
        self.print_header("👥 LIST USERS")
        
        users = self.app.fetch_users()
        if not users:
            print("❌ Could not fetch users from API or cache")
            return
        
        filters = self.get_user_filters()
        filtered_users = self.app.get_filtered_users(filters)
        
        self.display_users(filtered_users)
    
    def view_post_details(self):
        """View detailed post information by ID"""
        self.print_header("🔍 VIEW POST DETAILS")
        
        try:
            post_id = int(input("Enter Post ID (1-100): "))
            if not 1 <= post_id <= 100:
                ErrorHandler.handle('invalid_input', "Post ID must be between 1-100")
                return
        except ValueError:
            ErrorHandler.handle('invalid_input', "Post ID must be a number")
            return
        
        post = self.app.get_post_details(post_id)
        
        if post:
            self.print_section(f"📝 POST #{post['id']}")
            print(f"Title: {post.get('title', 'No Title')}")
            print(f"\nContent:\n{post.get('body', 'No Content')}")
            print(f"\nAuthor: User #{post.get('userId', 'N/A')}")
            
            # Show comments if available
            show_comments = input("\nView comments for this post? (y/n): ").lower()
            if show_comments == 'y':
                comments = self.app.get_post_comments(post_id)
                if comments:
                    print(f"\n💬 COMMENTS ({len(comments)}):")
                    for i, comment in enumerate(comments[:5], 1):  # Show first 5
                        print(f"\n  {i}. {comment.get('name', 'Anonymous')}")
                        print(f"     Email: {comment.get('email', 'No email')}")
                        print(f"     {comment.get('body', 'No comment')[:80]}...")
                    if len(comments) > 5:
                        print(f"\n  ... and {len(comments) - 5} more comments")
                else:
                    print("No comments available for this post.")
        else:
            ErrorHandler.handle('not_found', f"Post {post_id} not found")
    
    def view_user_details(self):
        """View detailed user information by ID"""
        self.print_header("👤 VIEW USER DETAILS")
        
        try:
            user_id = int(input("Enter User ID (1-10): "))
            if not 1 <= user_id <= 10:
                ErrorHandler.handle('invalid_input', "User ID must be between 1-10")
                return
        except ValueError:
            ErrorHandler.handle('invalid_input', "User ID must be a number")
            return
        
        user = self.app.get_user_details(user_id)
        
        if user:
            self.print_section(f"👤 USER #{user['id']}")
            print(f"Name: {user.get('name', 'No Name')}")
            print(f"Username: {user.get('username', 'N/A')}")
            print(f"Email: {user.get('email', 'No Email')}")
            print(f"Phone: {user.get('phone', 'N/A')}")
            print(f"Website: {user.get('website', 'N/A')}")
            
            address = user.get('address', {})
            if address:
                print(f"\n📍 ADDRESS:")
                print(f"  Street: {address.get('street', 'N/A')}")
                print(f"  Suite: {address.get('suite', 'N/A')}")
                print(f"  City: {address.get('city', 'N/A')}")
                print(f"  Zipcode: {address.get('zipcode', 'N/A')}")
            
            company = user.get('company', {})
            if company:
                print(f"\n🏢 COMPANY:")
                print(f"  Name: {company.get('name', 'N/A')}")
                print(f"  Catchphrase: {company.get('catchPhrase', 'N/A')}")
                print(f"  Business: {company.get('bs', 'N/A')}")
            
            # Show user's posts
            show_posts = input("\nView posts by this user? (y/n): ").lower()
            if show_posts == 'y':
                filters = {'user_id': user_id}
                user_posts = self.app.get_filtered_posts(filters)
                if user_posts:
                    print(f"\n📝 USER HAS {len(user_posts)} POSTS:")
                    for i, post in enumerate(user_posts[:5], 1):
                        print(f"  {i}. {post.get('title', 'No Title')[:60]}...")
                    if len(user_posts) > 5:
                        print(f"  ... and {len(user_posts) - 5} more posts")
        else:
            ErrorHandler.handle('not_found', f"User {user_id} not found")
    
    def refresh_data(self):
        """Force refresh data from API"""
        self.print_header("🔄 REFRESH DATA FROM API")
        
        print("⚠️ This will fetch fresh data from the API and update cache.")
        
        choice = input("\nRefresh: (1) Posts, (2) Users, or (3) Both? (1-3): ").strip()
        
        if choice in ["1", "3"]:
            print("\n🔄 Refreshing posts...")
            posts = self.app.fetch_posts(force_fresh=True)
            if posts:
                print(f"✅ Updated {len(posts)} posts in cache")
            else:
                print("❌ Failed to refresh posts")
        
        if choice in ["2", "3"]:
            print("\n🔄 Refreshing users...")
            users = self.app.fetch_users(force_fresh=True)
            if users:
                print(f"✅ Updated {len(users)} users in cache")
            else:
                print("❌ Failed to refresh users")
    
    def show_cache_info(self):
        """Display cache information"""
        self.print_header("💾 CACHE INFORMATION")
        
        info = self.app.cache.get_cache_info()
        
        print("\n📊 CACHE STATUS:")
        print(f"  • Posts cached: {'✅ Yes' if info['posts_cached'] else '❌ No'}")
        print(f"  • Users cached: {'✅ Yes' if info['users_cached'] else '❌ No'}")
        print(f"  • Individual posts cached: {info['individual_posts_cached']}")
        print(f"  • Individual users cached: {info['individual_users_cached']}")
        
        if info['posts_cached']:
            age_min = info['posts_cache_age_sec'] // 60
            age_sec = info['posts_cache_age_sec'] % 60
            print(f"  • Posts cache age: {age_min}m {age_sec}s")
        
        if info['users_cached']:
            age_min = info['users_cache_age_sec'] // 60
            age_sec = info['users_cache_age_sec'] % 60
            print(f"  • Users cache age: {age_min}m {age_sec}s")
        
        print(f"\n⚙️ CACHE CONFIGURATION:")
        print(f"  • Cache file: {info['cache_file']}")
        print(f"  • Cache TTL: {info['cache_ttl_sec']} seconds ({info['cache_ttl_sec']//60} minutes)")
        
        # Show cache file size
        if os.path.exists(CACHE_FILE):
            size = os.path.getsize(CACHE_FILE)
            print(f"  • Cache file size: {size:,} bytes")
    
    def run(self):
        """Main application loop"""
        
        # Clear screen and show welcome
        self.clear_screen()
        print("\n" + "=" * 60)
        print("         🌐 GLOBAL TREND TECHNOLOGIES")
        print("=" * 60)
        print("    API Integration Assignment")
        print("    Using JSONPlaceholder API with Professional Interface")
        print("-" * 60)
        print("\n📋 This program demonstrates:")
        print("   • API integration with JSONPlaceholder")
        print("   • Data caching (memory + file storage)")
        print("   • Filtering capabilities")
        print("   • Comprehensive error handling")
        print("   • Clean CLI interface")
        print("\n" + "=" * 60)
        
        input("\nPress Enter to start...")
        
        # Main menu loop
        while True:
            try:
                self.clear_screen()
                print("\n" + "=" * 60)
                print("                      📱 MAIN MENU")
                print("=" * 60)
                print("\n1. 📝 List Posts (with filters)")
                print("2. 👥 List Users (with filters)")
                print("3. 🔍 View Post Details by ID")
                print("4. 👤 View User Details by ID")
                print("5. 🔄 Refresh Data from API")
                print("6. 💾 View Cache Information")
                print("7. 🚪 Exit Application")
                print("\n" + "-" * 60)
                
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == "1":
                    self.list_posts()
                elif choice == "2":
                    self.list_users()
                elif choice == "3":
                    self.view_post_details()
                elif choice == "4":
                    self.view_user_details()
                elif choice == "5":
                    self.refresh_data()
                elif choice == "6":
                    self.show_cache_info()
                elif choice == "7":
                    print("\n" + "=" * 60)
                    print("         👍 Thank you for using the application!")
                    print("=" * 60)
                    break
                else:
                    print("\n⚠️ Invalid choice. Please enter a number between 1-7.")
                    time.sleep(1)
                    continue
                
                # Pause before showing menu again
                input("\nPress Enter to return to menu...")
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Application interrupted. Exiting...")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again or contact support if issue persists.")
                input("\nPress Enter to continue...")

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

def main():
    """Main function that runs the entire program"""
    
    print("\n🚀 Starting Global Trend Technologies API Assignment...")
    print("-" * 50)
    
    # Check if we have internet connection (optional)
    try:
        print("🔗 Checking internet connection...")
        test_response = requests.get("https://jsonplaceholder.typicode.com", timeout=5)
        if test_response.status_code == 200:
            print("✅ Connected to JSONPlaceholder API")
        else:
            print("⚠️ API server responded with non-200 status")
    except:
        print("⚠️ No internet connection detected")
        print("   The app will use cached data if available")
    
    print("-" * 50)
    
    # Create and run application
    try:
        app = Application()
        ui = UserInterface(app)
        ui.run()
        
    except Exception as e:
        print(f"\n💥 FATAL ERROR: {e}")
        print("\nPlease contact support if this error persists.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("       ✅ completed successfully!")
    print("=" * 60)
    
    # Show goodbye message
    print("\n📁 Files created during execution:")
    if os.path.exists(CACHE_FILE):
        print(f"  • {CACHE_FILE} - Data cache file")
    print("\n👋 Goodbye!")
    print("-" * 60)

# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    # Add some colors for Windows users
    if os.name == 'nt':
        os.system('color')
    
    # Run the main function
    main()