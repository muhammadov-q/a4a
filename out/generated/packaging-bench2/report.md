# repo2tools report: packaging-bench2

- Repo: https://github.com/pypa/packaging at `5a7d3386d2777180a381eb947f21293124ce8df5`
- Package: `packaging`, 99 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 2.4 min. LLM tokens: 327,137 in 210 requests (propose 7,129, spec 142,155, code 177,853)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 60 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 41 |
| Accepted and confirmed against a direct library call | 40 |
| Passed all checks on the first try | 25 |
| Rejected after the repair rounds | 19 |

First try, by the first check that failed: ok: 25, spec: 21, static: 4, differential: 4, runs: 2, fastmcp: 2, syntax: 1, loads: 1.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `dependency_group_lookup` | `packaging.dependency_groups.DependencyGroupResolver.lookup` | 2 | 4 / 1 | yes |
| `dependency_group_resolve` | `packaging.dependency_groups.DependencyGroupResolver.resolve` | 0 | 4 / 1 | yes |
| `direct_url_from_dict` | `packaging.direct_url.DirectUrl.from_dict` | 0 | 4 / 1 | yes |
| `direct_url_to_dict` | `packaging.direct_url.DirectUrl.to_dict` | 3 | 5 / 0 | yes |
| `direct_url_validate` | `packaging.direct_url.DirectUrl.validate` | 0 | 3 / 2 | yes |
| `marker_evaluate` | `packaging.markers.Marker.evaluate` | 0 | 5 / 1 | yes |
| `marker_evaluate_prepared` | `packaging.markers.Marker.evaluate_prepared` | 1 | 5 / 0 | yes |
| `default_marker_environment` | `packaging.markers.default_environment` | 0 | 4 / 0 | yes |
| `metadata_from_raw` | `packaging.metadata.Metadata.from_raw` | 0 | 0 / 1 | no: unstable, both_error |
| `parse_metadata_email` | `packaging.metadata.parse_email` | 0 | 5 / 0 | yes |
| `package_is_direct` | `packaging.pylock.Package.is_direct` | 3 | 5 / 0 | yes |
| `version_range_empty` | `packaging.ranges.VersionRange.empty` | 2 | 3 / 0 | yes |
| `version_range_full` | `packaging.ranges.VersionRange.full` | 0 | 5 / 0 | yes |
| `version_range_singleton` | `packaging.ranges.VersionRange.singleton` | 0 | 4 / 1 | yes |
| `version_range_from_bounds` | `packaging.ranges.VersionRange.from_bounds` | 0 | 5 / 1 | yes |
| `version_range_intersection` | `packaging.ranges.VersionRange.intersection` | 3 | 5 / 0 | yes |
| `version_range_complement` | `packaging.ranges.VersionRange.complement` | 2 | 5 / 0 | yes |
| `version_range_difference` | `packaging.ranges.VersionRange.difference` | 0 | 5 / 1 | yes |
| `version_range_is_subset` | `packaging.ranges.VersionRange.is_subset` | 0 | 6 / 0 | yes |
| `version_range_is_superset` | `packaging.ranges.VersionRange.is_superset` | 1 | 5 / 0 | yes |
| `version_range_is_disjoint` | `packaging.ranges.VersionRange.is_disjoint` | 2 | 5 / 0 | yes |
| `version_range_filter` | `packaging.ranges.VersionRange.filter` | 2 | 5 / 0 | yes |
| `version_range_snap_bounds` | `packaging.ranges.VersionRange.snap_bounds` | 2 | 5 / 0 | yes |
| `version_range_is_empty` | `packaging.ranges.VersionRange.is_empty` | 2 | 5 / 0 | yes |
| `version_range_contains` | `packaging.ranges.VersionRange.contains` | 2 | 6 / 0 | yes |
| `specifier_contains` | `packaging.specifiers.Specifier.contains` | 0 | 6 / 0 | yes |
| `specifier_filter` | `packaging.specifiers.Specifier.filter` | 1 | 5 / 0 | yes |
| `specifier_set_is_unsatisfiable` | `packaging.specifiers.SpecifierSet.is_unsatisfiable` | 0 | 5 / 0 | yes |
| `specifier_set_to_range` | `packaging.specifiers.SpecifierSet.to_range` | 0 | 5 / 0 | yes |
| `specifier_set_is_subset` | `packaging.specifiers.SpecifierSet.is_subset` | 0 | 5 / 0 | yes |
| `specifier_set_is_superset` | `packaging.specifiers.SpecifierSet.is_superset` | 0 | 5 / 0 | yes |
| `specifier_set_is_disjoint` | `packaging.specifiers.SpecifierSet.is_disjoint` | 0 | 5 / 0 | yes |
| `specifier_set_contains` | `packaging.specifiers.SpecifierSet.contains` | 0 | 5 / 0 | yes |
| `tag_interpreter` | `packaging.tags.Tag.interpreter` | 0 | 6 / 0 | yes |
| `tag_abi` | `packaging.tags.Tag.abi` | 1 | 5 / 0 | yes |
| `tag_platform` | `packaging.tags.Tag.platform` | 0 | 5 / 0 | yes |
| `interpreter_abi` | `packaging.tags.interpreter_abi` | 2 | 2 / 0 | yes |
| `interpreter_name` | `packaging.tags.interpreter_name` | 0 | 4 / 0 | yes |
| `interpreter_version` | `packaging.tags.interpreter_version` | 0 | 5 / 0 | yes |
| `parse_tag` | `packaging.tags.parse_tag` | 2 | 5 / 1 | yes |
| `platform_tags` | `packaging.tags.platform_tags` | 0 | 2 / 0 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `resolve_dependency_groups` | `packaging.dependency_groups.resolve_dependency_groups` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["ExceptionGroup: [dependency-groups] data for 'optional' was malformed (1 sub-exception)", "TypeError: expected string or bytes-like object, go |
| `canonicalize_license_expression` | `packaging.licenses.canonicalize_license_expression` | runs | Input {"raw_license_expression": "mit"}: the tool raised RecursionError: maximum recursion depth exceeded, but the direct library call returned "MIT" Input {"raw_license_expression": "mit and (apache-2.0 or bsd-2-clause) |
| `prepare_marker_environment` | `packaging.markers.prepare_environment` | end_to_end | over MCP it returned {"implementation_name": "cpython", "implementation_version": "3.12.3", "os_name": "posix", "platform_machine": "arm64", "platform_release": "27.2.0", "platform_system": "Linux", "platform_version": " |
| `metadata_from_email` | `packaging.metadata.Metadata.from_email` | syntax | line 175: unterminated string literal (detected at line 175) |
| `metadata_as_rfc822` | `packaging.metadata.Metadata.as_rfc822` | spec | the direct_call expression is wrong: AttributeError: 'Metadata' object has no attribute 'Version' |
| `sdist_filename` | `packaging.pylock.PackageSdist.filename` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'str' object is not callable"]. Use samples that are valid for the library. |
| `wheel_filename` | `packaging.pylock.PackageWheel.filename` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'str' object is not callable"]. Use samples that are valid for the library. |
| `pylock_from_dict` | `packaging.pylock.Pylock.from_dict` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["PylockValidationError: Unexpected type dict (expected Sequence) in 'packages'"]. Use samples that are valid for the library. |
| `pylock_to_dict` | `packaging.pylock.Pylock.to_dict` | fastmcp | PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'packaging.version.Version'>) For further information visit https://errors.pydantic.dev/2.14/u/invalid-for-json-schema |
| `pylock_validate` | `packaging.pylock.Pylock.validate` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["_PylockRequiredKeyError: Missing required value in 'packages'"]. Use samples that are valid for the library. |
| `pylock_select` | `packaging.pylock.Pylock.select` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'open' |
| `is_valid_pylock_path` | `packaging.pylock.is_valid_pylock_path` | spec | direct_call may not use: pathlib |
| `version_range_union` | `packaging.ranges.VersionRange.union` | differential | Input {"range1": ">=1.0,<2.0", "range2": ">=2.0,<3.0"}: the tool raised ValueError: Failed to compute union of version ranges: cannot create 'VersionRange' instances directly; use SpecifierSet.to_range(), VersionRange.fu |
| `version_range_relation` | `packaging.ranges.VersionRange.relation` | differential | Input {"range1": ">=1.0.0", "range2": ">=1.0.0"}: the tool returned "subset", but the direct library call returned 2 Input {"range1": ">=1.0.0,<2.0.0", "range2": ">=1.5.0,<1.9.0"}: the tool returned "overlapping", but th |
| `version_range_to_specifier_set` | `packaging.ranges.VersionRange.to_specifier_set` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'to_specifier_set' |
| `specifier_set_filter` | `packaging.specifiers.SpecifierSet.filter` | differential | Input {"iterable": [{"ver": "1.2"}, {"ver": "1.3"}], "prereleases": null, "specifiers": ">=1.2.3"}: the tool returned [{"ver": "1.3"}], but the direct library call returned [] |
| `compatible_tags` | `packaging.tags.compatible_tags` | runs | Input {"interpreter": "cp39", "python_version": [3, 9]}: the tool raised RecursionError: maximum recursion depth exceeded, but the direct library call returned ["py39-none-macosx_27_0_arm64", "py39-none-macosx_27_0_unive |
| `cpython_tags` | `packaging.tags.cpython_tags` | differential | Input {"abis": null, "platforms": null, "python_version": [3, 9], "warn": false}: the tool raised ValueError: Failed to generate CPython tags: Failed to generate CPython tags: Failed to generate CPython tags: Failed to g |
| `generic_tags` | `packaging.tags.generic_tags` | differential | Input {"abis": ["cp39", "abi3"], "interpreter": "py39", "platforms": ["linux_x86_64"]}: the tool raised ValueError: Failed to generate tags: Failed to generate tags: Failed to generate tags: Failed to generate tags: Fail |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/packaging-bench2/run_server.sh
```
