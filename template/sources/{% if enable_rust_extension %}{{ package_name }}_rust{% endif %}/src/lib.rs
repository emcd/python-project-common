use pyo3::prelude::*;

/// Version of the Rust extension module.
/// Synchronized with Python package version via build script.
const VERSION: &str = env!("CRATE_VERSION");

#[pymodule]
fn _rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add("__version__", VERSION)?;
    Ok(())
}