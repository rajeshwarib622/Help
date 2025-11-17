"""
Optimized Code Examples
This file demonstrates performance improvements over inefficient_code.py
"""

import time
import re
from collections import Counter, defaultdict
import heapq


# Example 1: Efficient duplicate finding - O(n) complexity
def find_duplicates_optimized(items):
    """Find duplicate items using set - FAST"""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)


# Example 2: Efficient String Building
def build_report_optimized(data):
    """Build a report string using join - FAST"""
    lines = [
        "=" * 50,
        "Performance Report",
        "=" * 50,
        ""
    ]
    
    for item in data:
        lines.extend([
            f"Item: {item['name']}",
            f"Value: {item['value']}",
            f"Status: {item['status']}",
            "-" * 30
        ])
    
    return "\n".join(lines)


# Example 3: Batch Database Queries
class UserRepositoryOptimized:
    """Demonstrates efficient database access patterns"""
    
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
    
    def get_users_with_posts_optimized(self, user_ids):
        """Batch query - makes only 2 queries total"""
        time.sleep(0.001)  # Simulate single DB query
        users = [u for u in self.users_db if u['id'] in user_ids]
        
        time.sleep(0.001)  # Simulate single DB query
        user_id_set = set(user_ids)
        posts = [p for p in self.posts_db if p['user_id'] in user_id_set]
        
        # Group posts by user_id
        posts_by_user = defaultdict(list)
        for post in posts:
            posts_by_user[post['user_id']].append(post)
        
        # Combine results
        results = []
        for user in users:
            results.append({
                'user': user,
                'posts': posts_by_user.get(user['id'], [])
            })
        return results


# Example 4: Using Set for Membership Checks
def check_permissions_optimized(usernames, allowed_list):
    """Check permissions using set lookup - O(1) per check"""
    allowed_set = set(allowed_list)  # Convert to set once
    results = []
    for username in usernames:
        if username in allowed_set:  # Constant time lookup - FAST
            results.append(username)
    return results


# Example 5: Compile Regex Once
# Compile regex at module level (outside function)
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_emails_optimized(emails):
    """Validate emails using pre-compiled regex - FAST"""
    valid_emails = []
    for email in emails:
        if EMAIL_PATTERN.match(email):  # Use compiled pattern
            valid_emails.append(email)
    return valid_emails


# Example 6: Efficient Data Structure Selection
def count_word_frequency_optimized(text):
    """Count word frequency using Counter - FAST"""
    words = text.lower().split()
    # Counter is optimized for this exact use case
    frequency = Counter(words)
    return list(frequency.items())


# Example 7: Reuse Objects
def process_timestamps_optimized(records):
    """Reuse datetime object instead of creating in loop"""
    import datetime
    
    # Create once, reuse for all records
    current_time = datetime.datetime.now()
    iso_time = current_time.isoformat()
    timestamp = current_time.timestamp()
    
    processed = []
    for record in records:
        record['processed_at'] = iso_time
        record['timestamp'] = timestamp
        processed.append(record)
    
    return processed


# Example 8: Filter Without Copying
def filter_data_optimized(data, threshold):
    """Filter using list comprehension - single pass"""
    # Single pass, no copying or removal operations
    return [item for item in data if item['value'] >= threshold]


# Example 9: Efficient Top-N Selection
def get_top_items_optimized(items, n):
    """Get top N items using heap - O(n log k) instead of O(n log n)"""
    # Only maintains heap of size n, much faster for small n
    return heapq.nlargest(n, items, key=lambda x: x['score'])


# Example 10: Set Intersection for Common Elements
def find_common_elements_optimized(list1, list2):
    """Find common elements using set intersection - O(n+m)"""
    # Convert to sets and use built-in intersection
    return list(set(list1) & set(list2))


# Benchmark function
def benchmark_function(func, *args, iterations=100):
    """Measure execution time of a function"""
    start = time.time()
    for _ in range(iterations):
        result = func(*args)
    end = time.time()
    avg_time = (end - start) / iterations
    return avg_time, result


def compare_implementations():
    """Compare inefficient vs optimized implementations"""
    from inefficient_code import (
        find_duplicates_inefficient,
        build_report_inefficient,
        UserRepository,
        check_permissions_inefficient,
        validate_emails_inefficient,
        count_word_frequency_inefficient,
    )
    
    print("=" * 70)
    print("PERFORMANCE COMPARISON: INEFFICIENT vs OPTIMIZED")
    print("=" * 70)
    
    # Test 1: Find duplicates
    print("\n1. Finding Duplicates")
    test_data = list(range(500)) + list(range(250))
    
    time_old, _ = benchmark_function(find_duplicates_inefficient, test_data, iterations=10)
    time_new, _ = benchmark_function(find_duplicates_optimized, test_data, iterations=10)
    speedup = time_old / time_new
    
    print(f"   Inefficient: {time_old*1000:.2f}ms (O(n²) nested loops)")
    print(f"   Optimized:   {time_new*1000:.2f}ms (O(n) with set)")
    print(f"   Speedup:     {speedup:.1f}x faster ⚡")
    
    # Test 2: String concatenation
    print("\n2. String Building")
    data = [{'name': f'Item{i}', 'value': i*10, 'status': 'active'} for i in range(1000)]
    
    time_old, _ = benchmark_function(build_report_inefficient, data, iterations=10)
    time_new, _ = benchmark_function(build_report_optimized, data, iterations=10)
    speedup = time_old / time_new
    
    print(f"   Inefficient: {time_old*1000:.2f}ms (string concatenation)")
    print(f"   Optimized:   {time_new*1000:.2f}ms (join)")
    print(f"   Speedup:     {speedup:.1f}x faster ⚡")
    
    # Test 3: Database queries
    print("\n3. Database Queries (N+1 Problem)")
    repo_old = UserRepository()
    repo_new = UserRepositoryOptimized()
    user_ids = list(range(20))
    
    time_old, _ = benchmark_function(
        repo_old.get_users_with_posts_inefficient, user_ids, iterations=5
    )
    time_new, _ = benchmark_function(
        repo_new.get_users_with_posts_optimized, user_ids, iterations=5
    )
    speedup = time_old / time_new
    
    print(f"   Inefficient: {time_old*1000:.2f}ms (40 queries)")
    print(f"   Optimized:   {time_new*1000:.2f}ms (2 queries)")
    print(f"   Speedup:     {speedup:.1f}x faster ⚡")
    
    # Test 4: Membership checks
    print("\n4. Membership Checks")
    usernames = [f'user{i}' for i in range(1000)]
    allowed = [f'user{i}' for i in range(500, 1500)]
    
    time_old, _ = benchmark_function(
        check_permissions_inefficient, usernames, allowed, iterations=50
    )
    time_new, _ = benchmark_function(
        check_permissions_optimized, usernames, allowed, iterations=50
    )
    speedup = time_old / time_new
    
    print(f"   Inefficient: {time_old*1000:.2f}ms (O(n) list lookup)")
    print(f"   Optimized:   {time_new*1000:.2f}ms (O(1) set lookup)")
    print(f"   Speedup:     {speedup:.1f}x faster ⚡")
    
    # Test 5: Regex validation
    print("\n5. Email Validation")
    emails = [f'user{i}@example.com' for i in range(1000)]
    
    time_old, _ = benchmark_function(validate_emails_inefficient, emails, iterations=20)
    time_new, _ = benchmark_function(validate_emails_optimized, emails, iterations=20)
    speedup = time_old / time_new
    
    print(f"   Inefficient: {time_old*1000:.2f}ms (recompile regex each time)")
    print(f"   Optimized:   {time_new*1000:.2f}ms (compiled regex)")
    print(f"   Speedup:     {speedup:.1f}x faster ⚡")
    
    # Test 6: Word frequency
    print("\n6. Word Frequency Count")
    text = " ".join([f"word{i%100}" for i in range(1000)])
    
    time_old, _ = benchmark_function(count_word_frequency_inefficient, text, iterations=10)
    time_new, _ = benchmark_function(count_word_frequency_optimized, text, iterations=10)
    speedup = time_old / time_new
    
    print(f"   Inefficient: {time_old*1000:.2f}ms (list of tuples)")
    print(f"   Optimized:   {time_new*1000:.2f}ms (Counter)")
    print(f"   Speedup:     {speedup:.1f}x faster ⚡")
    
    print("\n" + "=" * 70)
    print("Summary: Optimized code is significantly faster across all tests!")
    print("=" * 70)


if __name__ == "__main__":
    compare_implementations()
