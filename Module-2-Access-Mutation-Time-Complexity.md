# Module 2 - Access, Mutation & Time Complexity

## Purpose
This file is the single source of truth for Module 2.
We will keep all theory, examples, your doubts, answers, and progress here.

## Topics Covered in This Module
- Topic 7: Big-O Per Operation (45 min)
- Topic 8: Slicing Deep Dive (30 min)
- Topic 9: List Patterns (45 min)
- Topic 10: Dict Patterns (45 min)
- Topic 11: Set Patterns (30 min)

Estimated total: ~3 hours 15 min

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

### Topic 7: Big-O Per Operation
Status: Complete

#### Concept in One Line
Big-O describes how the cost of an operation grows as input size grows, so it helps you choose the right data structure before performance breaks.

#### Mental Model
Think of Big-O as the shape of the pain curve. For small data, many choices feel fine. As data grows, the wrong structure gets expensive fast. Big-O is how we predict that growth before production traffic teaches it the hard way.

#### Memory Behavior in CPython
- Time complexity comes from the underlying storage strategy of each structure.
- Lists are dynamic arrays, so indexing is fast but front inserts require shifts.
- Tuples are fixed-size sequences, so indexing is still fast, but mutation does not exist.
- Strings are immutable sequences, so concatenation and slicing usually create new objects.
- Dicts and sets use hash tables, which is why lookup, membership, insert, and delete are usually average O(1).
- Copying a container usually means copying references into a new container, so cost grows with the number of elements copied.
- Big-O is about growth rate, not exact runtime. CPython implementation details explain the behavior, but the key lesson is choosing structures whose growth pattern matches the workload.

#### Key Behaviors and Gotchas
- O(1) does not mean "free"; it means the cost does not grow much with input size.
- Average-case O(1) for dicts and sets is not the same as guaranteed O(1) in every pathological case.
- Amortized O(1) means most operations are cheap, but a few occasional ones cost more.
- `x in data` changes complexity depending on the type of `data`.
- Nested loops are not automatically O(n^2); complexity depends on how many total times the inner work runs.
- A slower Big-O can still win on tiny data because constant factors matter.
- An algorithm can trade extra memory for better runtime, and that is often the right choice.

#### Time Complexity Notes
- List index access: O(1)
- List append: amortized O(1)
- List insert/pop at front or middle: O(n)
- List membership: O(n)
- Tuple index access: O(1)
- Tuple membership: O(n)
- String index access: O(1)
- String concatenation with `+`: O(len(a) + len(b))
- Dict key lookup / insert / update / delete: average O(1)
- Dict key membership: average O(1)
- Set membership / add / remove: average O(1)
- Full copy of a sequence or mapping: O(n)
- Sorting: O(n log n)

Quick cheat sheet:

| Structure | Fast Operations | Expensive Operations |
|-----------|-----------------|----------------------|
| list | index, append, pop() | pop(0), insert(0, x), membership |
| tuple | index, iteration | membership, rebuilding |
| str | index, iteration | repeated concatenation, slicing copies |
| dict | key lookup, key insert, key update | full iteration, copy |
| set | membership, add, remove | full iteration, converting back to ordered forms |

#### Examples
Example 1: Membership cost depends on the structure

```python
from timeit import timeit

numbers_list = list(range(100_000))
numbers_set = set(numbers_list)

list_time = timeit("99_999 in numbers_list", globals=globals(), number=1_000)
set_time = timeit("99_999 in numbers_set", globals=globals(), number=1_000)

print(f"list membership: {list_time:.6f}s")
print(f"set membership:  {set_time:.6f}s")
```

What to notice:
- List membership scans.
- Set membership hashes.
- Same question, different growth behavior.

Example 2: End append vs front insert on list

```python
from timeit import timeit

append_time = timeit(
    "lst.append(1)",
    setup="lst = list(range(100_000))",
    number=20_000,
)

front_insert_time = timeit(
    "lst.insert(0, 1)",
    setup="lst = list(range(100_000))",
    number=2_000,
)

print(f"append end:   {append_time:.6f}s")
print(f"insert front: {front_insert_time:.6f}s")
```

What to notice:
- Appending touches the tail.
- Front insert shifts the rest of the array.

Example 3: Dict lookup beats list scan for keyed access

```python
records_list = [{"id": i, "name": f"user-{i}"} for i in range(100_000)]
records_dict = {row["id"]: row for row in records_list}

target = 90_000

found_from_list = next(row for row in records_list if row["id"] == target)
found_from_dict = records_dict[target]

print(found_from_list)
print(found_from_dict)
```

What to notice:
- The list search is linear.
- The dict lookup is direct by key.
- If lookups repeat, indexing once into a dict usually wins.

Example 4: Copying costs grow with data size

```python
from timeit import timeit

copy_small = timeit("data[:]", setup="data = list(range(100))", number=50_000)
copy_large = timeit("data[:]", setup="data = list(range(100_000))", number=500)

print(f"small copy: {copy_small:.6f}s")
print(f"large copy: {copy_large:.6f}s")
```

What to notice:
- A slice copy is not O(1).
- The amount copied matters.

Example 5: Sorting follows a more expensive growth curve than lookup

```python
values = [9, 2, 7, 1, 5]
print(sorted(values))
```

What to notice:
- Sorting is fundamentally heavier than direct access or membership.
- It is worth doing when order is needed, but not for every lookup problem.

#### Common Patterns
- Use a list when order and append matter.
- Use a set when repeated membership checks matter.
- Use a dict when fast lookup by meaningful key matters.
- Convert data once into a set or dict when the workload performs repeated lookups.
- Use tuple for fixed records, not for frequent mutation.
- Prefer measuring with `timeit` when two options seem close in practice.

#### Pitfalls to Avoid
- Using list membership inside hot loops when a set would fit the problem better.
- Treating amortized O(1) as if it means every single operation is identical in cost.
- Forgetting that copies and slices are proportional to data copied.
- Optimizing based only on theory when input sizes are tiny and readability matters more.
- Ignoring algorithm shape and only looking at one operation in isolation.
- Sorting data when you only needed membership or direct lookup.

#### Quick Recap
- Big-O is about growth, not exact stopwatch time.
- Underlying structure decides the common operation costs.
- Lists are great for order and append, weak for front mutation and membership.
- Dicts and sets win when lookup or membership repeats.
- Choosing the right structure early avoids performance pain later.

#### Interview Sound Bite
I choose Python data structures by workload shape: lists for ordered sequences, sets for fast membership, dicts for keyed lookup, and I use Big-O to reason about how that choice will scale as data grows.

#### Memory Hook
Big-O = growth curve, not stopwatch.

#### Practice Questions
1. Why is `x in my_list` usually slower than `x in my_set`?
2. What does amortized O(1) really mean for `list.append()`?
3. Why is slicing a list not O(1)?
4. When is a dict better than a list of records?
5. Why is sorting usually more expensive than direct lookup?

#### Practice Answers
1. `x in my_list` usually scans values one by one, while `x in my_set` usually uses hashing to jump near the right slot directly.
2. Amortized O(1) means most appends are cheap, but occasional resizes make some appends more expensive.
3. Slicing a list creates a new list and copies references for the sliced range, so the cost grows with the slice length.
4. A dict is better than a list of records when you do repeated lookups by a meaningful key like `id`, `email`, or `sku`.
5. Sorting compares and rearranges many values to produce order, while direct lookup or membership only answers one specific question.

---

### Topic 8: Slicing Deep Dive
Status: Complete

#### Concept in One Line
Slicing selects a range from a sequence using `[start:stop:step]`, where `start` is inclusive, `stop` is exclusive, and `step` controls how you move through the data.

#### Mental Model
Think of slicing like placing two markers on a ruler and then deciding how to walk between them. You start at `start`, stop before `stop`, and hop by `step`. A negative step means you walk backward instead of forward.

#### Memory Behavior in CPython
- Slicing built-in sequences like `list`, `tuple`, and `str` usually creates a new object, not a view into the old one.
- For lists and tuples, the sliced container holds references to the same inner objects, so slicing is shallow.
- That means nested mutable objects are still shared between the original sequence and the slice.
- String slices create new string values because strings are immutable.
- A full list slice like `lst[:]` creates a new outer list object.
- Slice assignment such as `lst[1:3] = [...]` mutates the original list in place and may shift later elements.
- Because slicing copies elements or references into a new container, slicing cost grows with the slice length.

#### Key Behaviors and Gotchas
- `start` is included, `stop` is excluded.
- Negative indices count from the end: `-1` means last item, `-2` means second last, and so on.
- Omitting values gives defaults, so `seq[:]` means the whole sequence.
- `seq[::-1]` walks backward one step at a time, which is why it reverses the sequence.
- `step` cannot be zero.
- Slicing out of bounds does not raise `IndexError`; Python clips the range safely.
- A slice copy is different from aliasing, but it is still shallow for nested mutable values.
- Slice assignment works for mutable sequences like `list`, but not for immutable sequences like `tuple` and `str`.

#### Time Complexity Notes
- Single index access: O(1)
- Slice of length `k`: O(k)
- Full slice copy of length `n`: O(n)
- Reverse with `[::-1]`: O(n)
- Membership on a slice: depends on the slice size, usually O(k)
- List slice assignment: grows with the replaced region and any shifting work; treat it as proportional to the size affected

#### Examples
Example 1: Basic slicing rules

```python
data = [0, 1, 2, 3, 4, 5]

print(data[1:4])   # [1, 2, 3]
print(data[:3])    # [0, 1, 2]
print(data[3:])    # [3, 4, 5]
print(data[::2])   # [0, 2, 4]
print(data[1:5:2]) # [1, 3]
```

What to notice:
- `start` is included.
- `stop` is excluded.
- `step` controls the stride.

Example 2: Negative indices and reverse slicing

```python
text = "python"

print(text[-3:])    # hon
print(text[:-1])    # pytho
print(text[::-1])   # nohtyp
print(text[5:1:-1]) # noht
```

What to notice:
- Negative indices count from the end.
- Negative step means move backward.
- When moving backward, your start must be to the right of your stop to collect anything.

Example 3: Slicing creates a new outer list, but it is shallow

```python
matrix = [[1, 2], [3, 4], [5, 6]]
copy_matrix = matrix[:]

matrix[0].append(99)

print(matrix)       # [[1, 2, 99], [3, 4], [5, 6]]
print(copy_matrix)  # [[1, 2, 99], [3, 4], [5, 6]]
print(matrix is copy_matrix)  # False
```

What to notice:
- The outer list is new.
- The inner lists are still shared references.

Example 4: Out-of-bounds slicing is safe

```python
values = [10, 20, 30]

print(values[0:10])   # [10, 20, 30]
print(values[10:20])  # []
print(values[-10:2])  # [10, 20]
```

What to notice:
- Slicing is forgiving.
- Python clips the range instead of throwing `IndexError`.

Example 5: Palindrome check with slicing

```python
word = "level"
print(word == word[::-1])  # True
```

What to notice:
- Reverse slicing is concise.
- This is elegant for simple interview-style problems.

Example 6: Slice assignment mutates the same list object

```python
nums = [10, 20, 30, 40, 50]
nums[1:4] = [200, 300]

print(nums)  # [10, 200, 300, 50]
```

What to notice:
- Slice reading creates a value.
- Slice assignment changes the original list in place.
- The replacement can change the list length.

Example 7: Every-nth element pattern

```python
events = ["e1", "e2", "e3", "e4", "e5", "e6"]
print(events[::3])  # ['e1', 'e4']
```

What to notice:
- Slicing is useful for sampling or stepping patterns.
- It stays readable when the stride is meaningful.

#### Common Patterns
- Use `seq[:n]` for a prefix.
- Use `seq[n:]` for a suffix.
- Use `seq[:-1]` or `seq[1:]` to drop edges.
- Use `seq[::-1]` for a quick reverse.
- Use `seq[::k]` for every `k`th item.
- Use `lst[:]` for a shallow outer copy of a list.
- Use slice assignment to replace or delete a range in a list.

#### Pitfalls to Avoid
- Thinking the stop index is included.
- Assuming slicing returns a view into the original list.
- Forgetting that list slicing is shallow for nested mutables.
- Using repeated slicing in tight loops when it creates too many copies.
- Forgetting that `[::-1]` copies rather than reversing in place.
- Using `step=0`, which raises `ValueError`.

#### Quick Recap
- Slicing uses `[start:stop:step]`.
- `start` is inclusive, `stop` is exclusive.
- Negative indices count from the end, and negative steps move backward.
- List slicing copies the outer container, not nested mutable contents.
- Slice assignment mutates a list in place.

#### Interview Sound Bite
In Python, slicing is a range-selection tool with inclusive start and exclusive stop; it is powerful for extraction and reversal, but I remember that built-in slices usually allocate new objects and list slices are shallow copies.

#### Memory Hook
Slice = take a range, not a view.

#### Practice Questions
1. Why does `seq[1:4]` return three items instead of four?
2. Why can `matrix[:]` still lead to shared nested mutations?
3. What does `[::-1]` mean exactly?
4. Why does `values[100:200]` return `[]` instead of crashing?
5. What is the difference between `nums[1:3]` and `nums[1:3] = [...]`?

#### Practice Answers
1. `seq[1:4]` returns three items because slicing includes the start index but excludes the stop index.
2. `matrix[:]` only copies the outer list, so the inner lists remain shared references between the original and the slice.
3. `[::-1]` means take the whole sequence and walk through it backward one step at a time.
4. `values[100:200]` returns `[]` because slicing is bounds-safe and Python clips the requested range instead of raising `IndexError`.
5. `nums[1:3]` reads and returns a slice value, while `nums[1:3] = [...]` mutates that region of the original list in place.

---

### Topic 9: List Patterns
Status: In Progress

#### Concept in One Line
List patterns are the common problem-solving shapes that make lists powerful in real code: filtering, flattening, grouping, chunking, zipping, rotating, and deduplicating while preserving order.

#### Mental Model
Think of a list as a flexible conveyor belt. List patterns are the standard operations you perform on that belt: keep some items, reshape them, combine multiple belts, split one belt into chunks, or rearrange order without losing clarity.

#### Memory Behavior in CPython
- Most list pattern operations create a new list rather than mutating the old one.
- List comprehensions allocate a fresh list and append references into it.
- Generator expressions do not build the whole result up front; they produce one value at a time as you iterate.
- Flattening usually builds a new output list, which grows with the total number of nested elements produced.
- `zip()` itself is lazy in Python 3, but converting it to `list(zip(...))` materializes the paired values in memory.
- Generator functions using `yield` also stay lazy and preserve execution state between iterations.
- `dict.fromkeys(lst)` for order-preserving deduplication creates an intermediate dict before producing the final list.
- Chunking with slicing creates multiple new list objects, and each slice is shallow.
- Rotating with slicing like `lst[k:] + lst[:k]` creates new lists and then combines them, so it is elegant but not free.

#### Key Behaviors and Gotchas
- A list comprehension is often clearer and faster than building the same list with repeated `append()` in a manual loop.
- A generator expression is the lazy sibling of a list comprehension.
- Flattening one level is easy; flattening arbitrary depth usually needs recursion or an explicit stack.
- `zip()` stops at the shortest input.
- Use `itertools.zip_longest()` when you need to keep going across uneven inputs.
- `zip(*matrix)` is a compact transpose pattern.
- `lst[i:i+n]` is a standard chunking pattern, but the last chunk may be shorter.
- Order-preserving deduplication is not the same as plain deduplication with `set()`.
- Rotating with slicing handles many problems cleanly, but modulo arithmetic keeps rotation counts safe.
- Generators are one-pass iterators; once consumed, they are exhausted.

#### Time Complexity Notes
- Filtering a list: O(n)
- Mapping or transforming a list: O(n)
- Flattening one level with total `n` produced elements: O(n)
- Deduplicate while preserving order: O(n)
- Chunking into slices across the whole list: O(n)
- Transpose a matrix of `r x c`: O(r * c)
- Rotation via slicing: O(n)
- Zipping two lists of length `n`: O(n) when materialized
- A generator expression does O(n) total work when fully consumed, but it does not store all `n` produced values at once

#### Examples
Example 1: Filtering with a comprehension

```python
nums = [1, 2, 3, 4, 5, 6]
evens = [num for num in nums if num % 2 == 0]

print(evens)  # [2, 4, 6]
```

What to notice:
- This is the cleanest common filtering pattern.
- One pass over the data, one resulting list.

Example 2: Flatten one level of nesting

```python
rows = [[1, 2], [3, 4], [5, 6]]
flat = [value for row in rows for value in row]

print(flat)  # [1, 2, 3, 4, 5, 6]
```

What to notice:
- The order of loops in the comprehension matches nested iteration.
- This is for one-level flattening, not arbitrary depth.

Example 3: Deduplicate while preserving order

```python
names = ["ana", "bob", "ana", "chris", "bob", "dina"]
unique_names = list(dict.fromkeys(names))

print(unique_names)  # ['ana', 'bob', 'chris', 'dina']
```

What to notice:
- `set(names)` removes duplicates but loses order semantics.
- `dict.fromkeys()` preserves first-seen order.

Example 4: Chunk a list into fixed-size groups

```python
data = list(range(1, 11))
chunks = [data[i:i + 3] for i in range(0, len(data), 3)]

print(chunks)  # [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
```

What to notice:
- Slicing makes chunking easy.
- The final chunk may be smaller.

Example 5: Transpose a matrix

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
]

transposed = [list(col) for col in zip(*matrix)]
print(transposed)  # [[1, 4], [2, 5], [3, 6]]
```

What to notice:
- `zip(*matrix)` is one of Python's most useful shape-transform tricks.
- `zip()` returns tuples, so we convert columns to lists here.

Example 6: Zip two lists together

```python
names = ["ana", "bob", "chris"]
scores = [92, 85, 88]

paired = list(zip(names, scores))
print(paired)  # [('ana', 92), ('bob', 85), ('chris', 88)]
```

What to notice:
- `zip()` combines positionally.
- It stops at the shorter input.

Example 7: Unzip paired data

```python
pairs = [("ana", 92), ("bob", 85), ("chris", 88)]
names, scores = zip(*pairs)

print(names)   # ('ana', 'bob', 'chris')
print(scores)  # (92, 85, 88)
```

What to notice:
- `zip(*pairs)` reverses a previously zipped structure.
- This is often called unzipping.

Example 8: Uneven inputs with `zip()` vs `zip_longest()`

```python
from itertools import zip_longest

names = ["ana", "bob", "chris"]
scores = [92, 85]

print(list(zip(names, scores)))
print(list(zip_longest(names, scores, fillvalue="missing")))
```

What to notice:
- `zip()` truncates to the shortest input.
- `zip_longest()` preserves the longer input and fills missing values.

Example 9: Generator expression vs list comprehension

```python
nums = [1, 2, 3, 4, 5]

squares_list = [num * num for num in nums]
squares_gen = (num * num for num in nums)

print(squares_list)       # [1, 4, 9, 16, 25]
print(next(squares_gen))  # 1
print(next(squares_gen))  # 4
```

What to notice:
- The list comprehension builds everything immediately.
- The generator expression yields values on demand.
- The generator keeps moving forward as you consume it.

Example 10: Generator function for chunked processing

```python
def chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]

for chunk in chunked(list(range(1, 8)), 3):
    print(chunk)
```

What to notice:
- `yield` turns the function into a generator.
- This pattern is useful when you want chunk-by-chunk processing instead of building all chunks at once.

Example 11: Rotate a list left

```python
items = [1, 2, 3, 4, 5]
k = 2
k %= len(items)

rotated = items[k:] + items[:k]
print(rotated)  # [3, 4, 5, 1, 2]
```

What to notice:
- Rotation is just two slices glued together.
- Modulo makes large rotation counts safe.

Example 12: Remove falsy values

```python
values = [0, 1, "", "python", None, [], [1, 2]]
cleaned = [value for value in values if value]

print(cleaned)  # [1, 'python', [1, 2]]
```

What to notice:
- This is a compact cleanup pattern.
- Be careful: it removes all falsy values, not just `None`.

#### Common Patterns
- Use comprehensions for filter-and-transform tasks.
- Use generator expressions when you want lazy transformation rather than immediate materialization.
- Use nested comprehensions for one-level flattening.
- Use `dict.fromkeys()` to deduplicate while preserving order.
- Use slicing with a step in `range()` for chunking.
- Use `zip()` to pair related lists.
- Use `zip(*pairs)` to unzip paired data.
- Use `zip_longest()` when uneven inputs must be preserved.
- Use `zip(*matrix)` for transpose problems.
- Use generator functions with `yield` for streaming or chunked processing.
- Use slicing plus concatenation for simple rotations.

#### Pitfalls to Avoid
- Using `set()` when first-seen order must be preserved.
- Overusing nested comprehensions when a simple loop would be clearer.
- Forgetting that `zip()` stops at the shortest iterable.
- Assuming `zip()` pads automatically when inputs differ in length.
- Treating shallow flattening as if it handled arbitrary nesting.
- Forgetting that generators are exhausted after you iterate through them.
- Converting a generator to a list immediately and then expecting a memory benefit.
- Repeatedly slicing large lists in hot loops without considering copy cost.
- Removing falsy values when you only meant to remove `None`.

#### Quick Recap
- List patterns are reusable shapes for common data work.
- Comprehensions are central for filtering and transforming.
- `zip()` is for pairing, `zip(*pairs)` is for unpairing, and `zip_longest()` helps with uneven inputs.
- Generators let you process values lazily instead of materializing them all at once.
- Flattening, chunking, transposing, and rotating are mostly composition of simple tools.
- Preserving order during deduplication needs a different approach than plain `set()`.
- Clean patterns matter because list operations are frequent in interviews and production code.

#### Interview Sound Bite
For Python list problems, I lean on a small set of reusable patterns: comprehensions or generators for transform, `dict.fromkeys()` for ordered deduplication, `zip()` and `zip(*...)` for pairing and reshaping, and slicing for chunking and rotation.

#### Memory Hook
List patterns = reshape the conveyor belt. Generators = do not load the whole belt.

#### Practice Questions
1. Why is `dict.fromkeys(lst)` often better than `set(lst)` for deduplication?
2. How does `zip(*matrix)` transpose rows into columns?
3. Why is `[x for row in rows for x in row]` only a one-level flatten?
4. Why can chunking with slicing be expensive on very large lists?
5. What is the risk of filtering with `if value`?
6. Why does `zip()` sometimes seem to "drop" extra values?
7. What is the practical difference between a list comprehension and a generator expression?

#### Practice Answers
1. `dict.fromkeys(lst)` preserves the first-seen order of elements, while `set(lst)` only guarantees uniqueness, not meaningful order.
2. `zip(*matrix)` unpacks each row as a separate argument to `zip()`, so `zip()` groups elements by position, effectively turning columns into tuples.
3. `[x for row in rows for x in row]` only flattens one nesting layer because it assumes each `row` is directly iterable into final values.
4. Chunking with slicing creates many new list objects and copies references into each slice, so the total work still scales with the data size.
5. `if value` removes every falsy value such as `0`, `''`, `None`, and `[]`, which may be broader than the intended cleanup.
6. `zip()` stops at the shortest iterable, so any extra values in longer inputs are ignored unless you use `itertools.zip_longest()`.
7. A list comprehension builds the full result list immediately, while a generator expression produces values lazily as you iterate, which can save memory for large or streaming workloads.

---

### Topic 10: Dict Patterns
Status: Not Started

Notes: Pending.

---

### Topic 11: Set Patterns
Status: Not Started

Notes: Pending.

---

## Doubts and Q&A Log
Use this section whenever you ask a question during Module 2.

| # | Date | Topic | Your Doubt | Answer Summary | Action |
|---|------|-------|------------|----------------|--------|
| 1 | 2026-05-24 | Topic 8: Slicing Deep Dive | Does `start > stop` without negative indexing also work for reading a string in reverse? | Yes, but only when the slice step is negative. Reverse slicing depends on a negative step like `s[5:1:-1]`, not on negative indices. If `start > stop` and the step is positive or omitted, the result is an empty slice. | Remember: reverse direction comes from negative step, not from negative indices. |

---

## Mistakes and Corrections
Track recurring mistakes so we can fix patterns quickly.

| # | Date | Mistake | Why It Happened | Correct Pattern |
|---|------|---------|-----------------|-----------------|
| 1 | 2026-05-22 | - | - | - |

---

## Module 2 Progress Tracker

- [x] Topic 7 complete
- [x] Topic 8 complete
- [ ] Topic 9 complete
- [ ] Topic 10 complete
- [ ] Topic 11 complete
- [ ] Module 2 revision complete

Current module status: In Progress