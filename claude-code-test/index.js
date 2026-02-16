const path = require("path");
const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

let todos = [];
let nextId = 1;

// 全Todo取得
app.get("/todos", (req, res) => {
  res.json(todos);
});

// Todo作成
app.post("/todos", (req, res) => {
  const { title } = req.body;
  if (!title) {
    return res.status(400).json({ error: "title is required" });
  }
  const todo = { id: nextId++, title, completed: false };
  todos.push(todo);
  res.status(201).json(todo);
});

// Todo更新
app.put("/todos/:id", (req, res) => {
  const todo = todos.find((t) => t.id === Number(req.params.id));
  if (!todo) {
    return res.status(404).json({ error: "todo not found" });
  }
  const { title, completed } = req.body;
  if (!title) {
    return res.status(400).json({ error: "title is required" });
  }
  todo.title = title;
  todo.completed = completed !== undefined ? completed : false;
  res.json(todo);
});

// Todo削除
app.delete("/todos/:id", (req, res) => {
  const index = todos.findIndex((t) => t.id === Number(req.params.id));
  if (index === -1) {
    return res.status(404).json({ error: "todo not found" });
  }
  todos.splice(index, 1);
  res.status(204).end();
});

app.listen(PORT, () => {
  console.log(`Todo app listening on http://localhost:${PORT}`);
});
