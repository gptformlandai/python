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
10. Practice questions

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

#### Practice Questions
1. Why does appending to one list affect another variable sometimes?
2. When should you use is instead of ==?
3. What changes when assignment happens for immutable objects?

---

### Topic 2: Lists - Internals
Status: Not Started

Notes: Pending.

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

Current module status: Not Started
