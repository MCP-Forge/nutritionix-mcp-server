# 🥦 Nutritionix MCP Server

This is an **MCP (Model Context Protocol) server** for integrating with the [Nutritionix API](https://developer.nutritionix.com/), enabling AI agents to access food search, nutrition data, and exercise calorie estimates via natural language input.

The goal of this project is to expose Nutritionix's functionality through MCP-compatible tools that can be used seamlessly by large language models and agent frameworks.

---

## 🧠 What is MCP?

MCP (Model Context Protocol) is a lightweight protocol designed to let **AI agents interact with external tools and APIs** in a structured and modular way. Think of it like **USB for AI** — this server acts as a "driver" for the Nutritionix platform.

With this MCP server, AI models can:

- 🔍 Search for common and branded food items  
- 🍽️ Parse natural language meals into nutritional breakdowns  
- 🏃 Estimate calories burned from exercises like running, cycling, or yoga

---

# 🚀 How to Run

To use this MCP server, you'll need:

## ✅ Prerequisites

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) – a modern Python package manager
- A supported LLM (e.g., Claude)
- A Nutritionix API App ID and App Key – get them at [developer.nutritionix.com](https://developer.nutritionix.com)

## Add this to Claude Desktop config

```json
{
  "mcpServers": {
    "nutritionix-mcp": {
      "command": "uvx",
      "args": [
        "nutritionix-mcp-server",
        "--app-id",
        "YOUR APP ID",
        "--app-key",
        "YOUR APP KEY"
      ]
    }
  }
}
```

---

## 🤝 Contributions Welcome!

Whether you're into nutrition tech, AI agent development, or API tooling — we’d love your help improving this project. You can contribute by:

- Adding new tools (e.g., barcode search, food logging)
- Improving response formatting
- Writing tests or documentation
- Suggesting new ideas via Issues or Discussions

Feel free to fork, explore, and submit a PR. Let’s make agent-integrated nutrition smarter, together. 🧠🥗

---

**MCP-FORGE** – Building tools for the future of intelligent automation.
