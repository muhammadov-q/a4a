# repo2tools report: networkx-bench2

- Repo: https://github.com/networkx/networkx at `ada19dd8000ec550fd45cf72841c416319dc568d`
- Package: `networkx`, 1180 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 2.7 min. LLM tokens: 500,882 in 225 requests (propose 46,797, spec 288,276, code 165,809)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 45 (dropped: 12, for unknown functions, duplicates or bad names) |
| Accepted | 3 |
| Accepted and confirmed against a direct library call | 3 |
| Passed all checks on the first try | 0 |
| Rejected after the repair rounds | 42 |

First try, by the first check that failed: spec: 27, static: 8, fastmcp: 7, differential: 3.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `create_undirected_graph` | `networkx.Graph` | 2 | 4 / 1 | yes |
| `create_directed_graph` | `networkx.DiGraph` | 1 | 3 / 1 | yes |
| `compute_degree_centrality` | `networkx.degree_centrality` | 1 | 5 / 0 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `add_node_to_graph` | `networkx.Graph.add_node` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'add_node' |
| `add_edge_to_graph` | `networkx.Graph.add_edge` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'add_edge' |
| `get_graph_nodes` | `networkx.Graph.nodes` | spec | only 1 samples gave a result to compare; 2 are needed. Add valid samples with different inputs. |
| `get_graph_edges` | `networkx.Graph.edges` | differential | Input {"graph": {"edges": [[1, 2], [2, 3]], "nodes": [1, 2, 3]}}: the tool returned [[1, 2], [2, 3]], but the direct library call returned {} Input {"graph": {"edges": [["a", "b"], ["b", "c"]], "nodes": ["a", "b", "c"]}} |
| `check_edge_exists` | `networkx.Graph.has_edge` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'has_edge' |
| `add_star_to_graph` | `networkx.add_star` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'add_node' |
| `add_path_to_graph` | `networkx.add_path` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'add_node' |
| `add_cycle_to_graph` | `networkx.add_cycle` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'add_node' |
| `set_node_attributes` | `networkx.set_node_attributes` | fastmcp | PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'networkx.classes.graph.Graph'>) For further information visit https://errors.pydantic.dev/2.14/u/invalid-for-json-schem |
| `get_node_attributes` | `networkx.get_node_attributes` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `set_edge_attributes` | `networkx.set_edge_attributes` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `get_edge_attributes` | `networkx.get_edge_attributes` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_multigraph' |
| `create_petersen_graph` | `networkx.petersen_graph` | spec | only 1 samples gave a result to compare; 2 are needed. Add valid samples with different inputs. |
| `load_karate_club_network` | `networkx.karate_club_graph` | differential | Input {}: the tool returned {"clubs": {"0": "Mr. Hi", "1": "Mr. Hi", "10": "Mr. Hi", "11": "Mr. Hi", "12": "Mr. Hi", "13": "Mr. Hi", "14": "Officer", "15": "Officer", "16": "Mr. Hi", "17": "Mr. Hi", "18": "Officer", "19" |
| `read_graph_from_edgelist` | `networkx.read_edgelist` | fastmcp | PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'networkx.classes.graph.Graph'>) For further information visit https://errors.pydantic.dev/2.14/u/invalid-for-json-schem |
| `write_graph_to_edgelist` | `networkx.write_edgelist` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'edges' |
| `compute_betweenness_centrality` | `networkx.betweenness_centrality` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'is_multigraph' |
| `compute_closeness_centrality` | `networkx.closeness_centrality` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_directed' |
| `compute_pagerank` | `networkx.pagerank` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'numpy' |
| `compute_hubs_and_authorities` | `networkx.hits` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'numpy' |
| `compute_clustering_coefficient` | `networkx.clustering` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'is_directed' |
| `shortest_path_length` | `networkx.shortest_path_length` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_directed' |
| `average_shortest_path_length` | `networkx.average_shortest_path_length` | fastmcp | PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'networkx.classes.graph.Graph'>) For further information visit https://errors.pydantic.dev/2.14/u/invalid-for-json-schem |
| `breadth_first_search_edges` | `networkx.bfs_edges` | fastmcp | PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'networkx.classes.graph.Graph'>) For further information visit https://errors.pydantic.dev/2.14/u/invalid-for-json-schem |
| `depth_first_search_edges` | `networkx.dfs_edges` | spec | this parameter needs a snake_case name and a JSON type: {"name": "source", "type": "any", "description": "Specify starting node for depth-first search", "required": false, "default": null} |
| `find_minimum_spanning_tree` | `networkx.minimum_spanning_tree` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_directed' |
| `check_graph_isomorphism` | `networkx.is_isomorphic` | spec | this parameter needs a snake_case name and a JSON type: {"name": "node_match", "type": "function", "description": "Function to determine if nodes are equivalent", "required": false, "default": null} |
| `draw_planar_graph` | `networkx.draw_planar` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'numpy' |
| `draw_shell_graph` | `networkx.draw_shell` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'numpy' |
| `draw_forceatlas2_graph` | `networkx.draw_forceatlas2` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'numpy' |
| `find_maximum_clique` | `networkx.algorithms.approximation.max_clique` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'is_multigraph' |
| `compute_node_connectivity` | `networkx.algorithms.approximation.node_connectivity` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'is_directed' |
| `solve_tsp` | `networkx.algorithms.approximation.traveling_salesman_problem` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'is_directed' |
| `find_communities` | `networkx.algorithms.community.greedy_modularity_communities` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'size' |
| `find_louvain_communities` | `networkx.algorithms.community.louvain_communities` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute '_adj' |
| `find_leiden_communities` | `networkx.algorithms.community.leiden_communities` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute '_adj' |
| `find_infomap_communities` | `networkx.algorithms.community.infomap_communities` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'is_directed' |
| `find_shortest_path` | `networkx.algorithms.shortest_paths.shortest_path` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'nx' |
| `find_minimum_node_cut` | `networkx.algorithms.connectivity.minimum_st_node_cut` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_directed' |
| `find_minimum_edge_cut` | `networkx.algorithms.connectivity.minimum_st_edge_cut` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_directed' |
| `check_tree_isomorphism` | `networkx.algorithms.isomorphism.tree_isomorphism` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_multigraph' |
| `generate_graph_isomorphisms` | `networkx.algorithms.isomorphism.isomorphvf2.GraphMatcher.isomorphisms_iter` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'is_directed' |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/networkx-bench2/run_server.sh
```
