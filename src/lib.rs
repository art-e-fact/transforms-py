use core::time::Duration;
use pyo3::prelude::*;
use transforms::{
    Registry, errors::TransformError, geometry::{Quaternion, Transform, Vector3, quaternion}, time::Timestamp
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

#[pyclass]
struct PyRegistry {
    inner: Registry,
}

#[pymethods]
impl PyRegistry {
    #[new]
    fn new(max_age_secs: u64) -> Self {
        PyRegistry {
            inner: Registry::new(Duration::from_secs(max_age_secs)),
        }
    }

    fn add_transform(
        &mut self,
        x: f64,
        y: f64,
        z: f64,
        qx: f64,
        qy: f64,
        qz: f64,
        qw: f64,
        timestamp: u128,
        parent: String,
        child: String,
    ) {
        println!("Adding transform from {} -> {} at timestamp {}\n", parent, child, timestamp);
        let transform = Transform {
            translation: Vector3::new(x, y, z),
            rotation: Quaternion { x: qx, y: qy, z: qz, w: qw },
            timestamp: Timestamp { t: timestamp },
            parent,
            child,
        };
        self.inner.add_transform(transform);
    }

    fn get_transform(&mut self, from: String, to: String, timestamp: u128) -> PyResult<Option<(f64, f64, f64, f64, f64, f64, f64, u128, String, String)>> {
        let ts = Timestamp { t: timestamp };
        println!("Getting transform from {} -> {} at timestamp {}\n", from, to, timestamp);
        match self.inner.get_transform(&from, &to, ts) {
            Ok(t) => Ok(Some((
                t.translation.x,
                t.translation.y,
                t.translation.z,
                t.rotation.x,
                t.rotation.y,
                t.rotation.z,
                t.rotation.w,
                t.timestamp.t,
                t.parent.clone(),
                t.child.clone(),
            ))),
            Err(e) => {
                println!("Error retrieving transform: {}", e);
                Ok(None)
            },
        }
    }
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_bin, m)?)?;
    m.add_function(wrap_pyfunction!(hello_transforms, m)?)?;
    m.add_class::<PyRegistry>()?;
    Ok(())
}
