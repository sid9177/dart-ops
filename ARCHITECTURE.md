# Project Architecture & Constraints

This document serves as the absolute source of truth for the project's architectural decisions and constraints. 
**Agent Instruction:** You MUST read this file before brainstorming any new features, creating plans, or writing any code. If a proposed design violates these rules, you must reject it.

## 1. Primary Goal: Copy-Paste Staging Environment
This repository is a staging area. The code here is meant to be perfectly accurate and robust so it can be directly copied and pasted into the corporate "Helix" environment (which is built on top of ADK).
- **NO Infrastructure:** Do not develop deployment, hosting, or full CI/CD infrastructure here. Helix handles its own infrastructure.
- **Portability:** Code must be fully self-contained.

## 2. Core Principle: Configuration Over Code Changes
The primary design pattern of this system is that business logic, agent instructions, and workflows must be defined via configuration (YAML/Markdown), NOT hardcoded in Python.
- Users should only ever need to modify non-code elements (skills, data sources, agent descriptions, prompts) to adapt the agents to new tasks.
- **Strict Rule:** Never hardcode an Agent's `instruction` or `name` in a Python file. They must be dynamically loaded from a configuration file.

## 3. ADK Constraints
- The company currently supports **Google ADK 1.31**.
- **No ADK 2.0:** Do not use ADK 2.0 Workflows or features.
- **No Blocking I/O:** The target Helix Web UI will freeze if Python `input()` or terminal-blocking functions are used. 

## 4. Human-In-The-Loop (HITL)
Because of the ADK 1.31 `input()` constraint, all human interaction must be **Conversational / Prompt-Driven**.
- We use "Approval Gates" and "Clarification Gates" via explicit instructions in the Agent's system prompt (e.g., "Ask the user for approval before proceeding").

## 5. Coding Behavior
- **Surgical Changes:** Touch only what is necessary. Clean up only your own mess. Every changed line must trace directly to the user's request.
- **Simplicity First:** Minimum code that solves the problem. No speculative abstractions.
- **Test-Driven Development:** Write the failing test first, then minimal implementation to pass it.
