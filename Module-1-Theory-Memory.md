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
Status: In Progress

#### Concept in One Line
A tuple is a fixed-size, immutable sequence of object references: lightweight, stable, and safe to hash when all its elements are hashable.

#### Mental Model
Think of a tuple as a sealed container with numbered slots. You can read what is inside each slot, but you cannot add, remove, or replace slots after creation.

#### Memory Behavior
- CPython tuples store references to objects, just like lists do.
- Unlike lists, tuples do not keep extra spare capacity for future growth because their size never changes.
- That fixed-size layout usually gives tuples a smaller memory footprint than lists with the same elements.
- Immutability lets Python safely reuse tuple constants created from only compile-time constants.
- This is why literal tuples like `(1, 2, 3)` can be constant-folded by the compiler, while lists are normally built at runtime.
- `sys.getsizeof()` shows the tuple container size, not the deep memory of objects stored inside it.

#### Key Behaviors and Gotchas
- Tuples are immutable, so `t[0] = 10` raises `TypeError`.
- A tuple can still contain mutable objects, and those nested objects can change.
- A tuple is hashable only if every element inside it is hashable.
- That makes tuples useful as dictionary keys, set members, and cache keys.
- Parentheses alone do not make a tuple; the comma does. Example: `(5)` is an `int`, but `(5,)` is a one-item tuple.
- Multiple assignment and multiple return values use tuple packing and unpacking.

#### Time Complexity Notes
- Index access: O(1)
- Iteration: O(n)
- Membership test (`x in tup`): O(n)
- Slicing: O(k)
- Tuple creation from `n` items: O(n)
- Hashing: O(n) in the number of elements because Python combines the hashes of the contained values

#### Examples
Example 1: Tuple usually uses less memory than list for the same items

```python
import sys

numbers_list = [1, 2, 3, 4, 5]
numbers_tuple = (1, 2, 3, 4, 5)

print(sys.getsizeof(numbers_list))
print(sys.getsizeof(numbers_tuple))
```

What to notice:
- The tuple container is usually smaller.
- The saved space comes from fixed size and no over-allocation for growth.

Example 2: Swap without a temporary variable

```python
a = 10
b = 20

a, b = b, a

print(a, b)  # 20 10
```

What to notice:
- Python packs values on the right-hand side and unpacks them on the left.
- This is one of the most common tuple-powered patterns in Python code.

Example 3: Return multiple values

```python
def min_and_max(values):
    return min(values), max(values)

low, high = min_and_max([8, 3, 11, 5])
print(low, high)  # 3 11
```

What to notice:
- The function returns one tuple object.
- Unpacking makes the call site clean and readable.

Example 4: Tuple as a dictionary key

```python
locations = {
    ("ap-south-1", "primary"): "Mumbai",
    ("us-east-1", "primary"): "N. Virginia",
}

print(locations[("ap-south-1", "primary")])  # Mumbai
```

What to notice:
- Tuples work well when the key is naturally a combination of fields.
- This only works because the tuple elements are hashable strings.

Example 5: Immutability is shallow, not deep

```python
record = ([1, 2], "active")
record[0].append(3)

print(record)  # ([1, 2, 3], 'active')
```

What to notice:
- The tuple did not change shape.
- But the mutable list inside the tuple changed successfully.

Example 6: Constant folding with tuple literals

```python
import dis

def use_tuple():
    return (1, 2, 3)

def use_list():
    return [1, 2, 3]

dis.dis(use_tuple)
print(use_tuple.__code__.co_consts)
dis.dis(use_list)
```

What to notice:
- The tuple literal appears in the function constants.
- The list literal is built at runtime because lists are mutable.

#### Common Patterns
- Use tuples for fixed records such as coordinates, RGB values, and `(host, port)` pairs.
- Use tuple unpacking to return multiple values cleanly from a function.
- Use tuples as dictionary keys when the lookup key is composite.
- Use tuples for read-only configuration values that should not be modified accidentally.
- Prefer tuples over lists when the sequence is stable and memory sensitivity matters.

#### Pitfalls to Avoid
- Assuming a tuple is deeply immutable even when it contains lists, dicts, or sets.
- Forgetting the trailing comma in a single-element tuple.
- Using a tuple as a dictionary key when one of its elements is unhashable.
- Choosing a tuple when you actually need frequent appends or deletes.
- Overstating constant folding: only tuples made from compile-time constants can be folded safely.

#### Quick Recap
- Tuples are fixed-size immutable sequences.
- They are usually smaller than lists because they do not over-allocate for growth.
- Their immutability enables safe hashing and compiler optimizations like constant folding for literal constants.
- Packing and unpacking make swaps and multi-value returns natural.
- Tuple immutability is shallow, so nested mutable objects can still change.

#### Interview Sound Bite
A tuple is Python's lightweight immutable sequence, so I use it for fixed data, composite keys, and function returns when I want lower overhead and hashability compared with a list.

#### Memory Hook
Tuple = sealed list. Fixed shape, smaller shell, safer key.

#### Practice Questions
1. Why does a tuple usually take less memory than a list with the same elements?
2. Why can a tuple be used as a dictionary key but a list cannot?
3. What is the difference between `(5)` and `(5,)`?
4. How does Python return multiple values from a function?
5. Why can Python constant-fold tuple literals more safely than list literals?

#### Practice Answers
1. A tuple usually takes less memory because it has a fixed size and does not reserve extra capacity for future growth like a list does.
2. A tuple can be used as a dictionary key when all of its elements are hashable, because its immutable structure makes its hash stable. A list is mutable, so it is unhashable.
3. `(5)` is just the integer `5`, while `(5,)` is a one-element tuple. The comma is what creates the tuple.
4. Python returns multiple values by packing them into a tuple and then optionally unpacking that tuple at the call site.
5. Python can constant-fold tuple literals made only from constants because they cannot be mutated later, while list literals are mutable and must usually be created fresh at runtime.

---

### Topic 4: Strings
Status: In Progress

#### Concept in One Line
A Python string is an immutable sequence of Unicode text, so it is safe to share and hash, but repeated rebuilding creates new objects and gets expensive.

#### Mental Model
Think of a string as printed text on paper. You can read it, slice it, or compare it, but you cannot erase one character in place. Any "change" means creating a new piece of paper with the updated text.

#### Memory Behavior
- Python 3 `str` stores Unicode text, not raw bytes.
- `bytes` is a separate type used for encoded binary data such as UTF-8 bytes from a file or network.
- CPython uses a flexible internal Unicode representation, so ASCII-only strings can be stored more compactly than strings containing wider Unicode characters.
- Because strings are immutable, Python can cache their hash and safely use them as dictionary keys and set members.
- CPython may intern some strings, meaning equal strings can share one object in memory, especially for literals and identifier-like values.
- Operations such as concatenation and slicing generally create new string objects because the original string cannot change in place.

#### Key Behaviors and Gotchas
- Strings are immutable, so `s[0] = "P"` raises `TypeError`.
- `+` and `+=` create new strings rather than modifying the old one.
- Repeated string building in a loop is a common anti-pattern because each step copies data again.
- `"".join(parts)` is the preferred idiom when combining many pieces into one string.
- Use `==` for value comparison, not `is`; interning can make `is` appear to work sometimes, but it is not reliable.
- Indexing returns a one-character string, not a separate `char` type.
- `len(s)` counts Unicode code points, not encoded bytes and not always what a human would perceive as visual characters.

#### Time Complexity Notes
- `len(s)`: O(1)
- Index access: O(1)
- Slice of length `k`: O(k)
- Concatenation `a + b`: O(len(a) + len(b))
- `"".join(parts)`: O(total output length)
- Character membership (`ch in s`): O(n)
- Repeated `+=` over many pieces: often O(n^2) total work because earlier content gets copied repeatedly

#### Examples
Example 1: Immutability means "updates" create a new string

```python
word = "py"
alias = word
word += "thon"

print(alias)  # py
print(word)   # python
```

What to notice:
- The original string did not change in place.
- `word += "thon"` created a new string object and rebound `word`.

Example 2: String building anti-pattern

```python
parts = ["sys", "tem", "de", "sign"]

result = ""
for part in parts:
    result += part

print(result)  # systemdesign
```

What to notice:
- This works, but every loop step creates another string.
- For many pieces, the repeated copying becomes wasteful.

Example 3: `join` idiom

```python
parts = ["sys", "tem", "de", "sign"]
result = "".join(parts)

print(result)  # systemdesign
```

What to notice:
- `join` is the standard way to build one string from many pieces.
- It avoids the repeated rebuild pattern from `+=` in a loop.

Example 4: Interning with `sys.intern()`

```python
import sys

a = "".join(["data", "_", "pipeline"])
b = "".join(["data", "_", "pipeline"])

print(a == b)  # True
print(a is b)  # usually False

a = sys.intern(a)
b = sys.intern(b)

print(a is b)  # True
```

What to notice:
- Equal strings can be forced to share one canonical object with `sys.intern()`.
- This is an optimization technique, not a replacement for `==`.

Example 5: Unicode model: code points are not the same as bytes

```python
text = "A😊"

print(len(text))                 # 2
print(text.encode("utf-8"))      # b'A...'
print(len(text.encode("utf-8"))) # 5
```

What to notice:
- The string has two Unicode characters.
- Its UTF-8 encoded byte representation uses more than two bytes.

Example 6: Visually similar text can have different internal forms

```python
composed = "é"
decomposed = "e\u0301"

print(len(composed))    # 1
print(len(decomposed))  # 2
print(composed == decomposed)  # False
```

What to notice:
- Both values may look similar when printed.
- Unicode text can have multiple representations, which matters in comparison and normalization.

Example 7: Slicing tricks

```python
s = "abcdef"

print(s[:3])   # abc
print(s[3:])   # def
print(s[-3:])  # def
print(s[::2])  # ace
print(s[::-1]) # fedcba
```

What to notice:
- Slicing is concise for prefix, suffix, stride, and reverse operations.
- Each slice produces a new string value.

#### Common Patterns
- Use strings for text data and `bytes` for encoded or binary data.
- Build large strings by collecting pieces in a list and calling `"".join(...)`.
- Use f-strings for readable formatting when combining a small number of values.
- Use strings naturally as dictionary keys because they are immutable and hashable.
- Use slicing for fast prefix, suffix, and reverse-style operations on simple text.
- Use `sys.intern()` only in specialized cases such as parsers, token-heavy workloads, and repeated identifier storage.

#### Pitfalls to Avoid
- Building long strings with repeated `+=` inside loops.
- Using `is` for string comparison because interning made it "seem" correct in a test.
- Confusing text length with byte length.
- Assuming `len(s)` always matches what a human sees as one visual character.
- Treating Unicode normalization issues as rare when text comes from multiple systems or user inputs.
- Reversing complex user-facing Unicode text with naive slicing when grapheme clusters matter.

#### Quick Recap
- Strings are immutable Unicode text objects.
- Immutability makes them hashable and safe to share, but any apparent modification creates a new string.
- Interning lets Python reuse equal strings in some cases to save memory and speed comparisons.
- `join` is the right tool for combining many string pieces efficiently.
- Unicode means characters, bytes, and visible glyphs are related but not identical concepts.

#### Interview Sound Bite
A Python string is an immutable Unicode object, so I treat it as read-only text, use `join` instead of repeated `+=` for heavy construction, and remember that interning and Unicode representation affect memory behavior and comparison edge cases.

#### Memory Hook
String = immutable Unicode text. Join, do not grow.

#### Practice Questions
1. Why is repeated `+=` on strings inside a loop considered an anti-pattern?
2. What is string interning and when is it useful?
3. Why should you use `==` instead of `is` for string comparison?
4. What is the difference between `str` and `bytes` in Python 3?
5. Why can `len()` be surprising for Unicode text?

#### Practice Answers
1. Repeated `+=` is an anti-pattern because strings are immutable, so each concatenation creates a new string and copies old content again, which can lead to quadratic total work.
2. String interning is the practice of reusing one shared object for equal strings. It is useful in specialized workloads such as parsers, compilers, and systems that repeatedly store the same identifiers or tokens.
3. You should use `==` because it compares string values. `is` checks object identity, and interning can make identity appear equal sometimes even when that behavior is not guaranteed.
4. `str` represents Unicode text, while `bytes` represents raw encoded binary data. You decode bytes into strings and encode strings into bytes.
5. `len()` counts Unicode code points, not encoded bytes and not always the number of user-perceived visual characters, so text with emojis or combining marks can be surprising.

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
