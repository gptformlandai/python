# Python Data Structures — Mastery Plan

---

## Module 1 — Theory & Memory Internals (~4 hrs)

### Topic 1: Python Object Model (45 min)
- `id()`, `is` vs `==`, reference counting, how assignment really works
- **Examples:** aliasing trap, copy vs reference, mutable default argument bug

### Topic 2: Lists — Internals (45 min)
- Dynamic array, over-allocation, `sys.getsizeof` growth curve
- **Examples:** append vs insert cost, list as stack, list as queue (and why it's bad)

### Topic 3: Tuples — Internals (30 min)
- Immutable, smaller memory footprint, constant folding
- **Examples:** swap without temp variable, return multiple values, tuple as dict key

### Topic 4: Strings (30 min)
- Immutable, interning, Unicode model
- **Examples:** string building anti-pattern, join idiom, slicing tricks

### Topic 5: Dicts — Hash Table Internals (60 min)
- Hashing, collision handling, insertion-order guarantee (3.7+), key constraints
- **Examples:** unhashable key errors, dict as dispatch table, counting frequencies

### Topic 6: Sets & Frozensets (30 min)
- Hash-based, no duplicates, set algebra, mutability variants
- **Examples:** deduplication, membership test speed vs list, finding common/unique elements

---

## Module 2 — Access, Mutation & Time Complexity (~3 hrs 15 min)

### Topic 7: Big-O Per Operation (45 min)
- O(1) vs O(n) for every structure, with timed proofs using `timeit`

### Topic 8: Slicing Deep Dive (30 min)
- Stride, negative index, copy semantics
- **Examples:** reverse a list, every-nth element, palindrome check

### Topic 9: List Patterns (45 min)
- Filtering, flattening, zipping, rotating
- **Examples:** remove duplicates preserving order, chunk a list into N parts, transpose a matrix

### Topic 10: Dict Patterns (45 min)
- Merge, invert, group-by, nested access safely
- **Examples:** invert a dict, group words by length, safe nested get, merge two dicts (3.9+ `|` operator)

### Topic 11: Set Patterns (30 min)
- Membership, deduplication, algebra
- **Examples:** find missing numbers, common friends problem, unique words in a document

---

## Module 3 — Power Idioms & Collections Module (~4 hrs 30 min)

### Topic 12: Comprehensions vs Loops vs map/filter (45 min)
- List, dict, and set comprehensions with benchmarks

### Topic 13: Dict & Set Comprehensions (30 min)
- Real data transformation examples

### Topic 14: Unpacking (30 min)
- `*rest`, starred assignment, nested unpacking
- **Examples:** first/last split, ignore middle values, unpack CSV row

### Topic 15: `collections.Counter` (30 min)
- Top-N, arithmetic on counters
- **Examples:** word frequency, most common character, anagram check

### Topic 16: `collections.defaultdict` (30 min)
- Auto-init, grouping
- **Examples:** group-by pattern, inverted index, graph adjacency list

### Topic 17: `collections.deque` (30 min)
- O(1) both ends, maxlen sliding window
- **Examples:** sliding window max, undo/redo buffer, BFS queue

### Topic 18: `collections.namedtuple` & `dataclasses` (30 min)
- Readable structured data without a full class

### Topic 19: Sorting Masterclass (45 min)
- `sorted()`, multi-key sort, custom objects, `functools.cmp_to_key`

---

## Module 4 — Mastery Exercises (~7 hrs 30 min)

| # | Problem | Structures Used | Time |
|---|---------|----------------|------|
| 1 | Frequency counter | dict + Counter | 30 min |
| 2 | Anagram groups | defaultdict | 30 min |
| 3 | LRU cache simulation | OrderedDict | 30 min |
| 4 | Flatten arbitrarily nested list | recursion + list | 30 min |
| 5 | Sliding window maximum | deque | 30 min |
| 6 | Two-sum / Three-sum | set + dict | 30 min |
| 7 | Invert and merge dicts | dict | 30 min |
| 8 | Matrix transpose | zip + list comprehension | 30 min |
| 9 | Top-K frequent elements | Counter + heap | 30 min |
| 10 | Deduplicate preserving insertion order | dict + set | 30 min |
| 11 | Intersection of N lists | set | 30 min |
| 12 | Word frequency report | Counter + sorted | 30 min |
| 13 | Graph as adjacency dict | defaultdict | 30 min |
| 14 | Caesar cipher | dict mapping | 30 min |
| 15 | Leaderboard | sorted + heapq | 30 min |

---

## Module 5 — Mini Project (~3 hrs 30 min)

### Topic 20: End-to-End Data Pipeline (3 hrs 30 min)
- Read a CSV → parse rows into dicts → validate with sets → aggregate with Counter/defaultdict → sort and report
- **Constraint:** built-in structures only, no pandas
- **Goal:** demonstrate all structures working together in a real workflow

---

## Time Estimates Per Topic

### Module 1 — Theory & Memory Internals (~4 hrs)

| Topic | Estimated Time |
|-------|---------------|
| Topic 1: Python Object Model | 45 min |
| Topic 2: Lists — Internals | 45 min |
| Topic 3: Tuples — Internals | 30 min |
| Topic 4: Strings | 30 min |
| Topic 5: Dicts — Hash Table Internals | 60 min |
| Topic 6: Sets & Frozensets | 30 min |
| **Module 1 Total** | **4 hrs** |

### Module 2 — Access, Mutation & Time Complexity (~3 hrs)

| Topic | Estimated Time |
|-------|---------------|
| Topic 7: Big-O Per Operation | 45 min |
| Topic 8: Slicing Deep Dive | 30 min |
| Topic 9: List Patterns | 45 min |
| Topic 10: Dict Patterns | 45 min |
| Topic 11: Set Patterns | 30 min |
| **Module 2 Total** | **3 hrs 15 min** |

### Module 3 — Power Idioms & Collections (~4.5 hrs)

| Topic | Estimated Time |
|-------|---------------|
| Topic 12: Comprehensions vs Loops vs map/filter | 45 min |
| Topic 13: Dict & Set Comprehensions | 30 min |
| Topic 14: Unpacking | 30 min |
| Topic 15: `collections.Counter` | 30 min |
| Topic 16: `collections.defaultdict` | 30 min |
| Topic 17: `collections.deque` | 30 min |
| Topic 18: `namedtuple` & `dataclasses` | 30 min |
| Topic 19: Sorting Masterclass | 45 min |
| **Module 3 Total** | **4 hrs 30 min** |

### Module 4 — Mastery Exercises (~7.5 hrs)

| Topic | Estimated Time |
|-------|---------------|
| 15 graded exercises × ~30 min each | 7 hrs 30 min |
| **Module 4 Total** | **7 hrs 30 min** |

### Module 5 — Mini Project (~3.5 hrs)

| Topic | Estimated Time |
|-------|---------------|
| Topic 20: End-to-End Data Pipeline | 3 hrs 30 min |
| **Module 5 Total** | **3 hrs 30 min** |

---

## Total Time Summary

| Module | Time |
|--------|------|
| Module 1 — Theory & Memory Internals | 4 hrs 00 min |
| Module 2 — Access, Mutation & Time Complexity | 3 hrs 15 min |
| Module 3 — Power Idioms & Collections | 4 hrs 30 min |
| Module 4 — Mastery Exercises | 7 hrs 30 min |
| Module 5 — Mini Project | 3 hrs 30 min |
| **Grand Total** | **~23 hrs** |

### Study Pace Guide

| Daily Commitment | Completion Time |
|-----------------|----------------|
| 1 hr / day | ~23 days |
| 1.5 hrs / day | ~16 days |
| 2 hrs / day | ~12 days |
| 3 hrs / day | ~8 days |

> Recommended pace: **1.5–2 hrs/day** — enough to absorb theory and run examples without burnout.

---

## Progress Tracker

| Module | Status |
|--------|--------|
| Module 1 — Theory & Memory Internals | Not Started |
| Module 2 — Access, Mutation & Time Complexity | Not Started |
| Module 3 — Power Idioms & Collections | Not Started |
| Module 4 — Mastery Exercises | Not Started |
| Module 5 — Mini Project | Not Started |
