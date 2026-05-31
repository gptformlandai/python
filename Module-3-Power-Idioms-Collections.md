# Module 3 - Power Idioms & Collections Module

## Purpose
This file is the single source of truth for Module 3.
We will keep all theory, examples, your doubts, answers, and progress here.

## Topics Covered in This Module
- Topic 12: Comprehensions vs Loops vs map/filter (45 min)
- Topic 13: Dict & Set Comprehensions (30 min)
- Topic 14: Unpacking (30 min)
- Topic 15: collections.Counter (30 min)
- Topic 16: collections.defaultdict (30 min)
- Topic 17: collections.deque (30 min)
- Topic 18: collections.namedtuple & dataclasses (30 min)
- Topic 19: Sorting Masterclass (45 min)

Estimated total: ~4 hours 30 min

---

## Learning Workflow for Each Topic
1. Concept in one line
2. Mental model
3. Memory behavior in CPython
4. Key behaviors and gotchas
5. Time complexity
6. Runnable examples
7. Common patterns
8. Pitfalls to avoid
9. Quick recap
10. Interview sound bite
11. Memory hook
12. Practice questions
13. Practice answers

---

## Topic Notes

### Topic 12: Comprehensions vs Loops vs map/filter
Status: Complete

#### Concept in One Line
Comprehensions, loops, and map/filter solve the same broad class of transformation problems, but they differ in readability, eagerness, and how well they express the shape of the work.

#### Mental Model
Think of these as three styles of moving data through a pipe.
- A comprehension is the compact, expressive shortcut when the rule is simple.
- A loop is the explicit step-by-step version when the logic needs space.
- map/filter are function-pipeline tools that shine when you already have a reusable function and want lazy iteration.

#### Memory Behavior in CPython
- List, dict, and set comprehensions build the result container immediately.
- A loop that appends into a list also materializes the whole result, but it does so step by step.
- In Python 3, map() and filter() return lazy iterators, so they do not build all output up front.
- If you wrap map() or filter() in list(), you materialize the whole result at once.
- Comprehensions often perform well because Python handles the append/build pattern internally in optimized bytecode.
- map() with a named function avoids inline boilerplate, but each item still goes through a function call.
- If you only need one pass over the transformed data, lazy iterators can reduce memory pressure.

#### Key Behaviors and Gotchas
- Prefer a comprehension when the transformation or filtering rule is simple and readable in one line.
- Prefer a loop when the logic has multiple steps, branching, logging, mutation, or error handling.
- map() and filter() are often strongest when a named function already exists.
- map(lambda ...) or filter(lambda ...) can be less readable than a comprehension for everyday Python code.
- Comprehensions are for building containers, not for side effects.
- In Python 3, comprehension loop variables do not leak into the outer scope.
- map() and filter() are one-pass iterators; once consumed, they are exhausted.
- A comprehension can combine transformation and filtering in one expression.

#### Time Complexity Notes
- Loop with append over n items: O(n)
- List comprehension over n items: O(n)
- Set or dict comprehension over n items: O(n)
- map() or filter() fully consumed over n items: O(n)
- Memory for list/set/dict comprehensions: O(n)
- Extra memory for map()/filter() iterator itself: O(1) until materialized

#### Examples
Example 1: Classic loop build

```python
nums = [1, 2, 3, 4, 5]
result = []

for num in nums:
    result.append(num * num)

print(result)  # [1, 4, 9, 16, 25]
```

What to notice:
- This is explicit and easy to extend.
- It is the best shape when more logic is coming.

Example 2: List comprehension version

```python
nums = [1, 2, 3, 4, 5]
squares = [num * num for num in nums]

print(squares)  # [1, 4, 9, 16, 25]
```

What to notice:
- Same result, less boilerplate.
- This is usually the most Pythonic form for simple transformation.

Example 3: Filter inside a comprehension

```python
nums = [1, 2, 3, 4, 5, 6]
even_squares = [num * num for num in nums if num % 2 == 0]

print(even_squares)  # [4, 16, 36]
```

What to notice:
- Filtering and transformation can live in one compact expression.
- This is a common sweet spot for comprehensions.

Example 4: map() with a named function

```python
def square(num):
    return num * num


nums = [1, 2, 3, 4, 5]
squares = list(map(square, nums))

print(squares)  # [1, 4, 9, 16, 25]
```

What to notice:
- map() reads well when the function already exists.
- Without list(), the result is a lazy iterator.

Example 5: filter() with a named predicate

```python
def is_even(num):
    return num % 2 == 0


nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(is_even, nums))

print(evens)  # [2, 4, 6]
```

What to notice:
- filter() is a natural fit when you already have a predicate function.
- For simple conditions, a comprehension is often easier to read.

Example 6: Lazy behavior of map()

```python
nums = [1, 2, 3]
mapped = map(lambda x: x * 10, nums)

print(mapped)         # map object
print(next(mapped))   # 10
print(list(mapped))   # [20, 30]
```

What to notice:
- map() does not compute everything immediately.
- Once consumed, the iterator moves forward and cannot be restarted.

Example 7: Benchmark loop vs comprehension vs map

```python
from timeit import timeit

nums = list(range(50_000))

def square(num):
    return num * num


loop_time = timeit(
    "result = []\nfor num in nums:\n    result.append(num * num)",
    globals=globals(),
    number=200,
)

comp_time = timeit(
    "[num * num for num in nums]",
    globals=globals(),
    number=200,
)

map_time = timeit(
    "list(map(square, nums))",
    globals=globals(),
    number=200,
)

print(f"loop: {loop_time:.6f}s")
print(f"comp: {comp_time:.6f}s")
print(f"map:  {map_time:.6f}s")
```

What to notice:
- All three are O(n), but constant factors differ.
- Comprehensions are often very competitive or fastest for simple expressions.

Example 8: Dict and set comprehension preview

```python
nums = [1, 2, 3, 4]

square_map = {num: num * num for num in nums}
even_set = {num for num in nums if num % 2 == 0}

print(square_map)  # {1: 1, 2: 4, 3: 9, 4: 16}
print(even_set)    # {2, 4}
```

What to notice:
- Comprehension syntax extends beyond lists.
- Topic 13 will go deeper on dict and set comprehensions specifically.

#### Common Patterns
- Use list comprehensions for simple transformation.
- Use comprehensions with an if-clause for simple filtering.
- Use explicit loops when the logic spans several steps or needs debugging visibility.
- Use map() when you already have a named reusable function.
- Use filter() when you already have a clean predicate function.
- Keep map()/filter() lazy when you want to stream values instead of materializing all of them.
- Use dict and set comprehensions when the target container itself matters.

#### Pitfalls to Avoid
- Forcing a dense comprehension when a normal loop would be clearer.
- Using comprehensions for side effects like printing or appending elsewhere.
- Reaching for map(lambda ...) or filter(lambda ...) when a comprehension is more readable.
- Forgetting that map() and filter() are iterators in Python 3.
- Consuming a map/filter iterator once and then expecting to reuse it.
- Assuming faster-looking syntax changes Big-O; most of these choices are still O(n).

#### Quick Recap
- Loops, comprehensions, and map/filter solve similar transformation problems.
- Comprehensions usually win for simple readable transform/filter tasks.
- Loops win when logic becomes multi-step or side-effect heavy.
- map()/filter() are lazy and work best with named functions or pipelines.
- Choose by clarity first, then use benchmarks when performance actually matters.

#### Interview Sound Bite
For Python transformation problems, I usually choose a comprehension for simple readable work, a loop for complex logic, and map/filter when I already have reusable functions and want lazy iteration.

#### Memory Hook
Comprehension = concise build. Loop = explicit control. map/filter = lazy pipeline.

#### Practice Questions
1. When is a list comprehension better than a loop?
2. When is a normal loop better than a comprehension?
3. Why can map() or filter() save memory in Python 3?
4. Why is map(lambda ...) often less readable than a comprehension?
5. Do comprehensions and loops usually have different Big-O for the same work?
6. What happens if you consume a map() iterator once and try to use it again?
7. Why are dict and set comprehensions a natural extension of list comprehensions?

#### Practice Answers
1. A list comprehension is better when the transformation or filtering rule is simple, readable, and directly produces a list.
2. A normal loop is better when the logic needs multiple statements, branching, logging, mutation, or easier debugging.
3. map() and filter() save memory because they return lazy iterators that produce values on demand instead of materializing the full output immediately.
4. map(lambda ...) is often less readable because the transformation logic gets split between the higher-order function and an inline lambda, while a comprehension keeps the rule visually local.
5. No. For equivalent full work over the same number of elements, comprehensions and loops are usually both O(n); the main difference is readability and constant factors.
6. Once a map() iterator is consumed, it is exhausted, so reusing it will produce no remaining values.
7. Dict and set comprehensions are a natural extension because they use the same concise iteration-and-filter style, but target different container types.

---

### Topic 13: Dict & Set Comprehensions
Status: In Progress

#### Concept in One Line
Dict and set comprehensions are concise ways to build mappings and unique-value collections in one readable pass, usually replacing small loops used for transform-and-filter work.

#### Mental Model
Think of them as list comprehensions with a different target container.
- A dict comprehension answers: for each item, what key and value should I store?
- A set comprehension answers: for each item, what unique normalized value should I keep?

#### Memory Behavior in CPython
- Dict comprehensions build a new dict eagerly.
- Set comprehensions build a new set eagerly.
- Unlike generator expressions, neither of them is lazy.
- Dict comprehensions insert key-value pairs into a hash table as they iterate.
- Set comprehensions insert produced values into a hash table and automatically collapse duplicates.
- If a dict comprehension produces the same key more than once, the last value wins.
- Since both target hash-based containers, produced keys or set elements must be hashable.

#### Key Behaviors and Gotchas
- Use a dict comprehension when the output is naturally key-value shaped.
- Use a set comprehension when you care about uniqueness.
- Dict comprehensions can transform, filter, or invert data in one pass.
- Set comprehensions are ideal for normalization tasks like lowercasing and deduplicating words.
- Repeated dict keys overwrite earlier values.
- Repeated set values vanish automatically.
- Complex nested comprehensions can become unreadable fast; clarity still wins.
- If order or duplicates matter in the final result, a set comprehension is the wrong tool.

#### Time Complexity Notes
- Dict comprehension over n items: O(n)
- Set comprehension over n items: O(n)
- Filtering during comprehension: still O(n)
- Hash insertion per produced item: average O(1)
- Extra memory for the built dict or set: O(n)

#### Examples
Example 1: Dict comprehension for simple transformation

```python
nums = [1, 2, 3, 4]
squares = {num: num * num for num in nums}

print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16}
```

What to notice:
- The left side of the colon is the key.
- The right side of the colon is the value.

Example 2: Dict comprehension with filtering

```python
scores = {"ana": 92, "bob": 85, "chris": 88, "dina": 95}
top_scores = {name: score for name, score in scores.items() if score >= 90}

print(top_scores)  # {'ana': 92, 'dina': 95}
```

What to notice:
- Filtering sits at the end of the comprehension.
- This avoids building the result with manual conditionals and assignment.

Example 3: Invert a dict with a comprehension

```python
codes = {"python": "py", "javascript": "js", "typescript": "ts"}
inverted = {short: name for name, short in codes.items()}

print(inverted)  # {'py': 'python', 'js': 'javascript', 'ts': 'typescript'}
```

What to notice:
- Swapping key and value is concise.
- This only works safely when original values are unique.

Example 4: Last key wins in dict comprehensions

```python
pairs = [("a", 1), ("b", 2), ("a", 99)]
data = {key: value for key, value in pairs}

print(data)  # {'a': 99, 'b': 2}
```

What to notice:
- Duplicate keys do not raise an error.
- The later assignment overwrites the earlier one.

Example 5: Normalize keys with a dict comprehension

```python
raw = {" Name ": "Aravind", " Role ": "Learner", " CITY ": "Hyderabad"}
normalized = {key.strip().lower(): value for key, value in raw.items()}

print(normalized)  # {'name': 'Aravind', 'role': 'Learner', 'city': 'Hyderabad'}
```

What to notice:
- Comprehensions are great for data cleanup.
- The original dict stays untouched.

Example 6: Set comprehension for even squares

```python
nums = [1, 2, 3, 4, 5, 6]
even_squares = {num * num for num in nums if num % 2 == 0}

print(even_squares)  # {4, 16, 36}
```

What to notice:
- Set comprehension uses braces without `key: value`.
- It behaves like a unique-value builder.

Example 7: Unique normalized words

```python
text = "Python python Data DATA structures Structures"
unique_words = {word.lower() for word in text.split()}

print(unique_words)  # {'python', 'data', 'structures'}
```

What to notice:
- Set comprehensions are ideal for deduplicate-and-normalize tasks.
- Repeated values collapse naturally.

Example 8: Build a lookup set from records

```python
users = [
    {"id": 1, "active": True},
    {"id": 2, "active": False},
    {"id": 3, "active": True},
]

active_ids = {user["id"] for user in users if user["active"]}
print(active_ids)  # {1, 3}
```

What to notice:
- This is a common real-world pattern.
- Set comprehensions are great when the final result is a membership structure.

Example 9: Dict comprehension vs generator expression

```python
nums = [1, 2, 3]
dict_comp = {num: num * num for num in nums}
gen_expr = ((num, num * num) for num in nums)

print(dict_comp)       # {1: 1, 2: 4, 3: 9}
print(dict(gen_expr))  # {1: 1, 2: 4, 3: 9}
```

What to notice:
- The dict comprehension builds immediately.
- The generator expression stays lazy until passed into `dict()`.

#### Common Patterns
- Use dict comprehensions for transform-and-filter work on mappings.
- Use dict comprehensions to invert one-to-one mappings.
- Use dict comprehensions to normalize keys or values.
- Use set comprehensions for deduplication plus normalization.
- Use set comprehensions to build fast membership structures.
- Reach for a normal loop when the comprehension starts getting too dense.

#### Pitfalls to Avoid
- Using a set comprehension when duplicates or ordering matter.
- Forgetting that dict key collisions overwrite earlier values.
- Building unreadable nested comprehensions just to stay concise.
- Producing unhashable dict keys or set elements.
- Assuming dict or set comprehensions are lazy like generator expressions.
- Using a comprehension when a named multi-step loop would communicate intent better.

#### Quick Recap
- Dict comprehensions build mappings; set comprehensions build unique-value collections.
- Both are eager, not lazy.
- Dict comprehensions are strong for transformation, filtering, inversion, and normalization.
- Set comprehensions are strong for uniqueness, cleanup, and membership prep.
- Choose them when they improve clarity, not just to make code shorter.

#### Interview Sound Bite
I use dict comprehensions when the output is naturally key-value shaped and set comprehensions when I need unique normalized values, but I switch back to a normal loop as soon as the expression stops being easy to read.

#### Memory Hook
Dict comprehension = map shape. Set comprehension = unique shape.

#### Practice Questions
1. What is the structural difference between a dict comprehension and a set comprehension?
2. What happens if a dict comprehension produces the same key twice?
3. Why is a set comprehension useful for word normalization tasks?
4. Why are dict and set comprehensions not considered lazy?
5. When should you prefer a normal loop over a comprehension?
6. Why can a set comprehension not store lists directly?
7. What is the difference between `{x for x in nums}` and `(x for x in nums)`?

#### Practice Answers
1. A dict comprehension produces `key: value` pairs, while a set comprehension produces a single value per iteration and stores only unique results.
2. If the same key is produced twice, the later value overwrites the earlier one.
3. A set comprehension is useful because it can transform words, such as lowercasing them, while automatically removing duplicates.
4. They are not lazy because they build the full dict or set immediately as the comprehension runs.
5. Prefer a normal loop when the logic needs multiple steps, clearer debugging, side handling, or would make the comprehension too dense to read comfortably.
6. A set comprehension cannot store lists directly because set elements must be hashable, and lists are mutable and unhashable.
7. `{x for x in nums}` is a set comprehension that builds a set immediately, while `(x for x in nums)` is a generator expression that yields values lazily.

---

### Topic 14: Unpacking
Status: Not Started

Notes: Pending.

---

### Topic 15: collections.Counter
Status: Not Started

Notes: Pending.

---

### Topic 16: collections.defaultdict
Status: Not Started

Notes: Pending.

---

### Topic 17: collections.deque
Status: Not Started

Notes: Pending.

---

### Topic 18: collections.namedtuple & dataclasses
Status: Not Started

Notes: Pending.

---

### Topic 19: Sorting Masterclass
Status: Not Started

Notes: Pending.

---

## Doubts and Q&A Log
Use this section whenever you ask a question during Module 3.

| # | Date | Topic | Your Doubt | Answer Summary | Action |
|---|------|-------|------------|----------------|--------|
| 1 | 2026-05-28 | - | - | - | - |

---

## Mistakes and Corrections
Track recurring mistakes so we can fix patterns quickly.

| # | Date | Mistake | Why It Happened | Correct Pattern |
|---|------|---------|-----------------|-----------------|
| 1 | 2026-05-28 | - | - | - |

---

## Module 3 Progress Tracker

- [ ] Topic 12 complete
- [ ] Topic 13 complete
- [ ] Topic 14 complete
- [ ] Topic 15 complete
- [ ] Topic 16 complete
- [ ] Topic 17 complete
- [ ] Topic 18 complete
- [ ] Topic 19 complete
- [ ] Module 3 revision complete

Current module status: In Progress