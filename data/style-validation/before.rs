use pyo3::prelude::*;
use std::{
    collections::{HashMap, HashSet},
    sync::{Arc, Mutex},
};

// Test single-line and multi-line function definitions
fn simple_function(value: i32) -> i32 { value * 2 }

fn complex_function(
    first_argument: HashMap<String, i32>,
    second_argument: Vec<String>,
    third_argument: Option<Box<dyn Fn(i32) -> i32>>,
) -> Result<HashSet<i32>, String> {
    // Implementation
    Ok(HashSet::new())
}

// Test trait definitions and implementations
trait DataProcessor {
    fn process(&self, data: &[u8]) -> Vec<u8>;
    fn validate(&self, input: &str) -> bool { input.len() > 0 }
}

impl DataProcessor for BasicProcessor {
    fn process(
        &self,
        data: &[u8],
    ) -> Vec<u8> {
        data.to_vec()
    }

    fn validate(&self, input: &str) -> bool { !input.is_empty() }
}

// Test struct definitions and instantiation
struct Configuration {
    name: String,
    value: i32,
    processor: Box<dyn DataProcessor>,
}

struct ComplexStructure<T>
where
    T: Clone + Default,
{
    field1: Vec<T>,
    field2: HashMap<String, T>,
    field3: Option<Arc<Mutex<T>>>,
}

// Test match expressions
fn process_value(value: Option<i32>) -> i32 {
    match value {
        Some(v) if v > 0 => v * 2,
        Some(v) => v,
        None => 0,
    }
}

// Test array and slice operations
fn array_ops() {
    let array = [1..5, 6..10, 11..15];
    let slice = &array[1..3];
    let range = 0..10;
}

// Test doc comments and attributes
/// Processes Python data using Rust.
///
/// # Arguments
/// * `data` - Input data as bytes
/// * `config` - Processing configuration
///
/// # Returns
/// Processed data as bytes
#[pyfunction]
#[pyo3(name = "process_data")]
fn process_python_data(
    data: &[u8],
    config: HashMap<String, String>,
) -> PyResult<Vec<u8>> {
    // Processing implementation
    Ok(data.to_vec())
}

// Test macro invocations and nested expressions
lazy_static! {
    static ref GLOBAL_CONFIG: Arc<Mutex<Configuration>> = Arc::new(
        Mutex::new(Configuration {
            name: "default".to_string(),
            value: 42,
            processor: Box::new(BasicProcessor::default()),
        }),
    );
}

// Test complex type signatures
type ProcessorResult<T, E = Box<dyn std::error::Error>> =
    Result<Vec<T>, E>;

// Test impl blocks with where clauses
impl<T, U> DataConverter<T, U>
where
    T: From<U> + Clone,
    U: Default,
{
    fn convert(
        &self,
        input: Vec<U>,
    ) -> ProcessorResult<T> {
        input
            .into_iter()
            .map(T::from)
            .collect::<Vec<_>>()
    }
}

// Test closure formatting
fn with_closure() {
    let processor = |x: i32, y: i32| -> i32 { x + y };
    let mapped: Vec<_> = (0..10)
        .filter(|x| x % 2 == 0)
        .map(|x| x * 2)
        .collect();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_processing() -> Result<(), Box<dyn std::error::Error>> {
        let data = vec![1, 2, 3];
        let processed = process_python_data(
            &data,
            HashMap::from([
                ("mode".to_string(), "fast".to_string()),
                ("quality".to_string(), "high".to_string()),
            ]),
        )?;
        assert_eq!(data, processed);
        Ok(())
    }
}
