.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+


*******************************************************************************
Architecture Documentation
*******************************************************************************

This guide covers architectural documentation practices, including architectural
decision records (ADRs) and design documentation standards.

Architectural Decision Records
===============================================================================

Architectural Decision Records (ADRs) document the significant architectural
decisions made during the project lifecycle. They capture the context,
reasoning, and consequences of decisions to provide future teams with the
rationale behind architectural choices.

Purpose and Benefits
-------------------------------------------------------------------------------

* **Historical context**: Preserve the reasoning behind architectural decisions
  for future reference and team onboarding.

* **Decision accountability**: Create a clear record of who made decisions and
  under what circumstances.

* **Alternative exploration**: Document what was considered but not chosen,
  providing valuable context for future architectural reviews.

* **Change management**: Track the evolution of architectural decisions over
  time through status updates and supersession.

ADR Format
-------------------------------------------------------------------------------

Use the following format for all architectural decision records:

.. code-block:: rst

    *******************************************************************************
    [Number]. [Title]
    *******************************************************************************

    Status
    ===============================================================================

    [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

    Context
    ===============================================================================

    [Describe the forces at play, constraints, and business/technical situation 
    that led to this decision. What problem are we trying to solve? What are the 
    key requirements and limitations?]

    Decision
    ===============================================================================

    [State the decision clearly and concisely. This should be the response to the 
    forces described in the Context section.]

    Alternatives
    ===============================================================================

    [Document what other options were considered and why each was rejected. This 
    provides valuable context for future decisions and shows that alternatives 
    were properly evaluated.]

    Consequences
    ===============================================================================

    [Describe the positive, negative, and neutral consequences of this decision. 
    Be honest about trade-offs and potential risks. Include impacts on:
    - Performance
    - Maintainability  
    - Team productivity
    - System complexity
    - Future flexibility]

ADR Lifecycle Management
-------------------------------------------------------------------------------

**Numbering Convention**

* Use sequential numbering: ``001-initial-architecture.rst``,
  ``002-database-selection.rst``, etc.
* Zero-pad numbers to three digits for consistent sorting.
* Use lowercase, hyphenated filenames.

**Status Workflow**

* **Proposed**: Decision is under consideration and review.
* **Accepted**: Decision has been approved and is being implemented.
* **Deprecated**: Decision is no longer relevant but kept for historical context.
* **Superseded**: Decision has been replaced by a newer ADR (reference the
  superseding ADR number).

**Immutability Principle**

* Once an ADR is accepted, do not edit its content.
* If circumstances change, create a new ADR that supersedes the previous one.
* This preserves the historical decision context and reasoning.

Best Practices
-------------------------------------------------------------------------------

**Context Documentation**

* Focus on forces and constraints that drove the decision.
* Include relevant business context, technical limitations, and team constraints.
* Avoid implementation details - focus on the decision-making environment.

**Clear Decision Statements**

* State decisions unambiguously.
* Avoid hedging language like "might" or "could".
* Be specific about what will be done.

**Comprehensive Alternatives**

* Document all seriously considered alternatives.
* Explain why each alternative was rejected with specific reasons.
* Include "do nothing" as an alternative when relevant.

**Honest Consequences**

* Document both positive and negative consequences.
* Include trade-offs and potential risks.
* Consider long-term implications, not just immediate benefits.

Architecture Documentation Beyond ADRs
===============================================================================

System Summary
-------------------------------------------------------------------------------

The system summary (``architecture/summary.rst``) should provide a high-level
overview of the system architecture including:

* **Major components**: Key system modules, services, or subsystems.
* **Component relationships**: How components interact and depend on each other.
* **Data flow**: Major data paths through the system.
* **Deployment architecture**: How components are distributed and deployed.
* **Key architectural patterns**: Major patterns employed (MVC, microservices,
  event-driven, etc.).

Design Documents
-------------------------------------------------------------------------------

Detailed design documents (under ``architecture/designs/``) capture
implementation-level specifications:

* **Interface specifications**: API contracts, service interfaces, module APIs.
* **Data schemas**: Database schemas, message formats, configuration structures.
* **Algorithm specifications**: Detailed algorithmic approaches for complex
  processing.
* **Protocol definitions**: Communication protocols between components.

**Design Document Guidelines**

* Reference the architectural decisions that informed the design.
* Include enough detail for implementation without over-specifying.
* Use diagrams and examples to illustrate complex concepts.
* Version design documents when significant changes occur.