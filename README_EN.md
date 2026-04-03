# Mentor.skill

> Turn a mentor's style, advice patterns, and working norms into an AI Skill you can revisit and refine.

Provide chat logs, notes, talks, public writing, screenshots, and your own observations. The skill turns them into a mentor-style conversational profile that feels grounded in how this person actually thinks and gives feedback.

## Use Cases

* Review a mentor's advice and patterns
* Simulate reporting, Q&A, and career discussions
* Capture communication style and expectations
* Keep refining the mentor profile as you collect more material

## Structure

Each generated mentor skill has two parts:

* `Mentorship Memory`: interaction history, guidance topics, memorable advice, recurring contexts
* `Persona`: tone, questioning style, reasoning habits, encouragement and critique patterns

## Quick Start

In Claude Code:

```bash
/create-mentor
```

Then provide:

1. A name or codename
2. Basic background
3. Style/personality summary
4. Optional source materials

After creation, use `/{slug}` to invoke the mentor skill.

## Example

Input:

```text
Professor Wang is my AI product mentor. I usually ask about project framing, portfolio decisions, and career tradeoffs. They speak directly, often start with "what exactly is your goal?", and give sharp but actionable feedback.
```

The generated skill should feel like someone who:

* starts with goals and constraints
* pushes for clearer thinking
* gives structured feedback instead of vague encouragement
* keeps the mentor's real tone and boundaries

## Commands

| Command | Description |
|---------|-------------|
| `/create-mentor` | Create a mentor skill |
| `/list-mentors` | List all mentor skills |
| `/{slug}` | Full mentor mode |
| `/{slug}-memory` | Mentorship memory only |
| `/{slug}-persona` | Persona only |
| `/mentor-rollback {slug} {version}` | Roll back to a previous version |
| `/delete-mentor {slug}` | Delete a mentor skill |

## Principles

* Prefer evidence over invention
* Preserve the mentor's real tone and boundaries
* Mark missing information instead of guessing
* Use for learning and rehearsal, not impersonation
