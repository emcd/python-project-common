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
Tests
*******************************************************************************

Core Testing Principles
===============================================================================

* **Dependency Injection Over Monkey-Patching**: This codebase uses immutable
  objects that prevent monkey-patching by design. Use dependency injection
  patterns instead.

* **Performance-Conscious Resource Use**: I/O performance is important. Prefer
  in-memory filesystems (e.g., ``pyfakefs``) over ones backed by
  higher-latency storage (temporary directories).

* **Avoid Monkey-Patching**: Try to avoid monkey-patching entirely. Any
  exceptions to this rule should be discussed and documented on a case-by-case
  basis.

* **100% Coverage Goal**: Always aim for 100% line and branch coverage. Use
  ``# pragma: no cover`` only as a last resort after exhausting dependency
  injection and architectural alternatives.

Anti-Patterns to Avoid
===============================================================================

* **Monkey-Patching Internal Code**: Will fail with immutable objects::

    # WRONG - will fail with AttributeImmutability
    with patch.object( MyClass, '_some_method' ): pass
    with patch( 'mypackage.module._some_function' ): pass

* **Excessive Mocking**: Over-mocking leads to tests that pass but don't catch
  real bugs.

* **Testing Implementation Details**: Tests should verify behavior, not
  internal implementation specifics.

Test Organization
===============================================================================

Test files should use a systematic numbering system to enforce execution order
and logical grouping.

Test Directory Structure
-------------------------------------------------------------------------------

::

    tests/
    ├── README.md                     # Test organization documentation
    └── test_000_packagename/         # Package-specific test namespace
        ├── __init__.py              # Test package initialization
        ├── fixtures.py              # Common test fixtures and utilities
        ├── test_000_package.py      # Package-level tests
        ├── test_010_internals.py    # Internal utilities
        ├── test_100_<layer 0>.py    # Lowest levels of public API
        ├── test_200_<layer 1>.py    # Lower levels of public API
        ├── ...                      # Higher levels of API
        └── test_500_integration.py  # Top levels of API; Integration tests

Numbering System
-------------------------------------------------------------------------------

* **000-099**: Package internals (private utilities, base classes, etc.)
* **100-999**: Public API aspects, allocated by layer in blocks of 100

  - Lower-level functionality → lower-numbered blocks
  - Higher-level functionality and integration → higher-numbered blocks

* Test modules should generally correspond to source modules
* Siblings can be separated by increments of 10

Test Function Numbering
-------------------------------------------------------------------------------

Within test modules, number test functions similarly::

    def test_000_basic_functionality():
        ''' Basic feature works as expected. '''

    def test_100_error_handling():
        ''' Error conditions are handled gracefully. '''

    def test_200_advanced_scenarios():
        ''' Advanced usage patterns work correctly. '''

* **000-099**: Foundational tests for the module
* **100-199, 200-299, etc.**: Each function/class gets its own 100 block
* Closely related siblings can share a block (separated by 10 or 20)
* Different aspects of the same function/class separated by 5 or 10

Test README Documentation
-------------------------------------------------------------------------------

Maintain a ``tests/README.md`` file documenting:

* Test module numbering scheme specific to your package
* Rationale for any use of ``patch`` or other exceptions to standard patterns
* Project-specific testing conventions and fixtures

Preferred Testing Patterns
===============================================================================

Dependency Injection
-------------------------------------------------------------------------------

The most important testing pattern. Inject dependencies via parameters::

    # Function with injectable dependency
    async def process_data( data: str, processor: Callable = default_processor ):
        return await processor( data )

    # Test with custom processor
    async def test_process_data():
        def mock_processor( data ):
            return f"processed: {data}"

        result = await process_data( "test", processor = mock_processor )
        assert result == "processed: test"

Constructor injection for objects::

    @dataclass( frozen = True )
    class DataProcessor:
        validator: Callable[ [ str ], bool ] = default_validator

        def process( self, data: str ) -> str:
            if not self.validator( data ):
                raise ValueError( "Invalid data" )
            return data.upper()

    # Test with custom validator
    def test_data_processor():
        def always_valid( data ):
            return True

        processor = DataProcessor( validator = always_valid )
        result = processor.process( "test" )
        assert result == "TEST"

Filesystem Operations
-------------------------------------------------------------------------------

Prefer in-memory filesystems for performance. Use real temporary directories
only when necessary::

    from pyfakefs.fake_filesystem_unittest import Patcher
    from pathlib import Path

    # Preferred - use pyfakefs for most filesystem operations
    def test_sync_file_operations():
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_file( '/fake/config.toml', contents = '[section]\nkey = "value"' )
            result = process_config_file( Path( '/fake/config.toml' ) )
            assert result.key == 'value'

    # When necessary - use real temp directories for async operations
    @pytest.mark.asyncio
    async def test_async_file_operations():
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path( temp_dir )
            config_file = temp_path / 'config.toml'
            config_file.write_text( '[section]\nkey = "value"' )

            result = await async_process_config_file( config_file )
            assert result.key == 'value'

When to Mock
-------------------------------------------------------------------------------

* **Third-party libraries**: Some provide their own mocks (e.g., ``httpx``
  mock transport). Prefer these over writing custom mocks.

* **External services**: Mock network calls, database connections, etc.

* **Complex object creation**: When real objects are expensive to create.

Example with third-party mock::

    import httpx

    def test_http_client():
        def handler( request ):
            return httpx.Response( 200, json = { "result": "success" } )

        transport = httpx.MockTransport( handler )
        client = httpx.Client( transport = transport )

        response = client.get( "https://example.com/api" )
        assert response.json() == { "result": "success" }

When to Patch
-------------------------------------------------------------------------------

Avoid patching when possible. When necessary, only patch standard library
and external packages, and document the justification.

Note: ``importlib_metadata`` is a third-party package that maintains forward
compatibility with the latest ``importlib.metadata`` in the stdlib.

Testing Strategy by Code Type
===============================================================================

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Code Type
     - Strategy
     - Key Points
   * - **Sync Filesystem**
     - ``pyfakefs`` with ``Patcher()``
     - Fast, preferred for most file operations
   * - **Async Operations**
     - Real temp directories
     - ``aiofiles`` bypasses ``pyfakefs`` thread pool
   * - **Business Logic**
     - Dependency injection
     - Inject dependencies via constructor or method parameters
   * - **Third-Party Boundaries**
     - Mocking or case-by-case patching
     - Use library-provided mocks when available
   * - **Abstract Methods**
     - ``# pragma: no cover``
     - Apply to ``NotImplementedError`` lines only
   * - **Cross-Platform**
     - ``pathlib.Path`` with ``.resolve()`` and ``.samefile()``
     - Use ``Path.resolve()`` to unfurl symlinks; ``.samefile()`` for comparisons on Windows

Development Environment
===============================================================================

* **Always use hatch environment** for all testing commands::

    hatch --env develop run pytest          # run tests
    hatch --env develop run linters         # run linters
    hatch --env develop run testers         # run full test suite with coverage

* **Test performance**: The elapsed time reported by ``pytest`` should be
  under two seconds for the full test suite.

Test Code Standards
===============================================================================

Docstring Guidelines
-------------------------------------------------------------------------------

* **Describe behavior**, not function names
* **Keep headlines single-line** (don't spill across lines)
* **Good**: ``''' Error interceptor returns Value for successful awaitable. '''``
* **Bad**: ``''' intercept_error_async returns Value for successful awaitable. '''``

Code Style
-------------------------------------------------------------------------------

* Follow the project :doc:`code style guide <style>` for all test code
* **Mark slow tests** with ``@pytest.mark.slow``
* **Narrow try blocks** around exception-raising statements only

Advanced Testing Patterns
===============================================================================

Frame Inspection Testing
-------------------------------------------------------------------------------

Mock frame chains for call stack simulation (document justification)::

    def test_caller_discovery():
        # Mock frame chain simulating call stack
        external_frame = MagicMock()
        external_frame.f_code.co_filename = '/external/caller.py'
        external_frame.f_back = None

        internal_frame = MagicMock()
        internal_frame.f_code.co_filename = '/internal/module.py'
        internal_frame.f_back = external_frame

        with patch( 'inspect.currentframe', return_value = internal_frame ):
            result = module._discover_invoker_location()
            assert result == Path( '/external' )

Resource Management
-------------------------------------------------------------------------------

Use ``ExitStack`` for multiple temporary resources::

    from contextlib import ExitStack

    def test_multiple_temp_files():
        with ExitStack() as stack:
            temp1 = stack.enter_context(
                tempfile.NamedTemporaryFile( mode = 'w', delete = False ) )
            temp2 = stack.enter_context(
                tempfile.NamedTemporaryFile( mode = 'w', delete = False ) )
            # Both files cleaned up automatically

Error Simulation and Recovery
-------------------------------------------------------------------------------

Test error conditions and recovery paths::

    def safe_config_edit( config ):
        try:
            config[ 'application' ][ 'safe_mode' ] = True
        except Exception:
            config[ 'fallback' ] = True  # Apply fallback

    @pytest.mark.asyncio
    async def test_error_recovery():
        async with contextlib.AsyncExitStack() as exits:
            result = await prepare_with_config(
                exits, configedits = ( safe_config_edit, ) )
            assert result.configuration.get( 'fallback' )

Performance Optimization
===============================================================================

Strategies
-------------------------------------------------------------------------------

* **Avoid subprocess calls** when possible
* **Use pyfakefs for most filesystem tests** → Significant performance improvement
* **Minimize patching** → Maintain architecture integrity
* **Accept some real I/O for complex async operations** → Hybrid approach

Coverage Guidelines
===============================================================================

When to Use ``# pragma: no cover``
-------------------------------------------------------------------------------

* **Abstract methods** with ``NotImplementedError``
* **Defensive code** that's impossible to trigger
* **Platform-specific branches** that can't be tested in current environment
* **Last resort only** - prefer dependency injection

100% Coverage Standards
-------------------------------------------------------------------------------

Target 100% line and branch coverage systematically::

    @pytest.mark.asyncio
    async def test_development_mode_missing_package():
        ''' Prepare triggers development mode for missing package. '''
        with patch( 'importlib_metadata.packages_distributions', return_value = {} ):
            info = await module.prepare( 'nonexistent-package' )
            assert info.editable is True  # Development mode verified

Every line and branch should be covered by tests. Use ``# pragma: no cover``
only as a last resort.

Pre-Commit Validation
===============================================================================

**Always run validation before committing** to avoid Git hook failures::

    hatch --env develop run linters         # Check code style and quality
    hatch --env develop run testers         # Run full test suite with coverage

Git hooks will run these validations automatically, but running them manually
first saves turnaround time from CI failures.

Troubleshooting Common Issues
===============================================================================

1. **AttributeImmutability errors** → Use dependency injection instead of patching
2. **aiofiles not working with pyfakefs** → Fall back to real temp directories
3. **Test parameter conflicts** → Use ``Patcher()`` context manager, not ``@patchfs``
4. **Line number shifts in bulk editing** → Work from back to front

Decision Framework
===============================================================================

If you can't test something without monkey-patching:

1. **Try dependency injection** patterns above
2. **Check if interface supports injection** extension
3. **Consider available mocks** from third-party libraries
4. **Discuss design and justification** with team
5. **Last resort** - apply ``# pragma: no cover`` with justification

The goal is testable code through good design, not circumventing the architecture.

Benefits of This Approach
===============================================================================

1. **Realistic testing** - appropriate resource use catches more bugs
2. **Flexible code** - dependency injection improves design
3. **Maintainable tests** - less fragile than monkey-patching
4. **Preserved architecture** - immutability provides thread safety
5. **Optimized performance** - strategic use of in-memory filesystems
6. **Comprehensive coverage** - systematic targeting of uncovered branches
