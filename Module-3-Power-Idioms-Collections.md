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

## Quick Navigation
- [Topic 12: Comprehensions vs Loops vs map/filter](#topic-12)
- [Topic 13: Dict & Set Comprehensions](#topic-13)
- [Topic 14: Unpacking](#topic-14)
- [Topic 15: collections.Counter](#topic-15)
- [Topic 16: collections.defaultdict](#topic-16)
- [Topic 17: collections.deque](#topic-17)
- [Topic 18: collections.namedtuple & dataclasses](#topic-18)
- [Topic 19: Sorting Masterclass](#topic-19)
- [Doubts and Q&A Log](#module-3-doubts)
- [Mistakes and Corrections](#module-3-mistakes)
- [Module 3 Progress Tracker](#module-3-progress)

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

<a id="topic-12"></a>
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

<a id="topic-13"></a>
### Topic 13: Dict & Set Comprehensions
Status: Complete

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

<a id="topic-14"></a>
### Topic 14: Unpacking
Status: Complete

#### Concept in One Line
Unpacking assigns items from an iterable or mapping directly into named variables, making extraction, argument passing, and reshaping cleaner than manual indexing.

#### Mental Model
Think of unpacking as opening a box and placing each item straight into labeled slots. Instead of saying "give me item 0, item 1, item 2," you describe the shape you expect and let Python distribute the contents for you.

#### Memory Behavior in CPython
- Basic unpacking binds names to existing object references; it does not deep-copy the values.
- Sequence unpacking itself is mostly about assignment, not duplication.
- Starred unpacking like `first, *middle, last = data` creates a new list object for the starred part.
- Nested unpacking follows the same rule recursively: names are rebound to the existing contained objects.
- In function calls, `*iterable` expands positional arguments and `**mapping` expands keyword arguments before the function receives them.
- Because unpacking usually just rebinds references, it is often lightweight unless a starred target or call expansion requires building intermediate argument structures.

#### Key Behaviors and Gotchas
- The number of target variables must match the number of values unless you use a starred target.
- A single starred target can absorb the remaining items.
- The starred target is always a list in assignment context, even if the source is a tuple or string.
- In assignment targets and function definitions, starred names usually collect remaining values.
- In function calls and literals, `*` and `**` usually expand values into the surrounding context.
- `_` is a common convention for values you intentionally ignore.
- Nested unpacking works only if the inner shape matches what you describe.
- `*args` collects extra positional arguments in function definitions.
- `**kwargs` collects extra keyword arguments in function definitions.
- `*iterable` and `**mapping` also work in function calls and literals, not just in assignment.

#### Time Complexity Notes
- Fixed-size unpacking of k items: O(k)
- Starred unpacking over n items: O(n), because Python must collect the starred portion
- Nested unpacking: proportional to the total number of unpacked elements
- Function call unpacking with `*args` / `**kwargs`: proportional to the number of expanded arguments
- The main cost is usually linear in the amount of data being unpacked, not constant

#### Examples
Example 1: Basic sequence unpacking

```python
point = (10, 20)
x, y = point

print(x, y)  # 10 20
```

What to notice:
- This is the simplest unpacking shape.
- It is clearer than `point[0]` and `point[1]` when the structure is fixed.

Example 2: Swap values without a temporary variable

```python
a = 5
b = 9

a, b = b, a
print(a, b)  # 9 5
```

What to notice:
- Python packs values on the right and unpacks on the left.
- This is one of the most common tuple-unpacking idioms.

Example 3: Ignore values you do not need

```python
record = (101, "Aravind", "Python", "active")
user_id, name, _, status = record

print(user_id, name, status)  # 101 Aravind active
```

What to notice:
- `_` signals intentionally ignored data.
- The shape still has to match.

Example 4: Starred unpacking for first, middle, last

```python
nums = [1, 2, 3, 4, 5, 6]
first, *middle, last = nums

print(first)   # 1
print(middle)  # [2, 3, 4, 5]
print(last)    # 6
```

What to notice:
- The starred target captures the remaining values.
- The starred result is a list.

Example 5: Nested unpacking

```python
data = ("ana", (92, 88))
name, (math_score, science_score) = data

print(name, math_score, science_score)  # ana 92 88
```

What to notice:
- The left-hand side describes the nested shape.
- Python expects the inner structure to match.

Example 6: Unpack a CSV-style row

```python
row = "101,Aravind,Python,active".split(",")
user_id, name, track, status = row

print(user_id, name, track, status)
```

What to notice:
- Unpacking is practical for tabular or fixed-format data.
- This is cleaner than indexing each position manually.

Example 7: Use `*` in a function call

```python
def add(a, b, c):
    return a + b + c


values = [10, 20, 30]
print(add(*values))  # 60
```

What to notice:
- `*values` expands the iterable into positional arguments.
- The function sees separate arguments, not a list.

Example 8: Use `**` in a function call

```python
def greet(name, role):
    return f"{name} is a {role}"


info = {"name": "Aravind", "role": "learner"}
print(greet(**info))  # Aravind is a learner
```

What to notice:
- `**info` expands dict keys as keyword arguments.
- The dict keys must match parameter names.

Example 9: `*args` and `**kwargs` in function definitions

```python
def show(*args, **kwargs):
    print(args)
    print(kwargs)


show(1, 2, 3, name="Aravind", topic="Python")
```

What to notice:
- `args` becomes a tuple of extra positional values.
- `kwargs` becomes a dict of extra keyword values.

Example 10: Merge iterables and mappings with unpacking

```python
nums1 = [1, 2]
nums2 = [3, 4]
merged_list = [*nums1, *nums2]

config1 = {"host": "localhost", "port": 8000}
config2 = {"debug": True}
merged_dict = {**config1, **config2}

print(merged_list)  # [1, 2, 3, 4]
print(merged_dict)  # {'host': 'localhost', 'port': 8000, 'debug': True}
```

What to notice:
- Unpacking also works inside list and dict literals.
- This is a clean composition pattern for small data structures.

Example 11: Left side usually collects, right side usually expands

```python
nums = [1, 2, 3, 4]

first, *rest = nums
copied = [*nums]

print(first)   # 1
print(rest)    # [2, 3, 4]
print(copied)  # [1, 2, 3, 4]
```

What to notice:
- On the left in assignment, `*rest` collects the remaining values.
- On the right in a list literal, `*nums` expands the iterable's items into the new list.
- So your rule is close, but the clearer rule is: left-side starred targets collect, right-side stars expand.

Example 12: Why `[*nums1, *nums2]` is not `[[1, 2], [3, 4]]`

```python
nums1 = [1, 2]
nums2 = [3, 4]

print([nums1, nums2])       # [[1, 2], [3, 4]]
print([*nums1, *nums2])     # [1, 2, 3, 4]
print([[*nums1], [*nums2]]) # [[1, 2], [3, 4]]
```

What to notice:
- `[nums1, nums2]` puts two list objects inside a new outer list.
- `*nums1` does not insert the list object itself; it inserts each element of that list into the surrounding literal.
- That is why `[*nums1, *nums2]` becomes one flat list with four items.
- If you want nested lists, do not star them at that level.

#### Common Patterns
- Use unpacking for fixed-shape records.
- Use starred unpacking when you need first/rest/last style extraction.
- Use nested unpacking when the input structure is predictable.
- Remember: starred targets collect on the left; starred expressions expand on the right.
- Use `*iterable` to pass positional values into a function.
- Use `**mapping` to pass keyword data into a function.
- Use `*args` and `**kwargs` in flexible function signatures.
- Use unpacking in literals for quick merges and reshaping.

#### Pitfalls to Avoid
- Unpacking the wrong number of items without a starred target.
- Assuming starred unpacking preserves the source container type.
- Using unpacking when the input shape is uncertain or inconsistent.
- Overusing `_` so much that the code hides important structure.
- Expanding `**mapping` with keys that do not match the function parameter names.
- Forgetting that nested unpacking will fail if the inner shape does not match.

#### Quick Recap
- Unpacking assigns iterable contents directly into variables.
- Starred unpacking absorbs the remaining items and produces a list.
- Nested unpacking works when the data shape matches your target pattern.
- `*` and `**` also work in function calls and literal merges.
- `[nums1, nums2]` nests lists, while `[*nums1, *nums2]` expands their contents into one list.
- Use unpacking when the structure is known and the code becomes clearer, not just shorter.

#### Interview Sound Bite
I use unpacking whenever the data has a predictable shape, because it makes extraction and function calls more readable than manual indexing, and starred unpacking gives me a clean way to capture the rest when the middle is flexible.

#### Memory Hook
Unpacking = describe the shape, let Python distribute.

#### Practice Questions
1. What is the difference between basic unpacking and starred unpacking?
2. Why does the starred target become a list?
3. When is unpacking better than manual indexing?
4. What is the difference between `*args` in a definition and `*values` in a call?
5. Why can nested unpacking fail even when the outer structure looks correct?
6. What does `**mapping` require to work in a function call?
7. What is the difference between `{**a, **b}` and `a | b` at a high level?
8. Why does `[nums1, nums2]` differ from `[*nums1, *nums2]`?

#### Practice Answers
1. Basic unpacking requires the number of variables to match the number of values exactly, while starred unpacking lets one target capture the remaining values.
2. The starred target becomes a list because Python materializes the variable-length remainder in a mutable sequence for assignment.
3. Unpacking is better when the structure is fixed and meaningful, because the variable names communicate intent more clearly than numeric indexes.
4. In a definition, `*args` collects extra positional arguments into a tuple. In a call, `*values` expands an iterable into separate positional arguments.
5. Nested unpacking can fail because Python expects the inner iterable shapes to match exactly what the left-hand pattern describes.
6. `**mapping` requires a mapping whose keys are strings matching the target function's parameter names.
7. Both merge mappings, but `{**a, **b}` uses unpacking syntax inside a dict literal, while `a | b` is the dedicated dict merge operator introduced later; both prefer right-hand values on conflicts.
8. `[nums1, nums2]` inserts two list objects into a new list, while `[*nums1, *nums2]` expands the elements of each list into the surrounding list literal, producing one flat list.

---

<a id="topic-15"></a>
### Topic 15: collections.Counter
Status: In Progress

#### Concept in One Line
`collections.Counter` is a dict-like tool built for counting hashable items, making frequency analysis much cleaner than manual tally code.

#### Mental Model
Think of `Counter` as a tally sheet that updates itself.
- Every unique item becomes a key.
- Every time the item appears, its count goes up.
- Instead of writing `if key in counts`, `Counter` handles the bookkeeping for you.

#### Memory Behavior in CPython
- `Counter` is a subclass of `dict`, so it stores keys in a hash table with associated count values.
- Keys are references to the original hashable objects; the items themselves are not copied deeply.
- Counts are usually integers, but `Counter` can technically store other numeric values too.
- Building a `Counter` from an iterable updates counts one item at a time.
- Accessing a missing key returns `0` instead of raising `KeyError`.
- Keys with zero or negative counts can still remain in the counter until you delete them or clean them up.
- Methods like `most_common()` materialize a result list, while `elements()` returns an iterator over repeated keys.

#### Key Behaviors and Gotchas
- Use `Counter(iterable)` to count items from a string, list, tuple, or any iterable.
- The outer container passed into `Counter(...)` does not need to be hashable; the individual produced items do.
- Use `Counter(mapping)` when you already have counts.
- Missing keys read as `0`, which is one of `Counter`'s biggest conveniences.
- `update()` adds counts; it does not replace them.
- `subtract()` subtracts counts and can produce zero or negative values.
- `update()` and `subtract()` mutate the existing counter in place.
- `+` and `-` create a new counter instead of mutating the existing one.
- `counter1 - counter2` drops zero and negative results, while `counter.subtract(...)` keeps them.
- A key with count `0` is not automatically removed.
- `counter["x"] == 0` does not mean `"x"` is stored as a key.
- `most_common(n)` is a quick way to get top frequencies.
- `elements()` repeats each key by its positive integer count and ignores zero or negative counts.
- `+counter` is a neat cleanup trick that removes zero and negative counts.
- `Counter` only works for hashable elements, just like dict keys and set elements.

#### Time Complexity Notes
- Building a counter from `n` items: O(n)
- Looking up one item's count: average O(1)
- Incrementing or decrementing one item's count: average O(1)
- `update()` or `subtract()` over `n` incoming items: O(n)
- `most_common()` over `m` unique keys: roughly O(m log m) for a full ranking
- Extra memory: O(m), where `m` is the number of unique items

#### Examples
Example 1: Count characters in a string

```python
from collections import Counter

text = "banana"
counts = Counter(text)

print(counts)       # Counter({'a': 3, 'n': 2, 'b': 1})
print(counts["a"])  # 3
```

What to notice:
- Each unique character becomes a key.
- The count tells you how often that character appeared.

Example 2: Count words in a list

```python
from collections import Counter

words = ["python", "data", "python", "lists", "data", "python"]
word_counts = Counter(words)

print(word_counts)           # Counter({'python': 3, 'data': 2, 'lists': 1})
print(word_counts["python"]) # 3
print(word_counts["dict"])   # 0
```

What to notice:
- Missing keys return `0` instead of raising an error.
- This removes a lot of manual counting boilerplate.
- The list itself is just the iterable container.
- The counted items are the strings inside the list, and strings are hashable.

Example 3: Compare manual counting vs `Counter`

```python
nums = [1, 2, 2, 3, 3, 3]

manual = {}
for num in nums:
    manual[num] = manual.get(num, 0) + 1

from collections import Counter
counter_version = Counter(nums)

print(manual)          # {1: 1, 2: 2, 3: 3}
print(counter_version) # Counter({3: 3, 2: 2, 1: 1})
```

What to notice:
- `Counter` expresses the intent directly.
- It is essentially the standard-library version of a manual frequency dict pattern.

Example 4: Get the most common items

```python
from collections import Counter

votes = ["A", "B", "A", "C", "A", "B", "B", "A"]
vote_counts = Counter(votes)

print(vote_counts.most_common(2))  # [('A', 4), ('B', 3)]
```

What to notice:
- `most_common(n)` is perfect for top-k frequency tasks.
- The result is a list of `(item, count)` tuples.

Example 5: Update counts incrementally

```python
from collections import Counter

counts = Counter()
counts.update(["python", "python", "sql"])
counts.update(["sql", "ml"])

print(counts)  # Counter({'python': 2, 'sql': 2, 'ml': 1})
```

What to notice:
- `update()` adds to existing counts.
- This is useful for streaming or batch-by-batch tallying.

Example 6: Subtract counts and keep track of shortages

```python
from collections import Counter

inventory = Counter({"pen": 10, "notebook": 5})
sold = Counter({"pen": 4, "notebook": 7})

inventory.subtract(sold)
print(inventory)  # Counter({'pen': 6, 'notebook': -2})
```

What to notice:
- `subtract()` can create negative counts.
- Negative values can be useful when you want to represent shortages or deficits.

Example 7: Why `subtract()` is not the same as `-`

```python
from collections import Counter

inventory = Counter({"pen": 10, "notebook": 5})
sold = Counter({"pen": 4, "notebook": 7})

print(inventory - sold)  # Counter({'pen': 6})

inventory.subtract(sold)
print(inventory)         # Counter({'pen': 6, 'notebook': -2})
```

What to notice:
- `inventory - sold` creates a new counter.
- The `-` operator removes zero and negative results.
- `subtract()` mutates the existing counter and preserves negative counts.

Example 8: Multiset-style operations

```python
from collections import Counter

basket1 = Counter(["apple", "apple", "banana", "orange"])
basket2 = Counter(["apple", "banana", "banana", "grape"])

print(basket1 + basket2)  # Counter({'apple': 3, 'banana': 3, 'orange': 1, 'grape': 1})
print(basket1 - basket2)  # Counter({'apple': 1, 'orange': 1})
print(basket1 & basket2)  # Counter({'apple': 1, 'banana': 1})
print(basket1 | basket2)  # Counter({'apple': 2, 'banana': 2, 'orange': 1, 'grape': 1})
```

What to notice:
- `+` adds counts.
- `-` keeps only positive results.
- `&` keeps minimum shared counts.
- `|` keeps maximum counts.

Example 9: Why `update()` is not the same as `+`

```python
from collections import Counter

counts = Counter({"python": 2})
incoming = ["python", "sql"]

new_counts = counts + Counter(incoming)
print(counts)      # Counter({'python': 2})
print(new_counts)  # Counter({'python': 3, 'sql': 1})

counts.update(incoming)
print(counts)      # Counter({'python': 3, 'sql': 1})
```

What to notice:
- `+` returns a new counter and usually expects another counter-like operand.
- `update()` mutates the original counter.
- `update()` is convenient when fresh data arrives as an iterable and you want to keep accumulating.

Example 10: Expand back into repeated elements

```python
from collections import Counter

counts = Counter({"a": 3, "b": 1, "c": 0})

print(list(counts.elements()))  # ['a', 'a', 'a', 'b']
```

What to notice:
- `elements()` expands the multiset back into repeated items.
- Zero and negative counts are ignored.

Example 11: Clean out zero and negative counts

```python
from collections import Counter

counts = Counter({"a": 3, "b": 0, "c": -2})
cleaned = +counts

print(counts)   # Counter({'a': 3, 'b': 0, 'c': -2})
print(cleaned)  # Counter({'a': 3})
```

What to notice:
- `+counter` is a compact cleanup idiom.
- It keeps only keys with positive counts.

Example 12: Check if two strings are anagrams

```python
from collections import Counter

word1 = "listen"
word2 = "silent"

print(Counter(word1) == Counter(word2))  # True
```

What to notice:
- `Counter` is excellent for comparing frequency profiles.
- This is a common interview and practice problem pattern.

#### Production-Style Counter Examples
Example 13: Count API status codes from application logs

```python
from collections import Counter

status_codes = [200, 200, 201, 404, 500, 200, 404, 503, 500, 200]
status_counter = Counter(status_codes)

print(status_counter)
print(status_counter.most_common())
```

What to notice:
- This is a direct fit for observability summaries.
- You can quickly answer questions like "how many 5xx responses happened?"
- `most_common()` gives you an immediate incident snapshot.

Example 14: Aggregate events batch by batch from a stream

```python
from collections import Counter

running_counts = Counter()

batches = [
    ["login", "search", "search", "checkout"],
    ["login", "login", "search"],
    ["checkout", "search", "payment_failed"],
]

for batch in batches:
    running_counts.update(batch)

print(running_counts)
```

What to notice:
- This models event ingestion in chunks.
- `update()` is a natural fit when your process keeps a rolling in-memory tally.
- This is one reason `update()` exists separately from `+`.

Example 15: Top endpoints from access logs

```python
from collections import Counter

endpoints = [
    "/health",
    "/login",
    "/login",
    "/products",
    "/products",
    "/products",
    "/cart",
    "/login",
]

endpoint_counter = Counter(endpoints)

for endpoint, hits in endpoint_counter.most_common(3):
    print(endpoint, hits)
```

What to notice:
- This is a standard top-k reporting use case.
- `Counter` is excellent when you want the hottest keys quickly.
- Common production pattern: top endpoints, top search terms, top error types, top users by events.

Example 16: Detect inventory shortages by subtracting demand from stock

```python
from collections import Counter

stock = Counter({"pen": 100, "notebook": 40, "marker": 20})
demand = Counter({"pen": 85, "notebook": 50, "marker": 10})

remaining = stock.copy()
remaining.subtract(demand)

shortages = {item: -count for item, count in remaining.items() if count < 0}

print(remaining)   # Counter({'pen': 15, 'marker': 10, 'notebook': -10})
print(shortages)   # {'notebook': 10}
```

What to notice:
- `subtract()` is useful when negative numbers are meaningful.
- This is closer to operations and supply-chain logic than plain multiset math.
- If you had used `stock - demand`, the shortage signal would disappear.

Example 17: Compare yesterday vs today error distribution

```python
from collections import Counter

yesterday = Counter(["timeout", "timeout", "db_error", "auth_error"])
today = Counter(["timeout", "db_error", "db_error", "db_error", "auth_error"])

delta = today.copy()
delta.subtract(yesterday)

print(delta)  # Counter({'db_error': 2, 'timeout': -1, 'auth_error': 0})
```

What to notice:
- Positive counts mean an error type increased.
- Negative counts mean it decreased.
- This is a simple but useful diagnostic comparison pattern.

Example 18: Build a word-frequency feature from text data

```python
from collections import Counter

documents = [
    "python data pipelines",
    "python data structures",
    "data pipelines in production",
]

token_counter = Counter()

for doc in documents:
    tokens = doc.lower().split()
    token_counter.update(tokens)

print(token_counter)
print(token_counter.most_common(5))
```

What to notice:
- This is a common preprocessing step in analytics and ML pipelines.
- `Counter` works well for local bag-of-words style frequency features.
- In production, tokenization may be more advanced, but the counting pattern is still the same.

Example 19: Reconcile two services' category tallies

```python
from collections import Counter

service_a = Counter({"success": 1200, "failed": 43, "retry": 21})
service_b = Counter({"success": 1188, "failed": 52, "retry": 21})

drift = service_a.copy()
drift.subtract(service_b)

print(drift)  # Counter({'success': 12, 'failed': -9, 'retry': 0})
```

What to notice:
- This is useful when reconciling two sources that should mostly agree.
- Non-zero values immediately show drift.
- The sign tells you which side is higher.

Example 20: Remove noisy low-frequency keys before reporting

```python
from collections import Counter

search_terms = Counter({
    "python": 120,
    "sql": 95,
    "pandas": 44,
    "pyhton": 2,
    "sqll": 1,
})

filtered = Counter({term: count for term, count in search_terms.items() if count >= 5})

print(filtered)  # Counter({'python': 120, 'sql': 95, 'pandas': 44})
```

What to notice:
- This is useful for cleanup before dashboards or downstream rules.
- `Counter` pairs nicely with dict comprehensions when you need to prune noise.

#### When Counter Fits Production Well
- Local in-memory counting of events, tokens, endpoints, categories, or statuses.
- Batch or stream consumers that need rolling tallies.
- Top-k summaries and quick frequency dashboards.
- Inventory, reconciliation, and drift-analysis use cases where count differences matter.
- Pre-aggregation before writing results to a database, cache, or metrics system.

#### When Counter Alone Is Not Enough
- When counts must be shared across processes or machines.
- When updates must be durable across restarts.
- When concurrent writers need a strongly consistent source of truth.
- When event volume is too high for a single-process in-memory structure.
- In those cases, `Counter` is still useful as a local aggregation layer, but the system of record usually needs Redis, a database, Kafka consumers, or a metrics backend.

#### Common Patterns
- Use `Counter` for word frequency, character frequency, and event tallies.
- Use `most_common()` for leaderboards and top-k questions.
- Use `update()` when data arrives in chunks.
- Use `subtract()` when comparing demand vs supply or sold vs available.
- Use `update()` and `subtract()` when you want to mutate one running counter over time.
- Use `+` and `-` when you want a derived result and want to leave the original counters untouched.
- Use `Counter(a) == Counter(b)` for anagram-style frequency comparison.
- Use `&` and `|` when you want multiset intersection and union behavior.
- Use `+counter` to clean up non-positive counts before final output.

#### Pitfalls to Avoid
- Assuming `Counter` works with unhashable items like lists.
- Confusing an unhashable outer iterable container with the hashability requirement for each counted element.
- Forgetting that missing keys return `0`, which is different from normal dict access.
- Thinking a zero count means the key must exist in the underlying mapping.
- Assuming `subtract()` removes keys automatically when counts reach zero.
- Assuming `update()` and `subtract()` are interchangeable with `+` and `-`.
- Forgetting that `most_common()` materializes a ranked list.
- Using `Counter` when a simple running integer or boolean flag would be enough.

#### Quick Recap
- `Counter` is a dict-like frequency tool for hashable items.
- The counted elements must be hashable, but the iterable container you pass in does not.
- Missing keys return `0`, which simplifies counting code.
- `update()` adds counts; `subtract()` can create zero or negative counts.
- `update()` and `subtract()` mutate in place, while `+` and `-` return new counters.
- `counter1 - counter2` drops non-positive results, but `subtract()` keeps them.
- `most_common()` gives ranked frequency results.
- `Counter` also supports multiset-style arithmetic like `+`, `-`, `&`, and `|`.
- Zero and negative counts may stick around until you clean them up.

#### Interview Sound Bite
When I need frequency analysis in Python, I reach for `collections.Counter` because it removes manual tally boilerplate, gives me clean top-k queries through `most_common()`, and supports multiset-style operations for comparing inventories or counts.

#### Memory Hook
`Counter` = a dict that counts for you.

#### Practice Questions
1. Why is `Counter` often better than a normal dict for frequency problems?
2. What does `counter["missing"]` return for a missing key?
3. What is the difference between `update()` and `subtract()`?
4. Why can a `Counter` show zero or negative counts?
5. What does `most_common(3)` return?
6. What is the difference between `Counter(a) == Counter(b)` and `sorted(a) == sorted(b)` for anagram-style checks?
7. Why does `elements()` ignore zero and negative counts?
8. What does `+counter` do?
9. Why can `Counter(["a", "b", "a"])` work even though a list is unhashable?
10. Why are `subtract()` and `-` not the same thing?

#### Practice Answers
1. `Counter` is better because it is built specifically for tallying, returns `0` for missing keys, and includes useful tools like `most_common()`, `update()`, and multiset operations.
2. It returns `0` instead of raising `KeyError`.
3. `update()` adds incoming counts to the existing counter, while `subtract()` subtracts them and can create zero or negative results.
4. A `Counter` can show zero or negative counts because subtraction and manual assignments do not automatically remove keys when the count stops being positive.
5. It returns a list of the three most common `(item, count)` pairs.
6. `Counter(a) == Counter(b)` compares frequency directly and is usually the clearer fit for anagram logic, while `sorted(a) == sorted(b)` compares fully sorted sequences and often does more work than needed.
7. `elements()` represents the counter as repeated existing items, so only positive counts make sense to expand into actual repeated values.
8. `+counter` returns a cleaned counter containing only keys with positive counts.
9. It works because the list is only the iterable container being looped over; the actual counted elements are the strings inside it, and those strings are hashable.
10. `subtract()` mutates an existing counter and preserves zero or negative results, while `counter1 - counter2` creates a new counter and drops non-positive counts.

---

<a id="topic-16"></a>
### Topic 16: collections.defaultdict
Status: Complete

#### Concept in One Line
`collections.defaultdict` is a dict that automatically creates a default value for a missing key, removing a lot of manual "if key not in dict" code.

#### Mental Model
Think of `defaultdict` as a warehouse with automatic empty bins.
- The first time you ask for a missing bin, Python creates it for you.
- What gets created depends on the factory you choose.
- `list` gives an empty list, `set` gives an empty set, `int` gives `0`, and so on.

#### Memory Behavior in CPython
- `defaultdict` is a subclass of `dict`, so it stores keys in the same hash-table style structure as a normal dict.
- It has one extra piece of state: `default_factory`, which is a callable used to create missing values.
- When you access a missing key with bracket syntax like `d[key]`, Python calls the factory, stores the produced value under that key, and returns it.
- The produced default object becomes part of the dictionary from that moment onward.
- The factory is only used for missing-key access through `__getitem__` style lookups, not for every dict method.
- If the factory creates mutable objects like lists or sets, each missing key gets its own fresh container.

#### Key Behaviors and Gotchas
- `defaultdict(list)` is excellent for grouping values.
- `defaultdict(set)` is useful when you need grouping plus uniqueness.
- `defaultdict(int)` is a simple counting pattern because `int()` returns `0`.
- Accessing a missing key with `d[key]` creates and stores that key automatically.
- `.get(key)` does not trigger the factory.
- `key in d` does not trigger the factory.
- Iterating the dict does not trigger the factory.
- This means bracket access can mutate the dictionary even when you only meant to read.
- A normal dict plus `setdefault()` can solve some of the same problems, but `defaultdict` is usually cleaner when default creation is central to the pattern.
- If you later serialize or print deeply nested `defaultdict`s, you may want to convert them back to normal dicts for cleaner output.

#### Time Complexity Notes
- Lookup by key: average O(1)
- Insert/update by key: average O(1)
- Accessing a missing key with auto-creation: average O(1), plus the factory call cost
- Grouping or counting over `n` records: O(n)
- Extra memory: O(m), where `m` is the number of created keys and stored values

#### Examples
Example 1: Group words by first letter

```python
from collections import defaultdict

words = ["apple", "ant", "banana", "ball", "cat"]
grouped = defaultdict(list)

for word in words:
    grouped[word[0]].append(word)

print(grouped)
print(dict(grouped))
```

What to notice:
- Each missing key starts with an empty list.
- This removes the need for manual initialization.

Example 2: Normal dict version vs `defaultdict`

```python
words = ["apple", "ant", "banana", "ball", "cat"]

manual = {}
for word in words:
    first = word[0]
    manual.setdefault(first, []).append(word)

from collections import defaultdict
cleaner = defaultdict(list)
for word in words:
    cleaner[word[0]].append(word)

print(manual)
print(dict(cleaner))
```

What to notice:
- Both work.
- `defaultdict` is usually easier to read when default creation is the main idea.

Example 3: Count items with `defaultdict(int)`

```python
from collections import defaultdict

votes = ["A", "B", "A", "C", "A", "B"]
counts = defaultdict(int)

for vote in votes:
    counts[vote] += 1

print(dict(counts))  # {'A': 3, 'B': 2, 'C': 1}
```

What to notice:
- `int()` produces `0`, so missing keys start at zero.
- This is a lightweight counting pattern.

Example 4: Why `Counter` is still the better counting specialist

```python
from collections import Counter, defaultdict

votes = ["A", "B", "A", "C", "A", "B"]

counter_counts = Counter(votes)

default_counts = defaultdict(int)
for vote in votes:
    default_counts[vote] += 1

print(counter_counts)       # Counter({'A': 3, 'B': 2, 'C': 1})
print(dict(default_counts)) # {'A': 3, 'B': 2, 'C': 1}
```

What to notice:
- `defaultdict(int)` can count well.
- `Counter` is still more specialized when you want things like `most_common()` or multiset operations.

Example 5: Group unique users per endpoint

```python
from collections import defaultdict

events = [
    ("/login", "u1"),
    ("/login", "u2"),
    ("/login", "u1"),
    ("/cart", "u1"),
]

users_by_endpoint = defaultdict(set)

for endpoint, user_id in events:
    users_by_endpoint[endpoint].add(user_id)

print({key: sorted(value) for key, value in users_by_endpoint.items()})
```

What to notice:
- `set` is the right factory when duplicates should collapse.
- This is useful for uniqueness-per-group problems.

Example 6: Bucket records by status

```python
from collections import defaultdict

orders = [
    {"id": 1, "status": "paid"},
    {"id": 2, "status": "pending"},
    {"id": 3, "status": "paid"},
]

orders_by_status = defaultdict(list)

for order in orders:
    orders_by_status[order["status"]].append(order["id"])

print(dict(orders_by_status))  # {'paid': [1, 3], 'pending': [2]}
```

What to notice:
- This is a classic grouping/bucketing pattern.
- `defaultdict(list)` is often the cleanest shape for it.

Example 7: Build an adjacency list for a graph

```python
from collections import defaultdict

edges = [("A", "B"), ("A", "C"), ("B", "D")]
graph = defaultdict(list)

for source, target in edges:
    graph[source].append(target)

print(dict(graph))  # {'A': ['B', 'C'], 'B': ['D']}
```

What to notice:
- Graphs and dependency maps often use this pattern.
- Without `defaultdict`, adjacency-list code gets noisier.

Example 8: Nested `defaultdict`

```python
from collections import defaultdict

sales = [
    ("north", "laptop", 3),
    ("north", "mouse", 5),
    ("south", "laptop", 2),
]

summary = defaultdict(lambda: defaultdict(int))

for region, item, qty in sales:
    summary[region][item] += qty

print({region: dict(items) for region, items in summary.items()})
```

What to notice:
- Nested factories let you build multi-level structures naturally.
- This is powerful, but nested `defaultdict`s can become harder to debug if overused.

Example 9: The `.get()` surprise

```python
from collections import defaultdict

data = defaultdict(list)

print(data.get("missing"))  # None
print(dict(data))            # {}

print(data["missing"])      # []
print(dict(data))            # {'missing': []}
```

What to notice:
- `.get()` does not trigger the factory.
- Bracket access does trigger the factory and mutates the dict.

Example 10: Accidental key creation while reading

```python
from collections import defaultdict

counts = defaultdict(int, {"ok": 3})

if counts["missing"] == 0:
    print("not present yet")

print(dict(counts))  # {'ok': 3, 'missing': 0}
```

What to notice:
- A read with bracket syntax created a new key.
- This is one of the biggest practical gotchas with `defaultdict`.

Example 11: Custom factory

```python
from collections import defaultdict

def unknown_user():
    return "anonymous"


owners = defaultdict(unknown_user)
owners["session_1"] = "Aravind"

print(owners["session_1"])  # Aravind
print(owners["session_2"])  # anonymous
```

What to notice:
- The factory can be any callable.
- It does not have to be `list`, `set`, or `int`.

Example 12: Convert to a normal dict for cleaner output

```python
from collections import defaultdict

grouped = defaultdict(list)
grouped["python"].append("lists")
grouped["python"].append("dicts")

plain = dict(grouped)

print(grouped)  # defaultdict(<class 'list'>, {'python': ['lists', 'dicts']})
print(plain)    # {'python': ['lists', 'dicts']}
```

What to notice:
- `defaultdict` prints its factory too.
- Converting to a plain dict is often nicer for logs, APIs, or docs.

#### Production-Style defaultdict Examples
Example 13: Group log lines by severity

```python
from collections import defaultdict

logs = [
    ("INFO", "service started"),
    ("ERROR", "db timeout"),
    ("INFO", "healthcheck ok"),
    ("ERROR", "payment failed"),
]

messages_by_level = defaultdict(list)

for level, message in logs:
    messages_by_level[level].append(message)

print(dict(messages_by_level))
```

What to notice:
- This is useful for local log summarization or alert preparation.
- Grouping is where `defaultdict` shines most.

Example 14: Build an inverted index

```python
from collections import defaultdict

documents = {
    1: "python data structures",
    2: "python production systems",
    3: "data pipelines",
}

index = defaultdict(set)

for doc_id, text in documents.items():
    for token in text.split():
        index[token].add(doc_id)

print({term: sorted(doc_ids) for term, doc_ids in index.items()})
```

What to notice:
- This is a classic search/indexing pattern.
- `set` avoids duplicate document IDs.

Example 15: Group metrics by tenant

```python
from collections import defaultdict

events = [
    ("tenant_a", 120),
    ("tenant_b", 90),
    ("tenant_a", 80),
]

latencies = defaultdict(list)

for tenant, latency_ms in events:
    latencies[tenant].append(latency_ms)

averages = {
    tenant: sum(values) / len(values)
    for tenant, values in latencies.items()
}

print(averages)  # {'tenant_a': 100.0, 'tenant_b': 90.0}
```

What to notice:
- `defaultdict` often acts as the grouping step before later aggregation.
- This is a common local pre-processing pattern in services and jobs.

#### Common Patterns
- Use `defaultdict(list)` for grouping or bucketing.
- Use `defaultdict(set)` when each group should contain unique values.
- Use `defaultdict(int)` for simple counts when `Counter` would be overkill.
- Use nested `defaultdict`s for multi-level accumulation.
- Use `defaultdict` to build adjacency lists, inverted indexes, and grouped summaries.
- Convert to a normal dict when you want cleaner serialization or logging.

#### Pitfalls to Avoid
- Accidentally creating keys just by reading with bracket access.
- Forgetting that `.get()` does not use the default factory.
- Using `defaultdict` when a normal dict is clearer because missing keys should be treated as errors.
- Building deeply nested `defaultdict`s that become hard to inspect or serialize.
- Choosing `defaultdict(int)` for complex counting cases where `Counter` is more expressive.
- Assuming the factory runs for every access; it only runs when a missing key is accessed with bracket syntax.

#### Quick Recap
- `defaultdict` auto-creates missing values using a factory.
- `list`, `set`, and `int` are the most common factories.
- `d[key]` on a missing key creates and stores a default value.
- `.get(key)` does not create anything.
- `defaultdict` is strongest for grouping, bucketing, adjacency lists, and nested accumulation.
- Use it when automatic initialization helps; avoid it when silent key creation would hide bugs.

#### Interview Sound Bite
I reach for `defaultdict` when the core pattern is grouping or accumulating into missing keys, because it removes repetitive initialization code and keeps the main logic focused on the actual update, but I stay careful with bracket reads since they can create keys implicitly.

#### Memory Hook
`defaultdict` = dict with auto-created first value.

#### Practice Questions
1. What problem does `defaultdict` solve better than a normal dict?
2. What is `default_factory`?
3. What is the difference between `d[key]` and `d.get(key)` for a missing key in a `defaultdict`?
4. When would `defaultdict(list)` be better than `defaultdict(set)`?
5. When is `Counter` a better choice than `defaultdict(int)`?
6. Why can `defaultdict` accidentally change the dictionary during a read?
7. Why might you convert a `defaultdict` to a normal dict before output?
8. What is a good real-world use case for nested `defaultdict`s?

#### Practice Answers
1. It solves repetitive missing-key initialization by automatically creating a default value the first time a missing key is accessed with bracket syntax.
2. `default_factory` is the callable used to build the default value for a missing key.
3. `d[key]` triggers the factory, stores the new value, and returns it, while `d.get(key)` simply returns `None` by default and does not create a key.
4. `defaultdict(list)` is better when duplicates and insertion order inside each group matter, while `defaultdict(set)` is better when each group should contain unique values only.
5. `Counter` is better when the main problem is counting frequency and you want features like `most_common()` or multiset-style operations.
6. It can change the dictionary because bracket access on a missing key automatically creates and inserts the factory-produced value.
7. Converting to a normal dict often gives cleaner output for logs, APIs, JSON conversion, or debugging displays.
8. A good use case is multi-level aggregation, such as region-to-product sales totals or tenant-to-endpoint counters.

---

<a id="topic-17"></a>
### Topic 17: collections.deque
Status: Complete

#### Concept in One Line
`collections.deque` is a double-ended queue optimized for fast append and pop operations from both ends.

#### Mental Model
Think of a deque as a train where you can attach or remove coaches from the front or the back efficiently.
- A list is great when you mostly work at the right end.
- A deque is better when the left end matters too.
- The moment you need queue behavior with frequent front removals, `deque` becomes the right mental model.

#### Memory Behavior in CPython
- A deque is not a single contiguous dynamic array like a list.
- In CPython, it is implemented as a linked sequence of fixed-size blocks, which is why appending and popping from both ends stays efficient.
- Because it is block-based rather than fully contiguous, random access in the middle is slower than with a list.
- Appending or popping at either end usually only touches one block edge, so those operations are cheap.
- A bounded deque created with `maxlen` automatically discards items from the opposite side when full.
- A deque holds references to objects just like lists and dicts; it does not deep-copy stored items.

#### Key Behaviors and Gotchas
- `append()` and `pop()` work on the right side.
- `appendleft()` and `popleft()` work on the left side.
- `popleft()` is the big reason deque is better than list for queues.
- `deque(maxlen=n)` creates a fixed-length rolling buffer.
- When a bounded deque is full, appending to one side drops an item from the other side automatically.
- `rotate(k)` shifts items right for positive `k` and left for negative `k`.
- `extendleft(iterable)` adds items one by one to the left, so the iterable's order appears reversed in the final deque.
- Indexing near the ends is fine, but frequent middle access is not what deque is built for.
- Deques do not support slicing like lists do.
- If your workload is mostly random indexing and in-place middle updates, a list is usually the better fit.

#### Time Complexity Notes
- `append()` / `appendleft()`: O(1)
- `pop()` / `popleft()`: O(1)
- Access by index near either end: effectively fast, but general indexed access is O(n)
- Insert/remove in the middle: O(n)
- `rotate(k)`: proportional to the effective rotation work
- Queue processing over `n` items with repeated `popleft()`: O(n)
- List queue pattern with repeated `pop(0)`: O(n^2) over many removals

#### Examples
Example 1: Basic deque operations

```python
from collections import deque

items = deque([1, 2, 3])

items.append(4)
items.appendleft(0)

print(items)          # deque([0, 1, 2, 3, 4])
print(items.pop())    # 4
print(items.popleft())# 0
print(items)          # deque([1, 2, 3])
```

What to notice:
- A deque works naturally from both ends.
- This is the core behavior to remember.

Example 2: Why deque is better than list for queue behavior

```python
from collections import deque

queue = deque(["a", "b", "c"])
print(queue.popleft())  # a
print(queue.popleft())  # b

items = ["a", "b", "c"]
print(items.pop(0))     # a
```

What to notice:
- Both remove from the front.
- The deque version is designed for this pattern; the list version shifts remaining elements each time.

Example 3: Use deque as a stack too

```python
from collections import deque

stack = deque()
stack.append("first")
stack.append("second")

print(stack.pop())  # second
print(stack.pop())  # first
```

What to notice:
- Deque can act as both queue and stack.
- A list is also fine for stack behavior, so deque is mainly compelling when both ends matter.

Example 4: Fixed-size rolling history with `maxlen`

```python
from collections import deque

history = deque(maxlen=3)

for value in [10, 20, 30, 40, 50]:
    history.append(value)
    print(history)
```

What to notice:
- Once full, the deque keeps only the most recent items.
- This is a common rolling-window pattern.

Example 5: Rotate items

```python
from collections import deque

dq = deque([1, 2, 3, 4])

dq.rotate(1)
print(dq)  # deque([4, 1, 2, 3])

dq.rotate(-2)
print(dq)  # deque([2, 3, 4, 1])
```

What to notice:
- Positive rotation moves items from right to left.
- Negative rotation moves items from left to right.

Example 6: `extendleft()` reverses incoming order

```python
from collections import deque

dq = deque([3, 4])
dq.extendleft([1, 2])

print(dq)  # deque([2, 1, 3, 4])
```

What to notice:
- `extendleft()` inserts one item at a time on the left.
- That means the iterable appears reversed in the final deque.

Example 7: Breadth-first search queue

```python
from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E"],
    "D": [],
    "E": [],
}

queue = deque(["A"])
seen = {"A"}
order = []

while queue:
    node = queue.popleft()
    order.append(node)

    for neighbor in graph[node]:
        if neighbor not in seen:
            seen.add(neighbor)
            queue.append(neighbor)

print(order)  # ['A', 'B', 'C', 'D', 'E']
```

What to notice:
- BFS is one of the canonical deque use cases.
- `popleft()` keeps the queue efficient.

Example 8: Sliding window sum

```python
from collections import deque

window = deque(maxlen=3)
nums = [5, 7, 2, 8, 1]

for num in nums:
    window.append(num)
    print(list(window), sum(window))
```

What to notice:
- `maxlen` makes rolling windows simple.
- This pattern is common before building more advanced window logic.

Example 9: Recent log buffer

```python
from collections import deque

recent_logs = deque(maxlen=4)

for line in [
    "INFO start",
    "INFO ready",
    "WARN slow query",
    "ERROR timeout",
    "INFO retrying",
]:
    recent_logs.append(line)

print(list(recent_logs))
```

What to notice:
- This keeps only the newest log lines in memory.
- Very useful for debug snapshots and tail-style views.

Example 10: Undo/redo style buffer

```python
from collections import deque

undo_stack = deque()
redo_stack = deque()

for action in ["type A", "type B", "delete B"]:
    undo_stack.append(action)

last_action = undo_stack.pop()
redo_stack.append(last_action)

print(list(undo_stack))  # ['type A', 'type B']
print(list(redo_stack))  # ['delete B']
```

What to notice:
- Deque is a natural buffer for reversible operations.
- Both ends can matter depending on the workflow.

Example 11: Simple round-robin worker rotation

```python
from collections import deque

workers = deque(["w1", "w2", "w3"])

for task in ["t1", "t2", "t3", "t4"]:
    worker = workers[0]
    print(task, "->", worker)
    workers.rotate(-1)
```

What to notice:
- `rotate()` is useful when the active front item should cycle.
- This pattern shows up in round-robin scheduling and fair dispatching.

#### Production-Style deque Examples
Example 12: Keep a bounded request history per service instance

```python
from collections import deque

recent_requests = deque(maxlen=5)

for request_id in [101, 102, 103, 104, 105, 106]:
    recent_requests.append(request_id)

print(list(recent_requests))  # [102, 103, 104, 105, 106]
```

What to notice:
- This is a cheap in-memory debugging aid.
- `maxlen` prevents unbounded growth.

Example 13: Sliding error window for local alert logic

```python
from collections import deque

last_five = deque(maxlen=5)

for status in [200, 500, 500, 200, 503, 500, 200]:
    last_five.append(status)
    error_count = sum(code >= 500 for code in last_five)
    print(list(last_five), error_count)
```

What to notice:
- This is a compact local rolling-window pattern.
- It works well when the window size is small and fixed.

Example 14: Queue tasks for breadth-first processing

```python
from collections import deque

tasks = deque(["root_job"])

while tasks:
    current = tasks.popleft()
    print("processing", current)

    if current == "root_job":
        tasks.extend(["child_1", "child_2"])
```

What to notice:
- Deque is a better fit than list for work queues with front removals.
- This shape appears in crawlers, BFS-style jobs, and task expansion pipelines.

#### Common Patterns
- Use deque for queues with frequent front removals.
- Use deque with `maxlen` for rolling history and sliding windows.
- Use deque for BFS and worklist processing.
- Use `rotate()` for round-robin or cyclic scheduling patterns.
- Use deque as a stack when you want symmetry with queue behavior.
- Reach for list instead when random indexing is the dominant operation.

#### Pitfalls to Avoid
- Using a list as a queue with repeated `pop(0)`.
- Forgetting that `extendleft()` reverses the incoming iterable order.
- Treating deque like a list for slicing and frequent middle access.
- Accidentally relying on bracket reads in the middle of a large deque as if they were cheap.
- Using deque where you actually need a heap, priority queue, or sorted structure.
- Forgetting that bounded deques silently evict old items once full.

#### Quick Recap
- Deque means double-ended queue.
- Appends and pops at both ends are O(1).
- `popleft()` is the key advantage over list for queues.
- `maxlen` turns deque into a rolling buffer.
- `rotate()` is useful for cyclic workflows.
- Deque is great for queueing and windows, but not for list-style random access or slicing.

#### Interview Sound Bite
I use `collections.deque` when I need efficient operations at both ends, especially queue behavior with repeated front removals, because `popleft()` stays O(1) while a list-based queue with `pop(0)` keeps shifting elements and gets expensive over time.

#### Memory Hook
Deque = queue-friendly list alternative with fast left side.

#### Practice Questions
1. Why is deque better than list for queue behavior?
2. What is the difference between `appendleft()` and `append()`?
3. What does `maxlen` do?
4. Why is deque usually a poor fit for heavy random indexing?
5. What is a common gotcha with `extendleft()`?
6. When is a list still better than deque?
7. Why is deque a natural fit for BFS?
8. What happens when you append to a full bounded deque?

#### Practice Answers
1. Deque is better because removing from the left with `popleft()` is O(1), while list front removals with `pop(0)` shift remaining elements and are much more expensive over repeated operations.
2. `append()` adds to the right end, while `appendleft()` adds to the left end.
3. `maxlen` sets a fixed capacity, so once full the deque automatically discards items from the opposite side when new ones are appended.
4. It is a poor fit because deque is optimized for the ends, not for frequent indexed access into the middle.
5. `extendleft()` reverses the input iterable's visible order in the final deque because it inserts each item at the left one by one.
6. A list is still better when you mostly need random indexing, slicing, or array-like access patterns.
7. It is a natural fit for BFS because nodes are processed in FIFO order, and deque supports efficient enqueue at the right and dequeue from the left.
8. The deque keeps its maximum size and silently drops an item from the opposite end.

---

<a id="topic-18"></a>
### Topic 18: collections.namedtuple & dataclasses
Status: In Progress

#### Concept in One Line
`namedtuple` and `dataclass` both give structure to related values, but `namedtuple` is a lightweight immutable tuple-like record while `dataclass` is a class-first tool for readable, maintainable data objects.

#### Mental Model
Think of them as two ways to stop passing around anonymous tuples and messy dictionaries.
- `namedtuple` is for compact records that should feel like tuples with names.
- `dataclass` is for small-to-medium domain objects that should feel like normal classes without boilerplate.
- If you want tuple behavior plus field names, think `namedtuple`.
- If you want a real class with generated `__init__`, `__repr__`, and comparisons, think `dataclass`.

#### Memory Behavior in CPython
- A `namedtuple` instance is a tuple subclass, so it stores positional values in a tuple-like structure and is immutable at the field-binding level.
- Because it is tuple-based, a `namedtuple` is generally compact and supports tuple operations like unpacking and indexing.
- A `dataclass` is a normal Python class instance with generated methods layered on top.
- By default, a regular dataclass instance stores attributes in an instance dictionary, unless you use `slots=True`.
- `frozen=True` on a dataclass prevents normal attribute reassignment, but it does not deep-freeze mutable field values.
- Mutable defaults in dataclasses must use `field(default_factory=...)` so each instance gets its own fresh object.
- Both `namedtuple` and dataclass instances hold references to their field values; neither deep-copies values automatically.

#### Key Behaviors and Gotchas
- Use `namedtuple` when the record is simple, mostly immutable, and tuple-like behavior is useful.
- Use `dataclass` when readability, evolution, and explicit fields matter more than tuple compatibility.
- `namedtuple` fields are accessible by name, but the instance still behaves like a tuple.
- Dataclasses generate methods like `__init__`, `__repr__`, and optionally equality and ordering.
- `namedtuple` is immutable at the attribute level; use `_replace()` to create a modified copy.
- Dataclasses are mutable by default.
- Use `frozen=True` if a dataclass should behave like an immutable record.
- Do not use mutable defaults like `tags=[]` in a dataclass; use `field(default_factory=list)`.
- `namedtuple` instances can often be hashable if their fields are hashable.
- A frozen dataclass can also be hashable, depending on configuration and field types.
- If you need methods and validation logic, dataclasses usually scale better than namedtuples.

#### Time Complexity Notes
- Attribute access on either structure: O(1)
- Indexing a `namedtuple`: O(1)
- Creating an instance with `k` fields: O(k)
- Equality comparison: O(k) in the number of fields compared
- Converting to dict-like output with helpers such as `_asdict()` or `asdict()`: O(k), plus nested conversion cost where applicable
- The main trade-off here is not Big-O but ergonomics, immutability, and memory shape

#### Examples
Example 1: Basic `namedtuple`

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)

print(p.x)   # 10
print(p.y)   # 20
print(p[0])  # 10
```

What to notice:
- You get both named fields and tuple-style indexing.
- This is the classic lightweight record shape.

Example 2: Unpack a `namedtuple`

```python
from collections import namedtuple

Color = namedtuple("Color", ["red", "green", "blue"])
color = Color(10, 20, 30)

r, g, b = color
print(r, g, b)  # 10 20 30
```

What to notice:
- A `namedtuple` still behaves like a tuple.
- Unpacking feels natural.

Example 3: Use `_replace()` with `namedtuple`

```python
from collections import namedtuple

User = namedtuple("User", ["name", "role"])
user = User("Aravind", "learner")
updated_user = user._replace(role="engineer")

print(user)         # User(name='Aravind', role='learner')
print(updated_user) # User(name='Aravind', role='engineer')
```

What to notice:
- You do not mutate the original record.
- `_replace()` creates a new instance.

Example 4: `_asdict()` for export

```python
from collections import namedtuple

Book = namedtuple("Book", ["title", "pages"])
book = Book("Python Notes", 250)

print(book._asdict())  # {'title': 'Python Notes', 'pages': 250}
```

What to notice:
- `namedtuple` can be converted to a mapping-friendly representation.
- Helpful for logs, APIs, and serialization prep.

Example 5: Basic dataclass

```python
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    team: str


emp = Employee("Aravind", "platform")
print(emp)  # Employee(name='Aravind', team='platform')
```

What to notice:
- Dataclasses look like normal classes.
- The constructor and readable repr are generated for you.

Example 6: Dataclass with defaults

```python
from dataclasses import dataclass

@dataclass
class ServiceConfig:
    host: str
    port: int = 8000
    debug: bool = False


config = ServiceConfig("localhost")
print(config)  # ServiceConfig(host='localhost', port=8000, debug=False)
```

What to notice:
- Defaults feel natural.
- This is much cleaner than writing the boilerplate by hand.

Example 7: Mutable default pitfall in dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class Report:
    title: str
    tags: list[str] = field(default_factory=list)


report1 = Report("daily")
report2 = Report("weekly")

report1.tags.append("ops")

print(report1.tags)  # ['ops']
print(report2.tags)  # []
```

What to notice:
- `default_factory` gives each instance its own list.
- This avoids the shared mutable default bug.

Example 8: Frozen dataclass

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ApiKey:
    key_id: str
    owner: str


token = ApiKey("k1", "team-a")
print(token.owner)  # team-a
```

What to notice:
- The instance behaves like an immutable record at the attribute level.
- This is the dataclass equivalent of a more stable value object.

Example 9: Dataclass with computed setup in `__post_init__`

```python
from dataclasses import dataclass

@dataclass
class UserInput:
    raw_name: str
    normalized_name: str = ""

    def __post_init__(self):
        self.normalized_name = self.raw_name.strip().lower()


user = UserInput("  Aravind  ")
print(user.normalized_name)  # aravind
```

What to notice:
- `__post_init__` is useful when derived fields depend on the incoming constructor values.
- This is a dataclass advantage over a bare `namedtuple`.

Example 10: Ordering with dataclasses

```python
from dataclasses import dataclass

@dataclass(order=True)
class Score:
    points: int
    name: str


scores = [Score(92, "ana"), Score(85, "bob"), Score(95, "dina")]
print(sorted(scores))
```

What to notice:
- `order=True` generates ordering methods.
- Useful for small value objects that need natural sorting.

Example 11: `namedtuple` as a dict key

```python
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])
visited = {Coordinate(1, 2): "seen"}

print(visited[Coordinate(1, 2)])  # seen
```

What to notice:
- Tuple-like immutability makes this pattern natural when fields are hashable.
- This is one place `namedtuple` feels especially elegant.

Example 12: Convert a dataclass to a plain dict

```python
from dataclasses import asdict, dataclass

@dataclass
class Product:
    name: str
    price: float


product = Product("Keyboard", 49.99)
print(asdict(product))  # {'name': 'Keyboard', 'price': 49.99}
```

What to notice:
- `asdict()` is handy for serialization-friendly output.
- This is often useful before JSON conversion or logging.

#### Production-Style namedtuple / dataclass Examples
Example 13: Use a dataclass for parsed config

```python
from dataclasses import dataclass

@dataclass
class DbConfig:
    host: str
    port: int
    pool_size: int = 10
    ssl_enabled: bool = True


config = DbConfig("db.internal", 5432)
print(config)
```

What to notice:
- Config objects become clearer and safer than raw dicts.
- Named fields reduce key-typo mistakes.

Example 14: Use `namedtuple` for compact read-only rows

```python
from collections import namedtuple

LogRow = namedtuple("LogRow", ["timestamp", "level", "message"])

row = LogRow("2026-06-09T10:00:00", "ERROR", "timeout")
print(row.level)  # ERROR
```

What to notice:
- This is a good fit for compact record-like rows that should stay simple.
- It is especially nice when tuple compatibility matters.

Example 15: Group domain data with nested dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class LineItem:
    name: str
    quantity: int

@dataclass
class Order:
    order_id: int
    items: list[LineItem] = field(default_factory=list)


order = Order(101)
order.items.append(LineItem("mouse", 2))
print(order)
```

What to notice:
- Dataclasses scale well once the structure starts feeling like a real model.
- This is much clearer than nesting raw tuples and dicts.

Example 16: Frozen dataclass as a stable key-like value object

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class FeatureFlagKey:
    service: str
    environment: str


enabled = {FeatureFlagKey("billing", "prod"): True}
print(enabled[FeatureFlagKey("billing", "prod")])  # True
```

What to notice:
- Frozen dataclasses can behave like stable value objects when fields are hashable.
- This is often easier to evolve than a raw tuple key.

#### Common Patterns
- Use `namedtuple` for small immutable records with tuple-like behavior.
- Use `dataclass` for readable models, configs, DTOs, and structured domain objects.
- Use `field(default_factory=...)` for mutable dataclass fields.
- Use `frozen=True` when a dataclass should act like a value object.
- Use `__post_init__` for normalization or derived fields after initialization.
- Convert to dict-like output with `_asdict()` or `asdict()` when integrating with logs or APIs.

#### Pitfalls to Avoid
- Using raw tuples when field names would make the code clearer.
- Using a mutable dataclass default like `items=[]` instead of `default_factory`.
- Expecting `frozen=True` to deep-freeze nested mutable objects.
- Using `namedtuple` when the model is clearly growing methods, validation, or richer behavior.
- Using dataclasses for hot tuple-like records when you really want compact immutable tuple semantics.
- Forgetting that `namedtuple` is still positional under the hood, so field order still matters.

#### Quick Recap
- `namedtuple` is tuple-like, lightweight, and immutable at the field-binding level.
- `dataclass` is class-like, readable, and flexible.
- Use `namedtuple` for compact immutable records.
- Use dataclasses when the model is evolving or needs defaults, methods, or post-init logic.
- `field(default_factory=...)` is the correct fix for mutable dataclass defaults.
- The right choice is mostly about ergonomics and future evolution, not raw Big-O.

#### Interview Sound Bite
I use `namedtuple` when I want a compact immutable record with tuple behavior, and I use `dataclass` when I want a real readable data model with generated boilerplate, defaults, and optional post-initialization logic, because dataclasses scale better as the model becomes more expressive.

#### Memory Hook
`namedtuple` = named immutable tuple. Dataclass = boilerplate-free data class.

#### Practice Questions
1. What problem do `namedtuple` and `dataclass` both solve?
2. When is `namedtuple` a better fit than dataclass?
3. When is dataclass a better fit than `namedtuple`?
4. Why is `field(default_factory=list)` important?
5. What does `frozen=True` do in a dataclass?
6. Why might `__post_init__` be useful?
7. Why can a `namedtuple` often be used as a dict key?
8. What is the practical difference between `_replace()` and mutating a dataclass field?

#### Practice Answers
1. They both solve the problem of representing related values with clear named fields instead of anonymous tuples or loosely structured dictionaries.
2. `namedtuple` is a better fit when the record is simple, immutable, compact, and tuple-like behavior such as unpacking or indexing is useful.
3. Dataclass is a better fit when the model needs defaults, methods, validation, post-init logic, or is likely to evolve over time.
4. It is important because it creates a fresh list for each instance instead of sharing one mutable default across all instances.
5. It prevents normal attribute reassignment, making the dataclass behave more like an immutable value object.
6. It is useful for normalization, validation, or derived-field setup that should happen right after initialization.
7. It can often be used as a dict key because it is tuple-based and immutable at the field-binding level, assuming its contained field values are hashable.
8. `_replace()` creates a new `namedtuple` instance with changed values, while a normal mutable dataclass field can usually be updated directly on the existing instance.

---

<a id="topic-19"></a>
### Topic 19: Sorting Masterclass
Status: Not Started

Notes: Pending.

---

<a id="module-3-doubts"></a>
## Doubts and Q&A Log
Use this section whenever you ask a question during Module 3.

| # | Date | Topic | Your Doubt | Answer Summary | Action |
|---|------|-------|------------|----------------|--------|
| 1 | 2026-05-28 | - | - | - | - |
| 2 | 2026-06-01 | Topic 14: Unpacking | Is it correct to think `*` or `**` on the left packs and on the right unpacks? Why does `[*nums1, *nums2]` produce `[1, 2, 3, 4]` instead of `[[1, 2], [3, 4]]`? | Better rule: starred targets on the left usually collect remaining values, while starred expressions on the right usually expand values into the surrounding call or literal. `[nums1, nums2]` nests two list objects, but `[*nums1, *nums2]` expands both lists element by element into one outer list. | Remember: left starred target collects, right starred expression expands. |
| 3 | 2026-06-02 | Topic 15: collections.Counter | If `Counter` only accepts hashable items, how can `Counter(votes)` work when `votes` is a list? Why do we need `update()` and `subtract()` when `+` and `-` already exist? | The outer container passed to `Counter(...)` only needs to be iterable; the individual counted elements must be hashable. Here the list contains strings, and strings are hashable. Also, `update()` and `subtract()` mutate an existing counter, while `+` and `-` create new counters; `subtract()` preserves zero and negative counts, but `-` drops them. | Remember: iterable container can be unhashable, counted elements cannot. In-place methods and operators also have different semantics. |

---

<a id="module-3-mistakes"></a>
## Mistakes and Corrections
Track recurring mistakes so we can fix patterns quickly.

| # | Date | Mistake | Why It Happened | Correct Pattern |
|---|------|---------|-----------------|-----------------|
| 1 | 2026-05-28 | - | - | - |

---

<a id="module-3-progress"></a>
## Module 3 Progress Tracker

- [x] Topic 12 complete
- [x] Topic 13 complete
- [x] Topic 14 complete
- [x] Topic 15 complete
- [x] Topic 16 complete
- [x] Topic 17 complete
- [ ] Topic 18 complete
- [ ] Topic 19 complete
- [ ] Module 3 revision complete

Current module status: In Progress