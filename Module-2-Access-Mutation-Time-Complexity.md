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
Status: In Progress

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
Status: Not Started

Notes: Pending.

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
- [ ] Topic 8 complete
- [ ] Topic 9 complete
- [ ] Topic 10 complete
- [ ] Topic 11 complete
- [ ] Module 2 revision complete

Current module status: In Progress