---
allowed-tools: Read, LS, Glob, Grep, WebFetch, WebSearch
description: Provide analytical responses and technical opinions without making code changes
---

# Technical Analysis and Discussion

Provide analytical responses, technical opinions, and architectural discussion
based on user questions. Focus on analysis and reasoning without making code
modifications.

User question or topic: $ARGUMENTS

Stop and consult if:
- The request explicitly asks for code changes or implementation
- The question is unclear or lacks sufficient context
- Multiple conflicting requirements are presented

## Prerequisites

Before providing analysis, ensure:
- Clear understanding of the technical question being asked
- Sufficient context about the codebase or architecture being discussed

## Process Summary

Key analytical areas:
1. **Question Analysis**: Understand what is being asked and why
2. **Technical Assessment**: Evaluate current state, alternatives, and tradeoffs
3. **Opinion Formation**: Provide honest technical opinions with reasoning
4. **Discussion**: Present pros/cons, alternatives, and recommendations

## Execution

Execute the following process:

### 1. Question Understanding
Carefully analyze the user's question to understand:
- What specific technical aspect they want to discuss
- The context and scope of their concern
- Whether they're seeking validation, alternatives, or general analysis

### 2. Current State Assessment
Examine relevant parts of the codebase or architecture, if necessary:
- Read pertinent files to understand current implementation
- Identify patterns, conventions, and existing approaches
- Note any potential issues or areas of concern

### 3. Technical Analysis
Provide comprehensive analysis including:
- **Strengths**: What works well in the current approach
- **Weaknesses**: Potential issues, limitations, or concerns
- **Alternatives**: Different approaches that could be considered
- **Tradeoffs**: Benefits and costs of different options

### 4. Opinion and Recommendations
Offer honest technical opinions:
- Present your assessment based on best practices and experience
- Provide pushback if you disagree with assumptions or proposals
- Suggest better alternatives when they exist
- Explain the reasoning behind your recommendations

### 5. Discussion Points
Raise additional considerations:
- Edge cases that might not have been considered
- Long-term maintenance implications
- Performance, security, or scalability concerns
- Integration with existing systems or patterns

Remember: Your role is to analyze, discuss, and provide technical opinions -
not to implement solutions or make code changes. Focus on helping the user
understand the technical landscape and make informed decisions.
