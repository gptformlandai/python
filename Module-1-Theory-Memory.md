# Module 1 - Theory & Memory Internals

## Purpose
This file is the single source of truth for Module 1.
We will keep all theory, examples, your doubts, answers, and progress here.

## Topics Covered in This Module
- Topic 1: Python Object Model (45 min)
- Topic 2: Lists - Internals (45 min)
- Topic 3: Tuples - Internals (30 min)
- Topic 4: Strings (30 min)
- Topic 5: Dicts - Hash Table Internals (60 min)
- Topic 6: Sets and Frozensets (30 min)

Estimated total: ~4 hours

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

### Topic 1: Python Object Model
Status: In Progress

#### Concept in One Line
In Python, variables store references to objects, not raw values.

#### Mental Model
Think of a variable as a label and an object as a box in memory. Multiple labels can point to the same box.

#### Memory Behavior
- Every value in Python is an object with identity, type, and value.
- Use id(obj) to view identity and type(obj) to view object type.
- Assignment copies references, not objects.
- Mutable objects can change in-place; immutable objects create a new object when changed.

#### Key Behaviors and Gotchas
- is checks identity (same object), == checks value equality.
- Aliasing: b = a means both names point to the same object.
- For mutable objects (list, dict, set), changes through one alias appear in the other.
- For immutable objects (int, str, tuple), updates usually bind to a new object.

#### Time Complexity Notes
- Name assignment is O(1).
- Access by variable name is O(1) on average.
- Equality check cost depends on object size/content.

#### Examples
Example 1: Identity vs equality

```python
a = [1, 2, 3]
b = a
c = [1, 2, 3]

print(a is b)  # True, same object
print(a == b)  # True, same content
print(a is c)  # False, different object
print(a == c)  # True, same content
```

Example 2: Mutable aliasing

```python
x = {"topic": "python"}
y = x
y["level"] = "beginner"

print(x)  # {'topic': 'python', 'level': 'beginner'}
print(y)  # {'topic': 'python', 'level': 'beginner'}
```

Example 3: Immutable rebinding

```python
p = "py"
q = p
q += "thon"

print(p)  # py
print(q)  # python
print(p is q)  # False
```

Example 4: Mutable default argument bug

```python
def add_item(item, bucket=[]):
	bucket.append(item)
	return bucket

print(add_item("a"))  # ['a']
print(add_item("b"))  # ['a', 'b']  <- unexpected for many learners
```

Correct pattern:

```python
def add_item_safe(item, bucket=None):
	if bucket is None:
		bucket = []
	bucket.append(item)
	return bucket

print(add_item_safe("a"))  # ['a']
print(add_item_safe("b"))  # ['b']
```

#### Common Patterns
- Use copy() or deepcopy() when you need an independent mutable object.
- Use == for value comparison unless identity is explicitly required.
- Treat function arguments to mutable objects carefully to avoid side effects.

#### Pitfalls to Avoid
- Using is instead of == for strings or numbers in normal comparisons.
- Assuming b = a makes a new list/dict copy.
- Modifying mutable default arguments in function definitions.

#### Quick Recap
- Variables are references.
- Objects have identity, type, and value.
- is and == are different checks.
- Mutable objects can be shared accidentally through aliasing.
- Immutable updates usually rebind to a new object.

#### Interview Sound Bite
In Python, a variable is just a reference to an object, so assignment shares the same object until you explicitly copy or rebind.

#### Memory Hook
Name -> object, not name -> raw value.

#### Practice Questions
1. Why does appending to one list affect another variable sometimes?
2. When should you use is instead of ==?
3. What changes when assignment happens for immutable objects?

#### Practice Answers
1. Appending to one list affects another variable when both names point to the same underlying list object. Assignment shares the reference unless you create a copy.
2. Use `is` when you want to check identity, such as `x is None`. Use `==` for normal value comparison.
3. With immutable objects, an apparent "update" usually creates a new object and rebinds the variable name to it, instead of changing the original object in place.

---

### Topic 2: Lists - Internals
Status: In Progress

#### Concept in One Line
A Python list is a dynamic array of object references: fast for indexing and append, but expensive when elements must shift.

#### Mental Model
Think of a list as a row of numbered slots in memory. Each slot holds a reference to an object. When the row becomes full, Python creates a bigger row and moves the references over.

#### Memory Behavior
- CPython lists are dynamic arrays, not linked lists.
- A list stores references to objects, not the objects' raw bytes inline.
- Because slots are contiguous, `lst[i]` is fast.
- CPython keeps extra spare capacity when growing a list, so it does not reallocate on every `append()`.
- When capacity runs out, Python allocates a larger block and copies references to the new block.
- That is why `append()` is amortized O(1): most appends are cheap, but a few trigger resize work.
- `sys.getsizeof(lst)` shows the size of the list container and its pointer slots, not the deep memory of objects inside it.

#### Key Behaviors and Gotchas
- `append(x)` adds at the end and is usually cheap.
- `insert(0, x)` and `pop(0)` are expensive because all later elements shift by one slot.
- Lists are excellent stacks with `append()` and `pop()`.
- Lists are poor queues when you frequently remove from the front.
- Slicing like `lst[:]` creates a new outer list.
- `[[0] * 3] * 2` creates two references to the same inner list, not two independent rows.
- `list.sort()` sorts in place and returns `None`.

#### Time Complexity Notes
- Index access: O(1)
- Index update: O(1)
- Append at end: amortized O(1)
- Pop from end: O(1)
- Insert near front or middle: O(n)
- Pop near front or middle: O(n)
- Membership test (`x in lst`): O(n)
- Copy / full slice: O(n)
- Slice of length `k`: O(k)

#### Examples
Example 1: List stores references, so shallow copies still share nested objects

```python
outer = [[1, 2], [3, 4]]
copy_outer = outer.copy()

outer[0].append(99)

print(outer)       # [[1, 2, 99], [3, 4]]
print(copy_outer)  # [[1, 2, 99], [3, 4]]
```

Example 2: Observe over-allocation with `sys.getsizeof`

```python
import sys

data = []
last_size = sys.getsizeof(data)

for i in range(40):
    data.append(i)
    current_size = sys.getsizeof(data)
    if current_size != last_size:
        print(f"len={len(data):2d}, bytes={current_size}")
        last_size = current_size
```

What to notice:
- Size jumps in chunks, not on every append.
- That jump is the spare capacity strategy that makes repeated appends efficient.

Example 3: `append()` vs `insert(0, x)`

```python
from timeit import timeit

append_time = timeit(
    "lst.append(1)",
    setup="lst = list(range(100_000))",
    number=20_000,
)

insert_front_time = timeit(
    "lst.insert(0, 1)",
    setup="lst = list(range(100_000))",
    number=2_000,
)

print(f"append end:   {append_time:.6f}s")
print(f"insert front: {insert_front_time:.6f}s")
```

What to notice:
- `append()` touches the end only.
- `insert(0, x)` shifts many elements, so it gets expensive as the list grows.

Example 4: Stack is natural, queue is not

```python
stack = []
stack.append("page-1")
stack.append("page-2")
print(stack.pop())  # page-2

queue = ["task-1", "task-2", "task-3"]
print(queue.pop(0))  # works, but O(n)
```

If front operations are frequent, prefer:

```python
from collections import deque

queue = deque(["task-1", "task-2", "task-3"])
print(queue.popleft())  # O(1)
```

#### Common Patterns
- Use a list when you need an ordered, mutable, indexable sequence.
- Use `append()` plus `pop()` for stack behavior.
- Use list comprehensions for building transformed lists cleanly.
- Use `lst.copy()` or `lst[:]` when you need a new outer list.
- Switch to `collections.deque` when the workload needs queue semantics.

#### Pitfalls to Avoid
- Using `pop(0)` or `insert(0, x)` in performance-sensitive code.
- Assuming `sys.getsizeof()` includes all nested object memory.
- Building a 2D list with `[[0] * cols] * rows`.
- Forgetting that slicing copies references into a new list.
- Choosing a list for frequent membership checks when a `set` would fit better.

#### Quick Recap
- Python lists are dynamic arrays of references.
- Indexing is fast because positions map directly to contiguous slots.
- Appending is usually cheap because of over-allocation.
- Front insertions and deletions are slow because elements shift.
- Lists make great stacks and poor high-throughput queues.

#### Interview Sound Bite
A Python list is a dynamic array, so I get O(1) indexing and amortized O(1) append, but I avoid it for queue-heavy workloads because front operations are O(n).

#### Memory Hook
List = dynamic array. End good, front bad.

#### Practice Questions
1. Why is `append()` amortized O(1) instead of guaranteed O(1)?
2. Why does `pop(0)` slow down as the list grows?
3. What exactly does `sys.getsizeof()` measure for a list?
4. Why does `[[0] * 3] * 2` create a surprising bug?
5. When would `deque` be a better choice than `list`?

#### Practice Answers
1. `append()` is amortized O(1) because most appends only place a reference into free capacity, but occasionally Python must resize the array and copy existing references, which is more expensive.
2. `pop(0)` slows down because removing the first element forces every remaining element to shift one position left, so the amount of work grows with list size.
3. `sys.getsizeof()` measures the memory used by the list container itself, including its current slot allocation, but not the full deep memory of the objects stored inside it.
4. `[[0] * 3] * 2` repeats references to the same inner list, so changing one row changes the other because both rows alias the same object.
5. `deque` is better when you need frequent inserts or removals from the left side, such as queue workloads, BFS traversal, or streaming buffers.

---

### Topic 3: Tuples - Internals
Status: Not Started

Notes: Pending.

---

### Topic 4: Strings
Status: Not Started

Notes: Pending.

---

### Topic 5: Dicts - Hash Table Internals
Status: Not Started

Notes: Pending.

---

### Topic 6: Sets and Frozensets
Status: Not Started

Notes: Pending.

---

## Doubts and Q&A Log
Use this section whenever you ask a question during Module 1.

| # | Date | Topic | Your Doubt | Answer Summary | Action |
|---|------|-------|------------|----------------|--------|
| 1 | 2026-04-21 | - | - | - | - |

---

## Mistakes and Corrections
Track recurring mistakes so we can fix patterns quickly.

| # | Date | Mistake | Why It Happened | Correct Pattern |
|---|------|---------|-----------------|-----------------|
| 1 | 2026-04-21 | - | - | - |

---

## Module 1 Progress Tracker

- [ ] Topic 1 complete
- [ ] Topic 2 complete
- [ ] Topic 3 complete
- [ ] Topic 4 complete
- [ ] Topic 5 complete
- [ ] Topic 6 complete
- [ ] Module 1 revision complete

Current module status: In Progress
