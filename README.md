# Artefacts Transforms PY

A python wrapper for the excellent [transform library](https://github.com/deniz-hofmeister/transforms)


### Release on Pypi

(Assumes you have Pypi account and setup correctly)

* Update the version in cargo.toml then:
```
uv venv --seed --python 3.11
uv run --extra dev maturin publish
```