"""A tool set with one tool, `run_sql`, that runs a read-only query on one database. Standard library and `mcp` only.

`a4a db-benchmark` starts this file as an MCP server on stdio, inside the sandbox that holds a copy of the database:

    <env>/bin/python -I sql_tool.py --database database.sqlite

The database is opened read-only for every call, so a call cannot change it and nothing is kept between
calls. A query that runs longer than SECONDS is stopped. The reply is the rows as JSON, at most MAX_ROWS.
"""

import json
import sqlite3
import sys
import time
from pathlib import Path

SECONDS = 10
MAX_ROWS = 200
DESCRIPTION = ("Run one SQL query on the SQLite database and get the rows back as a JSON list of lists. The database is read-only. "
               "Use `SELECT name, sql FROM sqlite_master` to see the tables. At most {rows} rows are returned; a query is stopped after {seconds} seconds.")


def rows_of(database: str, query: str) -> str:
    """The rows of a query as JSON text. Raises RuntimeError with the reason if the query cannot be run."""
    connection = sqlite3.connect(f"{Path(database).resolve().as_uri()}?mode=ro", uri=True)
    deadline = time.monotonic() + SECONDS
    connection.set_progress_handler(lambda: time.monotonic() > deadline, 10_000)
    try:
        cursor = connection.execute(query)
        rows = cursor.fetchmany(MAX_ROWS + 1)
    except sqlite3.OperationalError as error:
        raise RuntimeError("the query did not finish in time" if "interrupted" in str(error) else f"{error}") from None
    except (sqlite3.Error, sqlite3.Warning) as error:
        raise RuntimeError(f"{type(error).__name__}: {error}") from None
    finally:
        connection.close()
    plain = [[value.hex() if isinstance(value, bytes) else value for value in row] for row in rows[:MAX_ROWS]]
    return json.dumps(plain) + (f"\n[only the first {MAX_ROWS} rows are shown]" if len(rows) > MAX_ROWS else "")


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != "--database":
        sys.exit("usage: sql_tool.py --database <file>")
    from mcp.server.fastmcp import FastMCP

    database = sys.argv[2]

    async def run_sql(query: str) -> str:
        return rows_of(database, query)

    server = FastMCP("sql", log_level="WARNING")
    server.add_tool(run_sql, description=DESCRIPTION.format(rows=MAX_ROWS, seconds=SECONDS))
    server.run()


if __name__ == "__main__":
    main()
