# Performance Optimization Guide: Identifying and Fixing Slow/Inefficient Code

## Table of Contents
1. [Introduction](#introduction)
2. [Common Performance Anti-Patterns](#common-performance-anti-patterns)
3. [Language-Specific Optimizations](#language-specific-optimizations)
4. [Profiling and Measurement](#profiling-and-measurement)
5. [Best Practices](#best-practices)

## Introduction

Performance optimization is about making code run faster and use fewer resources. However, premature optimization can lead to complex, unmaintainable code. Always:
- **Profile first**: Measure before optimizing
- **Focus on bottlenecks**: Optimize the 20% that causes 80% of the problems
- **Maintain readability**: Don't sacrifice code clarity unless necessary

## Common Performance Anti-Patterns

### 1. Inefficient Loops and Iterations

#### ❌ Bad: Nested loops with unnecessary work
```python
# O(n²) - Quadratic time complexity
def find_duplicates_bad(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates
```

#### ✅ Good: Use sets for O(1) lookups
```python
# O(n) - Linear time complexity
def find_duplicates_good(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

### 2. String Concatenation in Loops

#### ❌ Bad: Repeated string concatenation
```python
# Creates new string object on each iteration
def build_string_bad(words):
    result = ""
    for word in words:
        result += word + " "
    return result
```

#### ✅ Good: Use join() or list accumulation
```python
def build_string_good(words):
    return " ".join(words)
```

### 3. Unnecessary Database Queries (N+1 Problem)

#### ❌ Bad: Query in loop
```python
# Makes N+1 database queries
def get_user_posts_bad(user_ids):
    results = []
    for user_id in user_ids:
        user = db.query("SELECT * FROM users WHERE id = ?", user_id)
        posts = db.query("SELECT * FROM posts WHERE user_id = ?", user_id)
        results.append({'user': user, 'posts': posts})
    return results
```

#### ✅ Good: Batch query with JOIN
```python
# Makes 1 database query
def get_user_posts_good(user_ids):
    query = """
        SELECT u.*, p.* 
        FROM users u 
        LEFT JOIN posts p ON u.id = p.user_id 
        WHERE u.id IN (?)
    """
    return db.query(query, user_ids)
```

### 4. Inefficient Data Structures

#### ❌ Bad: Using list for membership checks
```python
# O(n) for each lookup
allowed_users = ['user1', 'user2', 'user3', ...]  # list
if username in allowed_users:  # Linear search
    grant_access()
```

#### ✅ Good: Use set or dict for O(1) lookups
```python
# O(1) for each lookup
allowed_users = {'user1', 'user2', 'user3', ...}  # set
if username in allowed_users:  # Constant time
    grant_access()
```

### 5. Unnecessary Object Creation

#### ❌ Bad: Creating objects in loops
```javascript
// Creates new Date object on each iteration
for (let i = 0; i < items.length; i++) {
    const now = new Date();  // Wasteful
    items[i].timestamp = now.getTime();
}
```

#### ✅ Good: Reuse objects when possible
```javascript
const now = new Date();  // Create once
const timestamp = now.getTime();
for (let i = 0; i < items.length; i++) {
    items[i].timestamp = timestamp;
}
```

### 6. Inefficient Regular Expressions

#### ❌ Bad: Recompiling regex in loop
```python
for line in lines:
    if re.match(r'^\d{3}-\d{3}-\d{4}$', line):  # Compiles each time
        process_phone(line)
```

#### ✅ Good: Compile regex once
```python
phone_pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
for line in lines:
    if phone_pattern.match(line):
        process_phone(line)
```

### 7. Synchronous Operations in Async Context

#### ❌ Bad: Blocking operations
```javascript
// Blocks the entire event loop
async function processFiles(files) {
    for (const file of files) {
        const data = fs.readFileSync(file);  // Blocking!
        await processData(data);
    }
}
```

#### ✅ Good: Use async operations
```javascript
async function processFiles(files) {
    for (const file of files) {
        const data = await fs.promises.readFile(file);  // Non-blocking
        await processData(data);
    }
}
```

### 8. Memory Leaks

#### ❌ Bad: Unbounded caches and event listeners
```javascript
// Memory leak - cache grows indefinitely
const cache = {};
function getCachedData(key) {
    if (!cache[key]) {
        cache[key] = expensiveOperation(key);
    }
    return cache[key];
}
```

#### ✅ Good: Implement cache size limits
```javascript
class LRUCache {
    constructor(maxSize) {
        this.maxSize = maxSize;
        this.cache = new Map();
    }
    
    get(key) {
        if (!this.cache.has(key)) {
            return null;
        }
        const value = this.cache.get(key);
        this.cache.delete(key);
        this.cache.set(key, value);  // Move to end
        return value;
    }
    
    set(key, value) {
        if (this.cache.has(key)) {
            this.cache.delete(key);
        }
        this.cache.set(key, value);
        if (this.cache.size > this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
    }
}
```

## Language-Specific Optimizations

### Python
```python
# Use list comprehensions instead of append in loops
# ❌ Slow
result = []
for i in range(1000):
    result.append(i * 2)

# ✅ Fast
result = [i * 2 for i in range(1000)]

# Use generators for large datasets
# ❌ Memory intensive
def get_numbers():
    return [i for i in range(1000000)]

# ✅ Memory efficient
def get_numbers():
    return (i for i in range(1000000))

# Use local variables in loops
# ❌ Slower - global lookup each time
import math
for i in range(100000):
    result = math.sqrt(i)

# ✅ Faster - local variable
import math
sqrt = math.sqrt
for i in range(100000):
    result = sqrt(i)
```

### JavaScript
```javascript
// Use const/let appropriately
// ✅ const for immutable bindings (slightly faster)
const data = fetchData();

// Avoid delete operator on objects (breaks optimization)
// ❌ Slow
delete obj.property;

// ✅ Fast
obj.property = undefined;

// Use array methods efficiently
// ❌ Multiple passes
const filtered = arr.filter(x => x > 0);
const doubled = filtered.map(x => x * 2);

// ✅ Single pass
const result = arr.reduce((acc, x) => {
    if (x > 0) acc.push(x * 2);
    return acc;
}, []);
```

### Java
```java
// Use StringBuilder for string concatenation
// ❌ Slow - creates many String objects
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i;
}

// ✅ Fast
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);
}
String result = sb.toString();

// Use appropriate collection sizes
// ❌ Multiple resizes
List<String> list = new ArrayList<>();  // Default size 10

// ✅ Single allocation
List<String> list = new ArrayList<>(1000);
```

### SQL
```sql
-- ❌ Bad: SELECT *
SELECT * FROM users WHERE age > 18;

-- ✅ Good: Select only needed columns
SELECT id, name, email FROM users WHERE age > 18;

-- ❌ Bad: Missing index
SELECT * FROM orders WHERE customer_id = 123;

-- ✅ Good: Add index
CREATE INDEX idx_customer_id ON orders(customer_id);
SELECT * FROM orders WHERE customer_id = 123;

-- ❌ Bad: Function on indexed column
SELECT * FROM users WHERE YEAR(created_at) = 2023;

-- ✅ Good: Maintain index usage
SELECT * FROM users 
WHERE created_at >= '2023-01-01' 
  AND created_at < '2024-01-01';
```

## Profiling and Measurement

### Python Profiling
```python
import cProfile
import pstats

# Profile a function
cProfile.run('my_function()', 'output.prof')

# Analyze results
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(10)

# Line-by-line profiling with line_profiler
# Install: pip install line_profiler
# Usage: @profile decorator and kernprof -l -v script.py
```

### JavaScript Profiling
```javascript
// Node.js profiling
// Run with: node --prof script.js
// Analyze with: node --prof-process isolate-*-v8.log

// Browser profiling
console.time('operation');
// ... code to measure
console.timeEnd('operation');

// Performance API
const start = performance.now();
// ... code to measure
const end = performance.now();
console.log(`Time: ${end - start}ms`);
```

### Tools
- **Python**: cProfile, line_profiler, memory_profiler, py-spy
- **JavaScript**: Chrome DevTools, Node.js --prof, clinic.js
- **Java**: JProfiler, VisualVM, Java Mission Control
- **Database**: EXPLAIN, query analyzers, slow query logs
- **General**: Flamegraphs, perf (Linux), Instruments (macOS)

## Best Practices

### 1. Algorithm Complexity
Choose algorithms with better time complexity:
- O(1) - Constant: Hash table lookup
- O(log n) - Logarithmic: Binary search
- O(n) - Linear: Single loop
- O(n log n) - Linearithmic: Efficient sorting
- O(n²) - Quadratic: Nested loops (avoid when possible)
- O(2ⁿ) - Exponential: Recursive algorithms (optimize with memoization)

### 2. Caching Strategies
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # Results cached automatically
    return compute_result(n)
```

### 3. Lazy Loading
```python
# Don't load everything upfront
class DataProcessor:
    def __init__(self, filename):
        self.filename = filename
        self._data = None  # Lazy load
    
    @property
    def data(self):
        if self._data is None:
            self._data = self._load_data()
        return self._data
    
    def _load_data(self):
        with open(self.filename) as f:
            return f.read()
```

### 4. Batch Operations
```python
# ❌ Individual operations
for item in items:
    db.insert(item)

# ✅ Batch operation
db.batch_insert(items)
```

### 5. Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# I/O-bound tasks: Use threads
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(fetch_url, urls)

# CPU-bound tasks: Use processes
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(compute_heavy, data)
```

### 6. Database Optimization
- Use indexes on frequently queried columns
- Avoid SELECT * - fetch only needed columns
- Use connection pooling
- Implement pagination for large result sets
- Use prepared statements/parameterized queries
- Consider database-specific optimizations (partitioning, sharding)

### 7. Network Optimization
- Use HTTP/2 or HTTP/3
- Implement compression (gzip, brotli)
- Use CDNs for static assets
- Implement proper caching headers
- Batch API requests when possible
- Use connection keep-alive

### 8. Memory Management
- Profile memory usage regularly
- Use generators/iterators for large datasets
- Implement proper cleanup (close files, connections)
- Avoid circular references
- Use weak references when appropriate
- Monitor memory leaks in production

## Checklist for Performance Review

- [ ] Profiled the code to identify bottlenecks
- [ ] Reviewed algorithm complexity (aim for O(n log n) or better)
- [ ] Checked for N+1 query problems
- [ ] Optimized database queries with indexes
- [ ] Used appropriate data structures (sets for lookups, etc.)
- [ ] Implemented caching where beneficial
- [ ] Avoided unnecessary object creation in loops
- [ ] Used batch operations instead of individual calls
- [ ] Considered parallel processing for independent tasks
- [ ] Checked for memory leaks
- [ ] Verified string concatenation is efficient
- [ ] Compiled regular expressions outside loops
- [ ] Used async operations appropriately
- [ ] Implemented proper error handling (doesn't impact happy path)
- [ ] Measured performance improvement after changes

## Conclusion

Performance optimization is an iterative process. Always:
1. **Measure** performance before and after changes
2. **Profile** to identify real bottlenecks, not assumed ones
3. **Test** to ensure optimizations don't break functionality
4. **Monitor** production performance over time
5. **Document** why specific optimizations were made

Remember: "Premature optimization is the root of all evil" - Donald Knuth. Focus on writing clean, correct code first, then optimize where profiling shows it's needed.
