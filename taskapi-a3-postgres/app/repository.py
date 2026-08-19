"""
TaskRepository — the ONLY module in this app that speaks SQL.

Routes and the app layer never see a connection or a query string; they
call methods here. That's what lets storage change (memory -> SQLite ->
Postgres, across A1/A2/A3) without touching a single route.

All queries are parameterized (%s placeholders) — user input is always
passed separately from the SQL text, never string-glued into it.
"""


class TaskRepository:
    def __init__(self, pool):
        self.pool = pool

    def init_table(self):
        with self.pool.connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
                """
            )

    def seed_if_empty(self):
        with self.pool.connection() as conn:
            (count,) = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()
            if count == 0:
                conn.execute(
                    """
                    INSERT INTO tasks (title, done) VALUES
                        (%s, %s),
                        (%s, %s),
                        (%s, %s)
                    """,
                    (
                        "Buy groceries", False,
                        "Write report", False,
                        "Walk the dog", True,
                    ),
                )

    def ping(self):
        with self.pool.connection() as conn:
            conn.execute("SELECT 1")

    def get_all(self):
        with self.pool.connection() as conn:
            rows = conn.execute(
                "SELECT id, title, done FROM tasks ORDER BY id"
            ).fetchall()
            return [self._to_dict(r) for r in rows]

    def get_by_id(self, task_id: int):
        with self.pool.connection() as conn:
            row = conn.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s", (task_id,)
            ).fetchone()
            return self._to_dict(row) if row else None

    def create(self, title: str, done: bool):
        with self.pool.connection() as conn:
            row = conn.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) "
                "RETURNING id, title, done",
                (title, done),
            ).fetchone()
            return self._to_dict(row)

    def update(self, task_id: int, title: str, done: bool):
        with self.pool.connection() as conn:
            row = conn.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s "
                "RETURNING id, title, done",
                (title, done, task_id),
            ).fetchone()
            return self._to_dict(row) if row else None

    def delete(self, task_id: int) -> bool:
        with self.pool.connection() as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            return cur.rowcount > 0

    @staticmethod
    def _to_dict(row):
        return {"id": row[0], "title": row[1], "done": row[2]}
