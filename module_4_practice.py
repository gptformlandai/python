"""Runnable reference implementations for Module 4 mastery exercises.

Run with:
    python3 module_4_practice.py
"""

import re
import string
from collections import Counter, OrderedDict, defaultdict, deque
from heapq import nlargest


def frequency_counter(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def frequency_counter_with_counter(items):
    return Counter(items)


def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        signature = "".join(sorted(word.lower()))
        groups[signature].append(word)
    return list(groups.values())


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.items = OrderedDict()

    def get(self, key):
        if key not in self.items:
            return None
        self.items.move_to_end(key)
        return self.items[key]

    def put(self, key, value):
        if key in self.items:
            self.items.move_to_end(key)
        self.items[key] = value
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)

    def snapshot(self):
        return list(self.items.items())


def flatten_nested_list(items):
    flattened = []
    for item in items:
        if isinstance(item, list):
            flattened.extend(flatten_nested_list(item))
        else:
            flattened.append(item)
    return flattened


def sliding_window_max(numbers, window_size):
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if window_size > len(numbers):
        return []

    candidate_indices = deque()
    result = []

    for index, value in enumerate(numbers):
        while candidate_indices and candidate_indices[0] <= index - window_size:
            candidate_indices.popleft()

        while candidate_indices and numbers[candidate_indices[-1]] <= value:
            candidate_indices.pop()

        candidate_indices.append(index)

        if index >= window_size - 1:
            result.append(numbers[candidate_indices[0]])

    return result


def two_sum_indices(numbers, target):
    seen_indices = {}
    for index, value in enumerate(numbers):
        needed = target - value
        if needed in seen_indices:
            return seen_indices[needed], index
        seen_indices[value] = index
    return None


def three_sum_unique(numbers, target=0):
    sorted_numbers = sorted(numbers)
    triples = []

    for first_index in range(len(sorted_numbers) - 2):
        if first_index > 0 and sorted_numbers[first_index] == sorted_numbers[first_index - 1]:
            continue

        left_index = first_index + 1
        right_index = len(sorted_numbers) - 1

        while left_index < right_index:
            total = (
                sorted_numbers[first_index]
                + sorted_numbers[left_index]
                + sorted_numbers[right_index]
            )

            if total == target:
                triples.append(
                    (
                        sorted_numbers[first_index],
                        sorted_numbers[left_index],
                        sorted_numbers[right_index],
                    )
                )
                left_index += 1
                right_index -= 1

                while (
                    left_index < right_index
                    and sorted_numbers[left_index] == sorted_numbers[left_index - 1]
                ):
                    left_index += 1

                while (
                    left_index < right_index
                    and sorted_numbers[right_index] == sorted_numbers[right_index + 1]
                ):
                    right_index -= 1
            elif total < target:
                left_index += 1
            else:
                right_index -= 1

    return triples


def invert_unique(mapping):
    return {value: key for key, value in mapping.items()}


def invert_grouped(mapping):
    inverted = defaultdict(list)
    for key, value in mapping.items():
        inverted[value].append(key)
    return dict(inverted)


def merge_sum_dicts(*mappings):
    merged = {}
    for mapping in mappings:
        for key, value in mapping.items():
            merged[key] = merged.get(key, 0) + value
    return merged


def transpose_matrix(matrix):
    if not matrix:
        return []

    expected_width = len(matrix[0])
    if any(len(row) != expected_width for row in matrix):
        raise ValueError("matrix rows must have equal length")

    return [list(row) for row in zip(*matrix)]


def top_k_frequent(items, top_count):
    if top_count < 0:
        raise ValueError("top_count must be non-negative")

    counts = Counter(items)
    top_pairs = nlargest(top_count, counts.items(), key=lambda pair: pair[1])
    return [item for item, count in top_pairs]


def dedupe_preserve_order(items):
    return list(dict.fromkeys(items))


def dedupe_by_key(items, key_func):
    seen_keys = set()
    result = []

    for item in items:
        marker = key_func(item)
        if marker not in seen_keys:
            seen_keys.add(marker)
            result.append(item)

    return result


def intersection_unique(collections):
    collections = list(collections)
    if not collections:
        return set()

    common = set(collections[0])
    for values in collections[1:]:
        common &= set(values)

    return common


def intersection_preserve_first_order(collections):
    collections = list(collections)
    if not collections:
        return []

    common = intersection_unique(collections)
    result = []
    emitted = set()

    for value in collections[0]:
        if value in common and value not in emitted:
            result.append(value)
            emitted.add(value)

    return result


def word_frequency_report(text, top_count=None):
    words = re.findall(r"[a-z0-9']+", text.lower())
    counts = Counter(words)
    ordered = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))

    if top_count is None:
        return ordered
    return ordered[:top_count]


def build_undirected_graph(edges):
    graph = defaultdict(set)
    for left_node, right_node in edges:
        graph[left_node].add(right_node)
        graph[right_node].add(left_node)

    return {node: sorted(neighbors) for node, neighbors in graph.items()}


def bfs_order(graph, start):
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


def build_caesar_map(shift):
    letters = string.ascii_lowercase
    normalized_shift = shift % len(letters)
    mapping = {
        source: letters[(index + normalized_shift) % len(letters)]
        for index, source in enumerate(letters)
    }
    upper_mapping = {source.upper(): target.upper() for source, target in mapping.items()}
    mapping.update(upper_mapping)
    return mapping


def caesar_cipher(text, shift):
    mapping = build_caesar_map(shift)
    return "".join(mapping.get(character, character) for character in text)


def rank_leaderboard(players):
    ordered = sorted(
        players,
        key=lambda player: (-player["score"], player["time"], player["name"]),
    )

    ranked = []
    previous_score = None
    previous_rank = 0

    for position, player in enumerate(ordered, start=1):
        current_rank = previous_rank if player["score"] == previous_score else position
        ranked.append({**player, "rank": current_rank})
        previous_score = player["score"]
        previous_rank = current_rank

    return ranked


def top_players(players, top_count):
    return nlargest(top_count, players, key=lambda player: (player["score"], -player["time"]))


def normalize_groups(groups):
    return sorted(sorted(group) for group in groups)


def run_smoke_tests():
    assert frequency_counter(["a", "b", "a"]) == {"a": 2, "b": 1}
    assert dict(frequency_counter_with_counter(["a", "b", "a"])) == {"a": 2, "b": 1}

    anagrams = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert normalize_groups(anagrams) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]

    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.get("b") is None
    assert cache.snapshot() == [("a", 1), ("c", 3)]

    assert flatten_nested_list([1, [2, [3, 4], []], 5]) == [1, 2, 3, 4, 5]
    assert sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]

    assert two_sum_indices([2, 7, 11, 15], 9) == (0, 1)
    assert three_sum_unique([-1, 0, 1, 2, -1, -4]) == [(-1, -1, 2), (-1, 0, 1)]

    assert invert_unique({"py": "python", "js": "javascript"}) == {
        "python": "py",
        "javascript": "js",
    }
    assert invert_grouped({"a": 1, "b": 1, "c": 2}) == {1: ["a", "b"], 2: ["c"]}
    assert merge_sum_dicts({"a": 2, "b": 1}, {"a": 3, "c": 4}) == {
        "a": 5,
        "b": 1,
        "c": 4,
    }

    assert transpose_matrix([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert top_k_frequent(["a", "a", "a", "b", "b", "c"], 2) == ["a", "b"]

    assert dedupe_preserve_order(["py", "js", "py", "go", "js"]) == ["py", "js", "go"]
    assert dedupe_by_key(["Py", "py", "JS"], str.lower) == ["Py", "JS"]

    lists = [[1, 2, 2, 3, 4], [2, 4, 6], [0, 2, 4, 8]]
    assert intersection_unique(lists) == {2, 4}
    assert intersection_preserve_first_order(lists) == [2, 4]

    assert word_frequency_report("Python python data, data data!", 2) == [
        ("data", 3),
        ("python", 2),
    ]

    graph = build_undirected_graph([("a", "b"), ("a", "c"), ("b", "d")])
    assert graph == {"a": ["b", "c"], "b": ["a", "d"], "c": ["a"], "d": ["b"]}
    assert bfs_order(graph, "a") == ["a", "b", "c", "d"]

    assert caesar_cipher("Abc xyz!", 2) == "Cde zab!"

    players = [
        {"name": "Ana", "score": 100, "time": 50},
        {"name": "Bob", "score": 120, "time": 70},
        {"name": "Dia", "score": 120, "time": 65},
    ]
    ranked = rank_leaderboard(players)
    assert [player["name"] for player in ranked] == ["Dia", "Bob", "Ana"]
    assert [player["rank"] for player in ranked] == [1, 1, 3]
    assert [player["name"] for player in top_players(players, 2)] == ["Dia", "Bob"]

    print("All Module 4 smoke tests passed.")


if __name__ == "__main__":
    run_smoke_tests()