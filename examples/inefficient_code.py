"""
Examples of Inefficient Code Patterns
This file demonstrates common performance anti-patterns.
See optimized_code.py for improved versions.
"""

import time
import re


# Example 1: Inefficient Loop - O(n²) complexity
def find_duplicates_inefficient(items):
    """Find duplicate items using nested loops - SLOW"""
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates


# Example 2: String Concatenation in Loop
def build_report_inefficient(data):
    """Build a report string using concatenation - SLOW for large data"""
    report = ""
    report += "=" * 50 + "\n"
    report += "Performance Report\n"
    report += "=" * 50 + "\n\n"
    
    for item in data:
        report += f"Item: {item['name']}\n"
        report += f"Value: {item['value']}\n"
        report += f"Status: {item['status']}\n"
        report += "-" * 30 + "\n"
    
    return report


# Example 3: Unnecessary Database Queries (N+1 Problem)
class UserRepository:
    """Simulates inefficient database access patterns"""
    
    def __init__(self):
        # Simulated database
        self.users_db = [
            {'id': i, 'name': f'User{i}', 'email': f'user{i}@example.com'}
            for i in range(100)
        ]
        self.posts_db = [
            {'id': i*10+j, 'user_id': i, 'title': f'Post {j} by User{i}'}
            for i in range(100) for j in range(10)
        ]
    
    def get_user(self, user_id):
        """Simulates single user query"""
        time.sleep(0.001)  # Simulate DB latency
        return next((u for u in self.users_db if u['id'] == user_id), None)
    
    def get_posts_by_user(self, user_id):
        """Simulates posts query for a user"""
        time.sleep(0.001)  # Simulate DB latency
        return [p for p in self.posts_db if p['user_id'] == user_id]
    
    def get_users_with_posts_inefficient(self, user_ids):
        """N+1 query problem - makes 2*N queries"""
        results = []
        for user_id in user_ids:
            user = self.get_user(user_id)  # Query 1, 2, 3, ...
            posts = self.get_posts_by_user(user_id)  # Query N+1, N+2, ...
            results.append({'user': user, 'posts': posts})
        return results


# Example 4: Using List for Membership Checks
def check_permissions_inefficient(usernames, allowed_list):
    """Check permissions using list lookup - O(n) per check"""
    # allowed_list is a regular list
    results = []
    for username in usernames:
        if username in allowed_list:  # Linear search - SLOW
            results.append(username)
    return results


# Example 5: Recompiling Regex in Loop
def validate_emails_inefficient(emails):
    """Validate emails by recompiling regex each time - SLOW"""
    valid_emails = []
    for email in emails:
        # Regex compiled on every iteration - WASTEFUL
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            valid_emails.append(email)
    return valid_emails


# Example 6: Inefficient Data Structure Selection
def count_word_frequency_inefficient(text):
    """Count word frequency using list of tuples - SLOW"""
    words = text.lower().split()
    frequency = []  # List of tuples - inefficient for lookups
    
    for word in words:
        found = False
        for i, (w, count) in enumerate(frequency):
            if w == word:
                frequency[i] = (w, count + 1)
                found = True
                break
        if not found:
            frequency.append((word, 1))
    
    return frequency


# Example 7: Creating Objects Unnecessarily
def process_timestamps_inefficient(records):
    """Create unnecessary objects in loop"""
    import datetime
    processed = []
    
    for record in records:
        # Creates new datetime object on each iteration
        current_time = datetime.datetime.now()
        record['processed_at'] = current_time.isoformat()
        record['timestamp'] = current_time.timestamp()
        processed.append(record)
    
    return processed


# Example 8: Copying Large Data Structures
def filter_data_inefficient(data, threshold):
    """Creates unnecessary copies of large data structures"""
    # Makes complete copy of entire dataset
    filtered = data.copy()
    
    # Remove items that don't meet threshold
    # O(n²) - iterates list AND each remove() is O(n)
    i = 0
    while i < len(filtered):
        if filtered[i]['value'] < threshold:
            filtered.pop(i)  # O(n) operation for each removal
        else:
            i += 1
    
    return filtered


# Example 9: Inefficient Sorting
def get_top_items_inefficient(items, n):
    """Sort entire list to get top N items - WASTEFUL"""
    # Sorts all items even though we only need top N
    sorted_items = sorted(items, key=lambda x: x['score'], reverse=True)
    return sorted_items[:n]


# Example 10: Nested Loop for Searching
def find_common_elements_inefficient(list1, list2):
    """Find common elements using nested loops - O(n*m)"""
    common = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2 and item1 not in common:
                common.append(item1)
    return common


# Benchmark function
def benchmark_function(func, *args, iterations=100):
    """Measure execution time of a function"""
    start = time.time()
    for _ in range(iterations):
        result = func(*args)
    end = time.time()
    avg_time = (end - start) / iterations
    return avg_time, result


if __name__ == "__main__":
    print("=" * 60)
    print("INEFFICIENT CODE EXAMPLES - PERFORMANCE BENCHMARKS")
    print("=" * 60)
    
    # Test 1: Find duplicates
    print("\n1. Finding Duplicates (O(n²) nested loops)")
    test_data = list(range(500)) + list(range(250))  # Create duplicates
    time_taken, result = benchmark_function(find_duplicates_inefficient, test_data, iterations=10)
    print(f"   Time: {time_taken*1000:.2f}ms | Found {len(result)} duplicates")
    
    # Test 2: String concatenation
    print("\n2. String Concatenation in Loop")
    data = [{'name': f'Item{i}', 'value': i*10, 'status': 'active'} for i in range(1000)]
    time_taken, result = benchmark_function(build_report_inefficient, data, iterations=10)
    print(f"   Time: {time_taken*1000:.2f}ms | Report length: {len(result)} chars")
    
    # Test 3: N+1 queries
    print("\n3. N+1 Database Query Problem")
    repo = UserRepository()
    user_ids = list(range(20))
    time_taken, result = benchmark_function(
        repo.get_users_with_posts_inefficient, user_ids, iterations=5
    )
    print(f"   Time: {time_taken*1000:.2f}ms | Fetched {len(result)} users with posts")
    
    # Test 4: List membership checks
    print("\n4. List Membership Checks (O(n) per check)")
    usernames = [f'user{i}' for i in range(1000)]
    allowed = [f'user{i}' for i in range(500, 1500)]
    time_taken, result = benchmark_function(
        check_permissions_inefficient, usernames, allowed, iterations=50
    )
    print(f"   Time: {time_taken*1000:.2f}ms | Authorized: {len(result)} users")
    
    # Test 5: Regex recompilation
    print("\n5. Regex Recompilation in Loop")
    emails = [f'user{i}@example.com' for i in range(1000)]
    time_taken, result = benchmark_function(validate_emails_inefficient, emails, iterations=20)
    print(f"   Time: {time_taken*1000:.2f}ms | Valid emails: {len(result)}")
    
    # Test 6: Word frequency with list
    print("\n6. Word Frequency with Inefficient Data Structure")
    text = " ".join([f"word{i%100}" for i in range(1000)])
    time_taken, result = benchmark_function(count_word_frequency_inefficient, text, iterations=10)
    print(f"   Time: {time_taken*1000:.2f}ms | Unique words: {len(result)}")
    
    print("\n" + "=" * 60)
    print("See optimized_code.py for improved implementations!")
    print("=" * 60)
