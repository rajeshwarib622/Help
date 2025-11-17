# Performance Optimization Quick Reference

## 🚀 Quick Wins - Apply These First

### 1. Algorithm Complexity
```
❌ O(n²): Nested loops
✅ O(n):  Single loop with set/dict
```

### 2. Data Structure Selection
```
❌ List for lookups: if item in my_list  # O(n)
✅ Set for lookups:  if item in my_set   # O(1)
```

### 3. String Building
```
❌ result = ""; for s in strings: result += s
✅ result = "".join(strings)
```

### 4. Database Queries
```
❌ for id in ids: query_user(id)  # N queries
✅ query_users_batch(ids)          # 1 query
```

### 5. Regex Compilation
```
❌ for text in texts: re.match(pattern, text)  # Recompile each time
✅ compiled = re.compile(pattern)               # Compile once
   for text in texts: compiled.match(text)
```

## 📊 Performance Impact Reference

| Optimization | Typical Speedup | When to Use |
|-------------|-----------------|-------------|
| O(n²) → O(n) using sets | **100-300x** | Finding duplicates, lookups |
| N+1 queries → batch | **10-50x** | Database operations |
| List → Set for membership | **50-200x** | Checking if item exists |
| String concat → join | **1.5-10x** | Building strings in loops |
| Compiled regex | **2-5x** | Validating many strings |
| Sort all → heapq.nlargest | **5-20x** | Getting top N items (N << total) |

## 🔍 How to Identify Issues

1. **Profile your code first**
   ```python
   import cProfile
   cProfile.run('my_function()')
   ```

2. **Look for these red flags**
   - Nested loops (especially with lookups)
   - String concatenation in loops
   - Database queries inside loops
   - Copying large data structures
   - Creating objects unnecessarily
   - List operations in tight loops

3. **Measure before and after**
   ```python
   import time
   start = time.time()
   # your code
   print(f"Time: {(time.time() - start)*1000:.2f}ms")
   ```

## 📚 Common Patterns

### Pattern 1: Find Duplicates
```python
# ❌ O(n²)
duplicates = []
for i in range(len(items)):
    for j in range(i+1, len(items)):
        if items[i] == items[j]:
            duplicates.append(items[i])

# ✅ O(n)
seen, duplicates = set(), set()
for item in items:
    if item in seen:
        duplicates.add(item)
    seen.add(item)
```

### Pattern 2: Filter Data
```python
# ❌ O(n²)
filtered = data.copy()
for item in data:
    if not condition(item):
        filtered.remove(item)  # O(n) each time

# ✅ O(n)
filtered = [item for item in data if condition(item)]
```

### Pattern 3: Count Frequencies
```python
# ❌ O(n²)
freq = []
for word in words:
    found = False
    for w, count in freq:
        if w == word:
            count += 1
            found = True
    if not found:
        freq.append((word, 1))

# ✅ O(n)
from collections import Counter
freq = Counter(words)
```

## ⚡ Memory vs Speed Trade-offs

| Approach | Memory | Speed | Use When |
|----------|--------|-------|----------|
| List comprehension | High | Fast | Result fits in memory |
| Generator expression | Low | Fast | Large datasets, streaming |
| In-place modification | Low | Medium | Memory constrained |
| Caching/Memoization | High | Very Fast | Repeated calls with same args |

## 🎯 Optimization Checklist

- [ ] Profiled code to find bottlenecks
- [ ] Used appropriate data structures (set/dict for O(1) lookups)
- [ ] Eliminated nested loops where possible
- [ ] Batch database/API calls
- [ ] Compile regex patterns outside loops
- [ ] Use list comprehensions/generators appropriately
- [ ] Cache expensive computations
- [ ] Avoid copying large data structures
- [ ] Use built-in functions (they're optimized)
- [ ] Measured performance improvement

## 🚫 What NOT to Do

1. Don't optimize without profiling first
2. Don't sacrifice code clarity for minor gains
3. Don't assume - measure actual performance
4. Don't optimize the wrong bottleneck
5. Don't forget to test after optimization

## 📖 Learn More

See [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md) for detailed explanations and examples.

---
**Remember**: "Premature optimization is the root of all evil" - Donald Knuth

Profile first, optimize the real bottlenecks, measure the results.
