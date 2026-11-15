# repo2tools report: more-itertools-bench2

- Repo: https://github.com/more-itertools/more-itertools at `ceafee8ce96f4bc1eb74c528bc247c91d648a0bb`
- Package: `more_itertools`, 176 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 3.5 min. LLM tokens: 388,924 in 237 requests (propose 11,703, spec 151,771, code 225,450)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 59 (dropped: 62, for unknown functions, duplicates or bad names) |
| Accepted | 25 |
| Accepted and confirmed against a direct library call | 25 |
| Passed all checks on the first try | 14 |
| Rejected after the repair rounds | 34 |

First try, by the first check that failed: spec: 25, ok: 14, static: 6, runs: 6, differential: 5, fastmcp: 2, loads: 1.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `create_peekable_iterator` | `more_itertools.peekable` | 0 | 5 / 0 | yes |
| `split_into_chunks` | `more_itertools.chunked` | 0 | 5 / 0 | yes |
| `get_first_item` | `more_itertools.first` | 0 | 5 / 0 | yes |
| `get_last_item` | `more_itertools.last` | 1 | 5 / 0 | yes |
| `get_nth_item` | `more_itertools.nth` | 1 | 5 / 0 | yes |
| `peek_at_items` | `more_itertools.spy` | 0 | 5 / 0 | yes |
| `consume_iterator` | `more_itertools.consume` | 0 | 5 / 0 | yes |
| `check_is_sorted` | `more_itertools.is_sorted` | 3 | 5 / 1 | yes |
| `generate_distinct_combinations` | `more_itertools.distinct_combinations` | 0 | 5 / 1 | yes |
| `generate_distinct_permutations` | `more_itertools.distinct_permutations` | 2 | 6 / 0 | yes |
| `interleave_iterables` | `more_itertools.interleave` | 3 | 5 / 0 | yes |
| `sliding_window` | `more_itertools.windowed` | 0 | 5 / 0 | yes |
| `split_into_sizes` | `more_itertools.split_into` | 0 | 5 / 0 | yes |
| `repeat_elements` | `more_itertools.repeat_each` | 0 | 5 / 0 | yes |
| `repeat_sequence` | `more_itertools.ncycles` | 0 | 5 / 0 | yes |
| `group_elements` | `more_itertools.grouper` | 0 | 4 / 2 | yes |
| `batch_elements` | `more_itertools.batched` | 0 | 5 / 0 | yes |
| `group_consecutive` | `more_itertools.consecutive_groups` | 1 | 4 / 1 | yes |
| `stagger_elements` | `more_itertools.stagger` | 0 | 5 / 0 | yes |
| `zip_with_offset` | `more_itertools.zip_offset` | 2 | 5 / 0 | yes |
| `powerset` | `more_itertools.powerset` | 1 | 5 / 0 | yes |
| `count_matches` | `more_itertools.quantify` | 3 | 2 / 3 | yes |
| `unique_elements` | `more_itertools.unique_everseen` | 3 | 3 / 2 | yes |
| `running_average` | `more_itertools.running_mean` | 0 | 5 / 0 | yes |
| `sum_of_squares` | `more_itertools.sum_of_squares` | 1 | 5 / 1 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `create_seekable_iterator` | `more_itertools.seekable` | differential | Input {"iterable": [1, 2, 3, 4, 5], "maxlen": null}: the tool returned {"iterator": []}, but the direct library call returned [1, 2, 3, 4, 5] Input {"iterable": ["a", "b", "c"], "maxlen": 2}: the tool returned {"iterator |
| `count_items` | `more_itertools.ilen` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `iterate_until_exception` | `more_itertools.iter_except` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ['TypeError: issubclass() arg 2 must be a class, a tuple of classes, or a union']. Use samples that are valid for the library. |
| `check_all_unique` | `more_itertools.all_unique` | differential | Input {"iterable": ["A", "B", "C", "b"], "key": "str.lower"}: the direct library call raised TypeError: 'str' object is not callable, but the tool returned false Input {"iterable": ["A", "B", "C", "B"], "key": "str.lower |
| `filter_unique_window` | `more_itertools.unique_in_window` | runs | Input {"iterable": [0, 1, 0, 2, 3, 0], "n": 3}: the tool raised output is not JSON: 01230, but the direct library call returned [0, 1, 2, 3, 0] Input {"iterable": ["a", "a", "b"], "n": 1}: the tool raised output is not J |
| `zip_with_broadcasting` | `more_itertools.zip_broadcast` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `interleave_longest_iterables` | `more_itertools.interleave_longest` | differential | Input {"iterables": [[1, 2, 3], [4, 5], [6, 7, 8]]}: the tool returned 14625738, but the direct library call returned [1, 4, 6, 2, 5, 7, 3, 8] Input {"iterables": [[1, 2], [3, 4, 5], [6]]}: the tool returned 136245, but  |
| `transform_groupby` | `more_itertools.groupby_transform` | loads | NameError: name 'Callable' is not defined |
| `sort_multiple_iterables` | `more_itertools.sort_together` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `find_duplicates_everseen` | `more_itertools.duplicates_everseen` | runs | Input {"iterable": ["m", "i", "s", "s", "i", "s", "s", "i", "p", "p", "i"], "key": null}: the tool raised output is not JSON: sissipi, but the direct library call returned ["s", "i", "s", "s", "i", "p", "i"] Input {"iter |
| `find_duplicates_justseen` | `more_itertools.duplicates_justseen` | runs | Input {"iterable": ["m", "i", "s", "s", "i", "s", "s", "i", "p", "p", "i"], "key": null}: the tool raised output is not JSON: sissipi, but the direct library call returned ["s", "s", "p"] Input {"iterable": [1, 2, 3, 4,  |
| `find_unique_to_each` | `more_itertools.unique_to_each` | differential | Input {"iterables": [["a", "b", "c"], ["c", "d", "e"]]}: the direct library call raised IndexError: list index out of range, but the tool returned [["a", "b"], ["d", "e"]] Input {"iterables": []}: the direct library call |
| `find_first_true` | `more_itertools.first_true` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `locate_elements` | `more_itertools.locate` | differential | Input {"iterable": [], "predicate": "bool"}: the tool raised ValueError: Unsupported predicate: bool. Only these are allowed: ['truthy', 'falsy', 'is_none', 'is_not_none'], but the direct library call returned [] |
| `locate_elements_reverse` | `more_itertools.rlocate` | spec | only 1 samples gave a result to compare; 2 are needed. Add valid samples with different inputs. |
| `split_after_condition` | `more_itertools.split_after` | static | line 3: no code at module level except imports, definitions and constants |
| `split_before_condition` | `more_itertools.split_before` | static | line 3: no code at module level except imports, definitions and constants |
| `split_when_condition` | `more_itertools.split_when` | spec | direct_call may not use Lambda: only calls, attributes, names, constants and simple conditions |
| `take_while_inclusive` | `more_itertools.takewhile_inclusive` | spec | direct_call may not use Lambda: only calls, attributes, names, constants and simple conditions |
| `filter_and_map` | `more_itertools.filter_map` | syntax | line 1: invalid syntax |
| `conditional_map` | `more_itertools.map_if` | spec | direct_call may not use Lambda: only calls, attributes, names, constants and simple conditions |
| `map_and_reduce` | `more_itertools.map_reduce` | spec | only 1 samples gave a result to compare; 2 are needed. Add valid samples with different inputs. |
| `apply_side_effect` | `more_itertools.side_effect` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'str' object is not callable"]. Use samples that are valid for the library. |
| `sample_from_iterable` | `more_itertools.sample` | runs | Input {"iterable": ["a", "b", "c"], "k": 0}: the tool raised output is not JSON: , but the direct library call returned [] Input {"iterable": [], "k": 0}: the tool raised output is not JSON: , but the direct library call |
| `repeat_last_element` | `more_itertools.repeat_last` | spec | this parameter needs a snake_case name and a JSON type: {"name": "default_value", "type": "any", "description": "The default value to yield if the iterable is empty", "required": false, "default": null} |
| `pad_with_none` | `more_itertools.pad_none` | runs | Input {"iterable": [0, 1, 2]}: the tool raised output is not JSON: 012, but the direct library call returned [0, 1, 2, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, |
| `partition_iterable` | `more_itertools.partition` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `split_before_after` | `more_itertools.before_and_after` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'getattr' |
| `flatten_nested_list` | `more_itertools.flatten` | runs | Input {"list_of_lists": [[0, 1], [2, 3]]}: the tool raised output is not JSON: 0123, but the direct library call returned [0, 1, 2, 3] Input {"list_of_lists": []}: the tool raised output is not JSON: , but the direct lib |
| `prepend_value` | `more_itertools.prepend` | differential | Input {"iterable": [1, 2, 3], "value": 42}: the tool raised ValidationError: 4 validation errors for prepend_valueArguments value Input should be a valid string [type=string_type, input_value=42, input_type=int] For furt |
| `random_subset` | `more_itertools.random_combination` | runs | Input {"iterable": ["a", "b", "c", "d"], "size": 2}: the tool raised output is not JSON: ad, but the direct library call returned ["a", "c"] Input {"iterable": [], "size": 0}: the tool raised output is not JSON: , but th |
| `random_permutation` | `more_itertools.random_permutation` | differential | Input {"iterable": [1, 2, 3, 4, 5], "r": 3}: the tool raised ValueError: Failed to generate random permutation: Failed to generate random permutation: Failed to generate random permutation: Failed to generate random perm |
| `take_first_n` | `more_itertools.take` | runs | Input {"iterable": [0, 1, 2, 3, 4, 5], "n": 3}: the tool raised output is not JSON: 012, but the direct library call returned [0, 1, 2] Input {"iterable": [0, 1, 2], "n": 10}: the tool raised output is not JSON: 012, but |
| `get_last_n` | `more_itertools.tail` | runs | Input {"iterable": ["A", "B", "C", "D", "E", "F", "G"], "n": 3}: the tool raised output is not JSON: EFG, but the direct library call returned ["E", "F", "G"] Input {"iterable": [1, 2, 3, 4, 5], "n": 0}: the tool raised  |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/more-itertools-bench2/run_server.sh
```
