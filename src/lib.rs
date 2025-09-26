use pyo3::prelude::*;
use core::time::Duration;
use transforms::{
    geometry::{Quaternion, Transform, Vector3},
    time::Timestamp,
    Registry,
};

#[pyfunction]
fn hello_from_bin() -> String {
    "Hello from transforms-py!".to_string()
}

#[pyfunction]
fn hello_transforms() -> String {
    let mut registry = Registry::new(Duration::from_secs(60));
    let timestamp = Timestamp::now();

    // Create a transform from frame "base" to frame "sensor"
    let transform = Transform {
        translation: Vector3::new(1.0, 0.0, 0.0),
        rotation: Quaternion::identity(),
        timestamp,
        parent: "base".into(),
        child: "sensor".into(),
    };

    // Add the transform to the registry
    registry.add_transform(transform);

    // Retrieve the transform
    let result = registry.get_transform("base", "sensor", timestamp);

    match result {
        Ok(t) => format!(
            "Transform from 'base' to 'sensor': translation = {:?}, rotation = {:?}",
            t.translation, t.rotation
        ),
        Err(e) => format!("Error retrieving transform: {}", e),
    }
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_bin, m)?)?;
    m.add_function(wrap_pyfunction!(hello_transforms, m)?)?;
    Ok(())
}
