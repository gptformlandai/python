# Module 4 - Mastery Exercises

## Purpose
This file is the single source of truth for Module 4.
We are switching from theory-first learning to coding-pattern practice.

The runnable companion file is [module_4_practice.py](module_4_practice.py).

The goal is not only to solve each problem, but to train this habit:
- identify the workload shape
- choose the right data structure
- write clean code
- explain the gotchas
- compare what we first think with what the problem actually needs
- separate good practice from bad practice

Estimated total: ~7 hours 30 min

---

## Topics Covered in This Module
- Exercise 1: Frequency counter
- Exercise 2: Anagram groups
- Exercise 3: LRU cache simulation
- Exercise 4: Flatten arbitrarily nested list
- Exercise 5: Sliding window maximum
- Exercise 6: Two-sum / Three-sum
- Exercise 7: Invert and merge dicts
- Exercise 8: Matrix transpose
- Exercise 9: Top-K frequent elements
- Exercise 10: Deduplicate preserving insertion order
- Exercise 11: Intersection of N lists
- Exercise 12: Word frequency report
- Exercise 13: Graph as adjacency dict
- Exercise 14: Caesar cipher
- Exercise 15: Leaderboard

---

## Module 4 Coding Workflow
Use this workflow for every exercise.

1. Restate the input and output.
2. Ask: do I need count, lookup, order, uniqueness, grouping, windowing, or ranking?
3. Pick the structure based on the operation, not based on habit.
4. Write the simplest correct version.
5. Test empty input, one item, duplicates, and tie cases.
6. State time and space complexity.
7. Name the gotcha that could break the solution.

---

## What We Are Reusing From Modules 1-3

| Earlier Learning | Used In Module 4 |
|------------------|------------------|
| Variables hold references | Avoid accidental mutation and understand shallow output containers |
| List dynamic array behavior | Avoid `pop(0)` and front inserts in hot paths |
| Tuple immutability | Use tuples as stable dict/set keys, especially for grouped signatures |
| String immutability | Build strings with `join()` instead of repeated `+=` |
| Dict hash table | Fast lookup, counting, indexing, and merging |
| Set hash table | Fast membership, deduplication, and intersection |
| Slicing copies | Avoid hidden O(n) copies in tight loops |
| Comprehensions | Clean transform/filter code when the logic is simple |
| Unpacking | Clean tuple/list/edge processing and function calls |
| Counter | Counting, frequency ranking, top-N |
| defaultdict | Grouping and graph adjacency lists |
| deque | Queues and sliding windows |
| dataclass/namedtuple | Readable structured records |
| sorted/key functions | Ranking, tie-breaking, deterministic reports |

---

## Pattern Recognition Cheat Sheet

| Problem Signal | First Structure To Consider | Why |
|----------------|-----------------------------|-----|
| Count items | `Counter` or `dict` | One pass, direct count update |
| Group items | `defaultdict(list)` | Avoid manual key initialization |
| Fast membership | `set` | Average O(1) membership |
| Keyed lookup | `dict` | Average O(1) lookup by key |
| Preserve insertion order while deduping | `dict.fromkeys()` or `seen` set plus list | Keep first occurrence |
| Queue behavior | `deque` | O(1) append/pop from both ends |
| Sliding window | `deque` | Track active window efficiently |
| Top K | `heapq` or `Counter.most_common()` | Avoid full sort when K is small |
| Ranking with rules | `sorted(..., key=...)` | Explicit tie-breaking |
| Nested traversal | recursion or stack | Process unknown depth |
| Fixed structured record | `dataclass` or `namedtuple` | Clear field names |

---

## Good Practices For This Module
- Prefer the structure that matches the operation: lookup means dict/set, grouping means defaultdict, queue means deque.
- Make tie-breaking explicit when output order matters.
- Keep input mutation intentional. If you sort input, either document it or sort a copy.
- Use small helper functions when one problem has two ideas, such as parsing plus ranking.
- Use names that describe roles: `counts`, `groups`, `seen`, `window`, `left`, `right`, `ranked`.
- Write tests for edge cases before trusting the main example.
- State complexity after coding, not before thinking through hidden copies.

## Bad Practices To Avoid
- Using `list.count()` inside a loop for frequency work. That turns counting into O(n^2).
- Using a list for repeated membership checks when a set would fit.
- Using `pop(0)` for queues.
- Writing dense comprehensions when the logic needs branching or explanation.
- Sorting the full dataset when only top K is needed and K is small.
- Forgetting that dict inversion can lose data when values repeat.
- Accidentally depending on set output order.
- Rebuilding expensive structures inside a loop instead of building once.

---

## Exercise Notes

### Exercise 1: Frequency Counter
Status: Ready for Practice

#### Coding Pattern
Count each item as you scan the data once.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "For each word, scan the whole list and count it." | Build one frequency table in one pass. |
| "Counting needs manual if/else every time." | `Counter` already models this pattern. |

#### Runnable Reference Solution
```python
from collections import Counter


def frequency_counter(items):
    return Counter(items)


words = ["python", "data", "python", "code", "data", "python"]
counts = frequency_counter(words)

print(counts)
print(counts["python"])
print(counts["missing"])
```

#### What We Used From Earlier Modules
- Dict-style hash lookup for item counts.
- `Counter` from collections.
- One-pass O(n) thinking from Big-O.

#### Minute Gotchas
- `Counter` returns `0` for a missing key, while a normal dict raises `KeyError`.
- `Counter` keys must be hashable.
- `items.count(x)` inside a loop looks simple but usually becomes O(n^2).

#### Good Practice
Use `Counter` when the problem is pure frequency counting.

#### Bad Practice
Do not write this for large input:

```python
def bad_frequency_counter(items):
    return {item: items.count(item) for item in items}
```

#### Complexity
- Time: O(n)
- Space: O(u), where `u` is the number of unique items

---

### Exercise 2: Anagram Groups
Status: Ready for Practice

#### Coding Pattern
Convert each word into a canonical signature, then group words by that signature.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Compare every word with every other word." | Build the same key for anagrams and group by key. |
| "Anagram checking is a pair problem." | Anagram grouping is a dictionary grouping problem. |

#### Runnable Reference Solution
```python
from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)

    for word in words:
        signature = "".join(sorted(word.lower()))
        groups[signature].append(word)

    return list(groups.values())


words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group_anagrams(words))
```

#### What We Used From Earlier Modules
- Dict keys must be hashable.
- Strings are immutable and sortable into a stable signature.
- `defaultdict(list)` removes manual list initialization.
- Sorting produces a comparable normalized form.

#### Minute Gotchas
- `sorted(word)` returns a list of characters, so use `"".join(...)` to make a string key.
- Sorting each word costs O(k log k), where `k` is word length.
- Lowercasing is a business rule. If case matters, remove `.lower()`.

#### Good Practice
Use a canonical key such as sorted letters or a tuple of character counts.

#### Bad Practice
Do not compare every pair of words unless the input is tiny.

#### Complexity
- Time: O(n * k log k)
- Space: O(n * k), because grouped words are stored

---

### Exercise 3: LRU Cache Simulation
Status: Ready for Practice

#### Coding Pattern
Combine fast lookup with recency order.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "A cache is just a dict." | LRU also needs ordering by recent use. |
| "Updating a key only changes the value." | In LRU, updating a key should also refresh recency. |

#### Runnable Reference Solution
```python
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None

        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


lru = LRUCache(capacity=2)
lru.put("a", 1)
lru.put("b", 2)
print(lru.get("a"))
lru.put("c", 3)
print(lru.get("b"))
print(lru.get("c"))
```

#### What We Used From Earlier Modules
- Dict lookup for O(1) access.
- Insertion/order behavior.
- Mutability and in-place updates.
- Collections module specialized tools.

#### Minute Gotchas
- A normal dict preserves insertion order, but it does not expose `move_to_end()`.
- `get()` must update recency, not only return the value.
- `popitem(last=False)` removes the least recently used item from the front.

#### Good Practice
Use `OrderedDict` when the code needs explicit order manipulation.

#### Bad Practice
Do not scan a list of keys on every access for an LRU cache.

#### Complexity
- `get`: O(1)
- `put`: O(1)
- Space: O(capacity)

---

### Exercise 4: Flatten Arbitrarily Nested List
Status: Ready for Practice

#### Coding Pattern
Use recursion when the same problem appears inside itself.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "A nested list can be flattened with one loop." | Arbitrary nesting needs repeated descent. |
| "`sum(nested, [])` is a clever shortcut." | It only handles shallow cases well and can be inefficient. |

#### Runnable Reference Solution
```python
def flatten(items):
    result = []

    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)

    return result


data = [1, [2, 3], [4, [5, 6]], 7]
print(flatten(data))
```

#### What We Used From Earlier Modules
- Lists store references.
- `append()` adds one object.
- `extend()` adds items from an iterable.
- Recursion plus list accumulation.

#### Minute Gotchas
- `append(flatten(item))` would create nested lists again.
- `extend(flatten(item))` merges the returned flat values.
- This version treats only lists as nestable. Tuples are left as values unless you expand the condition.
- Very deep nesting can hit Python's recursion limit.

#### Good Practice
Use a clear recursive function first. Optimize with an explicit stack only if depth becomes a real problem.

#### Bad Practice
Avoid `sum(nested_lists, [])` for serious flattening work.

#### Complexity
- Time: O(n), where `n` is total atomic values plus list containers visited
- Space: O(n) for output, plus recursion stack depth

---

### Exercise 5: Sliding Window Maximum
Status: Ready for Practice

#### Coding Pattern
Maintain a deque of candidate indices in decreasing value order.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "For each window, call `max(window)`." | Keep the maximum candidate alive as the window moves. |
| "A deque stores the window values." | The stronger pattern stores indices so stale values can be removed. |

#### Runnable Reference Solution
```python
from collections import deque


def sliding_window_max(nums, window_size):
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if window_size > len(nums):
        return []

    candidates = deque()
    result = []

    for right, value in enumerate(nums):
        while candidates and candidates[0] <= right - window_size:
            candidates.popleft()

        while candidates and nums[candidates[-1]] <= value:
            candidates.pop()

        candidates.append(right)

        if right >= window_size - 1:
            result.append(nums[candidates[0]])

    return result


nums = [1, 3, -1, -3, 5, 3, 6, 7]
print(sliding_window_max(nums, 3))
```

#### What We Used From Earlier Modules
- `deque` gives O(1) pops from both ends.
- List indexing gives O(1) access to values by index.
- Big-O reasoning avoids O(n * k).

#### Minute Gotchas
- Store indices, not values, so you can remove elements that leave the window.
- The deque is not the full window. It is only the useful maximum candidates.
- The `<=` in the second while loop removes older duplicates and keeps the newer duplicate.

#### Good Practice
Use a monotonic deque when each window needs a max or min.

#### Bad Practice
Do not slice each window and call `max()` for large inputs.

#### Complexity
- Time: O(n), because each index enters and leaves the deque at most once
- Space: O(k), where `k` is window size

---

### Exercise 6: Two-Sum / Three-Sum
Status: Ready for Practice

#### Coding Pattern
Use lookup for two-sum. Use sorting plus two pointers for unique three-sum triples.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Try all pairs or triples." | Use stored complements for pairs and ordered movement for triples. |
| "Sorting is only for output." | Sorting can create structure that makes pointer movement possible. |

#### Runnable Reference Solution
```python
def two_sum(nums, target):
    seen = {}

    for index, num in enumerate(nums):
        needed = target - num
        if needed in seen:
            return seen[needed], index
        seen[num] = index

    return None


def three_sum_zero(nums):
    nums = sorted(nums)
    triples = []

    for index, value in enumerate(nums):
        if index > 0 and value == nums[index - 1]:
            continue

        left = index + 1
        right = len(nums) - 1

        while left < right:
            total = value + nums[left] + nums[right]

            if total == 0:
                triples.append((value, nums[left], nums[right]))
                left += 1
                right -= 1

                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return triples


print(two_sum([2, 7, 11, 15], 9))
print(three_sum_zero([-1, 0, 1, 2, -1, -4]))
```

#### What We Used From Earlier Modules
- Dict membership for complement lookup.
- Sorting with `sorted()` to avoid mutating the original input.
- Tuples as immutable result records.
- Loop control and duplicate handling.

#### Minute Gotchas
- In two-sum, check the complement before storing the current value so you do not reuse the same index.
- In three-sum, skip duplicates at the fixed index and after finding a valid triple.
- Sorting changes index positions, so three-sum returns values, not original indices.

#### Good Practice
Use a dict for two-sum indices and sorted two-pointer logic for unique three-sum values.

#### Bad Practice
Do not jump straight to triple nested loops unless the input size is guaranteed tiny.

#### Complexity
- Two-sum time: O(n), space: O(n)
- Three-sum time: O(n^2), space: O(n) for the sorted copy and output

---

### Exercise 7: Invert and Merge Dicts
Status: Ready for Practice

#### Coding Pattern
Invert only when values are safe keys. Merge with explicit overwrite rules.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Inverting a dict is just swapping key and value." | Duplicate values can collapse multiple keys into one. |
| "Merging is always harmless." | Later values overwrite earlier ones for matching keys. |

#### Runnable Reference Solution
```python
from collections import defaultdict


def invert_one_to_one(mapping):
    return {value: key for key, value in mapping.items()}


def invert_grouped(mapping):
    inverted = defaultdict(list)

    for key, value in mapping.items():
        inverted[value].append(key)

    return dict(inverted)


def merge_with_override(base, updates):
    return base | updates


codes = {"python": "py", "pytest": "py", "javascript": "js"}
print(invert_one_to_one(codes))
print(invert_grouped(codes))
print(merge_with_override({"debug": False, "port": 8000}, {"debug": True}))
```

#### What We Used From Earlier Modules
- Dict comprehensions.
- `defaultdict(list)` for grouping duplicate values.
- Dict merge operator `|`.
- Hashability rules for dict keys.

#### Minute Gotchas
- `invert_one_to_one()` loses earlier keys when values repeat.
- Dict values must be hashable if they become keys after inversion.
- `base | updates` creates a new dict; `base |= updates` mutates `base`.

#### Good Practice
Use grouped inversion when duplicate values are possible.

#### Bad Practice
Do not silently invert a many-to-one mapping unless data loss is acceptable.

#### Complexity
- Time: O(n)
- Space: O(n)

---

### Exercise 8: Matrix Transpose
Status: Ready for Practice

#### Coding Pattern
Use unpacking with `zip()` to group columns.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Transpose needs manual nested indexing." | `zip(*matrix)` already groups column-wise values. |
| "`zip()` gives lists." | `zip()` yields tuples lazily. Convert if you need lists. |

#### Runnable Reference Solution
```python
def transpose(matrix):
    if not matrix:
        return []

    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("all rows must have the same length")

    return [list(column) for column in zip(*matrix)]


matrix = [
    [1, 2, 3],
    [4, 5, 6],
]

print(transpose(matrix))
```

#### What We Used From Earlier Modules
- Unpacking with `*matrix`.
- List comprehension for clean transformation.
- `zip()` for aligned grouping.
- Edge-case checking before relying on structure.

#### Minute Gotchas
- `zip(*matrix)` truncates to the shortest row if the matrix is ragged.
- `zip()` returns tuples, so convert columns to lists if the expected output is list-of-lists.
- `*matrix` expands rows into separate arguments to `zip()`.

#### Good Practice
Validate row lengths when ragged input would be a bug.

#### Bad Practice
Do not rely on silent truncation unless that behavior is explicitly desired.

#### Complexity
- Time: O(rows * columns)
- Space: O(rows * columns) for the transposed output

---

### Exercise 9: Top-K Frequent Elements
Status: Ready for Practice

#### Coding Pattern
Count first, then select the K highest counts.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Sort the original list." | Sort or heap-select the unique items by count. |
| "Top K means I always need a full sort." | A heap can be better when K is much smaller than unique items. |

#### Runnable Reference Solution
```python
from collections import Counter
import heapq


def top_k_frequent(items, k):
    if k <= 0:
        return []

    counts = Counter(items)
    return heapq.nlargest(k, counts, key=counts.get)


items = ["py", "js", "py", "java", "py", "js", "go"]
print(top_k_frequent(items, 2))
```

#### What We Used From Earlier Modules
- `Counter` for frequency table creation.
- Dict-like lookup with `counts.get` as a key function.
- `heapq` for top-K selection.

#### Minute Gotchas
- If tie order matters, define it explicitly. Heap output for equal keys should not be treated as a business rule.
- If `k` is bigger than the number of unique items, `nlargest()` returns all unique items.
- For simple frequency reports, `Counter.most_common(k)` is often clearer.

#### Good Practice
Use `Counter.most_common(k)` for clarity, or `heapq` when you want to practice the selection pattern.

#### Bad Practice
Do not sort every raw item when you only need ranked unique items.

#### Complexity
- Counting time: O(n)
- Heap selection time: O(u log k), where `u` is unique item count
- Space: O(u)

---

### Exercise 10: Deduplicate Preserving Insertion Order
Status: Ready for Practice

#### Coding Pattern
Track what you have seen while appending only first occurrences.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Use a set to remove duplicates." | A set removes duplicates but does not promise the original order as output. |
| "Deduplication is just uniqueness." | Sometimes the first-seen order is part of correctness. |

#### Runnable Reference Solution
```python
def dedupe_preserve_order(items):
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


def dedupe_hashable_fast(items):
    return list(dict.fromkeys(items))


values = ["a", "b", "a", "c", "b", "d"]
print(dedupe_preserve_order(values))
print(dedupe_hashable_fast(values))
```

#### What We Used From Earlier Modules
- Set membership for O(1) average lookup.
- List append for preserving order.
- Dict insertion-order guarantee.

#### Minute Gotchas
- Both versions require hashable items.
- `list(set(items))` loses original order.
- `dict.fromkeys(items)` keeps first occurrence order in modern Python.

#### Good Practice
Use `dict.fromkeys()` for a concise hashable-items solution, and use the explicit loop when you need more control.

#### Bad Practice
Do not use a set-only conversion when output order matters.

#### Complexity
- Time: O(n)
- Space: O(u)

---

### Exercise 11: Intersection of N Lists
Status: Ready for Practice

#### Coding Pattern
Convert each list to a set and repeatedly intersect.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Check each item against every list manually." | Turn membership into set operations. |
| "Intersection output is naturally ordered." | Set intersection gives a set, which is not an ordered report. |

#### Runnable Reference Solution
```python
def intersection_all(lists):
    iterator = iter(lists)

    try:
        first = next(iterator)
    except StopIteration:
        return set()

    common = set(first)

    for values in iterator:
        common &= set(values)

    return common


def intersection_preserve_first_order(lists):
    if not lists:
        return []

    common = intersection_all(lists)
    result = []
    emitted = set()

    for item in lists[0]:
        if item in common and item not in emitted:
            result.append(item)
            emitted.add(item)

    return result


data = [[1, 2, 2, 3, 4], [2, 4, 6], [0, 2, 4, 8]]
print(intersection_all(data))
print(intersection_preserve_first_order(data))
```

#### What We Used From Earlier Modules
- Set algebra.
- Fast membership.
- Iterator use to avoid slicing `lists[1:]`.

#### Minute Gotchas
- Set intersection removes duplicates.
- Set output order should not be used as meaningful order.
- If duplicate counts matter, this becomes a Counter problem, not a plain set problem.

#### Good Practice
Return a set when uniqueness is enough. Return a list when order is part of the requirement.

#### Bad Practice
Do not use repeated list membership checks for large inputs.

#### Complexity
- Time: O(total number of values across lists)
- Space: O(size of converted sets)

---

### Exercise 12: Word Frequency Report
Status: Ready for Practice

#### Coding Pattern
Normalize text, count words, sort by clear ranking rules.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Just split by spaces." | Real text needs normalization and punctuation handling. |
| "Frequency sorting is enough." | Ties need deterministic rules for clean reports. |

#### Runnable Reference Solution
```python
from collections import Counter
import re


def word_frequency_report(text, limit=None):
    words = re.findall(r"[a-z0-9']+", text.lower())
    counts = Counter(words)
    rows = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))

    if limit is not None:
        rows = rows[:limit]

    return rows


text = "Python, python! Data structures: data, code, and Python."
print(word_frequency_report(text))
print(word_frequency_report(text, limit=2))
```

#### What We Used From Earlier Modules
- String normalization.
- `Counter` for counting.
- `sorted()` with a tuple key.
- Slicing for optional limit.

#### Minute Gotchas
- Plain `split()` keeps punctuation attached, such as `"python!"`.
- Sorting by `(-count, word)` gives highest frequency first and alphabetical tie-break second.
- `rows[:limit]` creates a slice copy, which is fine for small reports but still O(limit).

#### Good Practice
Make normalization and tie-breaking visible in the code.

#### Bad Practice
Do not hide punctuation and case assumptions inside unexplained output.

#### Complexity
- Tokenization and counting: O(n)
- Sorting unique words: O(u log u)
- Space: O(u)

---

### Exercise 13: Graph as Adjacency Dict
Status: Ready for Practice

#### Coding Pattern
Represent each node as a key and its neighbors as a list or set.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "A graph needs a special class first." | Many graph problems start cleanly with a dict of neighbors. |
| "BFS can use a list queue." | A real queue should use `deque` to avoid O(n) front pops. |

#### Runnable Reference Solution
```python
from collections import defaultdict, deque


def build_graph(edges, directed=False):
    graph = defaultdict(list)

    for source, target in edges:
        graph[source].append(target)
        graph.setdefault(target, [])

        if not directed:
            graph[target].append(source)

    return dict(graph)


def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
graph = build_graph(edges)
print(graph)
print(bfs(graph, "A"))
```

#### What We Used From Earlier Modules
- `defaultdict(list)` for grouping neighbors.
- Sets for visited membership.
- `deque` for queue behavior.
- Tuple unpacking for edges.

#### Minute Gotchas
- Accessing a missing key in a `defaultdict` creates that key. Use `.get()` when you do not want mutation.
- Use a neighbor set instead of a list if duplicate edges must collapse.
- For directed graphs, do not add the reverse edge.

#### Good Practice
Choose `list` neighbors when order and duplicates matter; choose `set` neighbors when uniqueness matters.

#### Bad Practice
Do not use `queue.pop(0)` for BFS on large graphs.

#### Complexity
- Build graph time: O(E)
- BFS time: O(V + E)
- Space: O(V + E)

---

### Exercise 14: Caesar Cipher
Status: Ready for Practice

#### Coding Pattern
Build a character mapping, then transform the string with `join()`.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "String encryption means changing characters in place." | Strings are immutable, so build a new string. |
| "Repeated `+=` is fine for text building." | `join()` is the standard pattern for repeated string assembly. |

#### Runnable Reference Solution
```python
import string


def build_caesar_map(shift):
    alphabet = string.ascii_lowercase
    shift = shift % 26
    shifted = alphabet[shift:] + alphabet[:shift]

    lower_map = dict(zip(alphabet, shifted))
    upper_map = {key.upper(): value.upper() for key, value in lower_map.items()}

    return lower_map | upper_map


def caesar_encrypt(text, shift):
    cipher = build_caesar_map(shift)
    return "".join(cipher.get(char, char) for char in text)


print(caesar_encrypt("Attack at Dawn!", 3))
print(caesar_encrypt("Dwwdfn dw Gdzq!", -3))
```

#### What We Used From Earlier Modules
- Dict mapping for character transformation.
- String slicing and concatenation for shifted alphabet.
- Dict comprehension for uppercase map.
- `join()` for efficient string building.
- `dict.get()` for safe fallback.

#### Minute Gotchas
- `shift % 26` makes large and negative shifts work.
- Non-letter characters are preserved through `cipher.get(char, char)`.
- This implementation handles ASCII letters, not every Unicode alphabet.

#### Good Practice
Use a mapping plus `join()` when transforming characters one by one.

#### Bad Practice
Do not repeatedly concatenate to the same string inside a long loop.

#### Complexity
- Time: O(n), where `n` is text length
- Space: O(n) for the encrypted output

---

### Exercise 15: Leaderboard
Status: Ready for Practice

#### Coding Pattern
Model records clearly, then rank with explicit sort keys.

#### What We Think vs What It Actually Is
| What We Think | What It Actually Is |
|---------------|---------------------|
| "Leaderboard means sort by score only." | Real ranking needs tie-break rules. |
| "Top players always need full sorting." | Full ranking needs sort; top K can use a heap. |

#### Runnable Reference Solution
```python
from dataclasses import dataclass
import heapq


@dataclass(frozen=True)
class Score:
    player: str
    points: int
    wins: int = 0


def leaderboard(scores):
    return sorted(scores, key=lambda score: (-score.points, -score.wins, score.player))


def top_players(scores, k):
    if k <= 0:
        return []


    return heapq.nsmallest(
        k,
        scores,
        key=lambda score: (-score.points, -score.wins, score.player),
    )


scores = [
    Score("Maya", 90, 5),
    Score("Ana", 95, 3),
    Score("Bob", 95, 4),
    Score("Dev", 90, 6),
]

print(leaderboard(scores))
print(top_players(scores, 2))
```

#### What We Used From Earlier Modules
- `dataclass` for readable structured records.
- `sorted()` with a multi-field key.
- Tuple key ordering.
- `heapq` for top-K selection.

#### Minute Gotchas
- Negative numeric values in the key create descending order for those fields.
- `score.player` stays positive/normal so names sort alphabetically ascending on ties.
- `sorted()` returns a new list; it does not mutate the original.
- `heapq.nsmallest()` works here because the best rank has the smallest key tuple.

#### Good Practice
Write ranking rules directly in the key so ties are predictable.

#### Bad Practice
Do not rely on the accidental order of equal scores.

#### Complexity
- Full leaderboard time: O(n log n)
- Top K time: O(n log k)
- Space: O(n) for sorted output, O(k) for heap selection internals

---

## Module 4 Progress Tracker

| Exercise | Status |
|----------|--------|
| 1. Frequency counter | Ready for Practice |
| 2. Anagram groups | Ready for Practice |
| 3. LRU cache simulation | Ready for Practice |
| 4. Flatten arbitrarily nested list | Ready for Practice |
| 5. Sliding window maximum | Ready for Practice |
| 6. Two-sum / Three-sum | Ready for Practice |
| 7. Invert and merge dicts | Ready for Practice |
| 8. Matrix transpose | Ready for Practice |
| 9. Top-K frequent elements | Ready for Practice |
| 10. Deduplicate preserving insertion order | Ready for Practice |
| 11. Intersection of N lists | Ready for Practice |
| 12. Word frequency report | Ready for Practice |
| 13. Graph as adjacency dict | Ready for Practice |
| 14. Caesar cipher | Ready for Practice |
| 15. Leaderboard | Ready for Practice |

---

## Module 4 Recap

The core move in Module 4 is pattern recognition.

- Counting problems usually want `Counter` or a dict.
- Grouping problems usually want `defaultdict(list)`.
- Membership problems usually want a set.
- Queue and window problems usually want `deque`.
- Ranking problems usually want `sorted()` with a clear key or `heapq` for top K.
- Duplicate handling must be explicit.
- Ordering requirements must be explicit.
- Input mutation must be explicit.

## Interview Sound Bite
I first identify the operation shape: count, group, lookup, uniqueness, queue, window, or ranking. Then I choose the Python structure that makes that operation cheap and readable, and I check edge cases like duplicates, ordering, mutation, and tie-breaking.

## Memory Hook
Problem signal first, data structure second, code third.