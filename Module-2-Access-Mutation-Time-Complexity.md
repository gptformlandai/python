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
Status: In Progress

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
Status: Not Started

Notes: Pending.

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
| 1 | 2026-05-22 | - | - | - | - |

---

## Mistakes and Corrections
Track recurring mistakes so we can fix patterns quickly.

| # | Date | Mistake | Why It Happened | Correct Pattern |
|---|------|---------|-----------------|-----------------|
| 1 | 2026-05-22 | - | - | - |

---

## Module 2 Progress Tracker

- [ ] Topic 7 complete
- [ ] Topic 8 complete
- [ ] Topic 9 complete
- [ ] Topic 10 complete
- [ ] Topic 11 complete
- [ ] Module 2 revision complete

Current module status: In Progress