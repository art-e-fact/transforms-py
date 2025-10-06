from typing import List, Optional, Tuple
import numpy as np
import time
from transforms_py import PyRegistry
from posetree import CustomFramePoseTree, Transform


class TransformsPoseTree(CustomFramePoseTree):
    """My implementation of PoseTree to integrate with MyTransformManager"""

    def __init__(self, registry: PyRegistry):
        super().__init__()
        self._registry = registry

    def _get_transform(
        self, parent_frame: str, child_frame: str, timestamp: Optional[float] = None
    ) -> Transform:
        transform_data = self._registry.get_transform(
            parent_frame, child_frame, timestamp
        )
        if transform_data is None:
            raise KeyError(
                f"No transform found from {parent_frame} to {child_frame} at time {timestamp}"
            )
        tx, ty, tz, qx, qy, qz, qw, _ts, _parent, _child = transform_data
        return Transform.from_position_and_quaternion([tx, ty, tz], [qx, qy, qz, qw])


class TransformData:
    def __init__(
        self,
        num_frames=100,
        num_timesteps=1000,
        transforms_per_timestep=50,
        num_query_timestamps=100000,
    ):
        self.frames: List[str] = []
        self.links: List[Tuple[str, str]] = []

        assert num_frames >= transforms_per_timestep, (
            "Can't have more transforms per timestep than frames"
        )

        # Generate frames and links
        for i in range(num_frames):
            frame = f"F{i:03d}"
            parent_frame = np.random.choice(self.frames) if self.frames else None
            self.frames.append(frame)
            if parent_frame is None:
                continue
            self.links.append((str(parent_frame), frame))

        # Generate timestamps
        timestamps = [0]
        for _ in range(num_timesteps):
            average_delta = 3
            delta = np.random.normal(average_delta, average_delta * 0.1)
            delta = max(1, int(delta))
            if timestamps:
                timestamps.append(timestamps[-1] + delta)
            else:
                timestamps.append(delta)

        self.transforms = []

        for timestamp in timestamps:
            for link_idx in np.random.permutation(len(self.links)):
                link = self.links[link_idx]
                translation = np.random.normal(0, 10, size=3)
                rotation = np.random.normal(0, 1, size=4)
                rotation /= np.linalg.norm(rotation)  # Normalize to unit quaternion
                self.transforms.append(
                    (translation, rotation, timestamp, link[0], link[1])
                )

        timestamp_range = (np.min(timestamps), np.max(timestamps))
        self.query_timestamps = np.random.randint(
            timestamp_range[0], timestamp_range[1], size=num_query_timestamps
        )


def bench_transforms_py():
    registry = PyRegistry()

    transform_data = TransformData(
        # num_frames=4, num_timesteps=3, transforms_per_timestep=2, num_query_timestamps=3
    )
    print(
        f"Generated {len(transform_data.transforms)} transforms across {len(transform_data.frames)} frames and {len(transform_data.links)} links."
    )
    print(f"Frames: {transform_data.frames}")
    print(f"Links: {transform_data.links}")
    print(f"Query timestamps: {transform_data.query_timestamps}")

    # Measure insertion time
    start_time = time.time()
    for (
        translation,
        rotation,
        timestamp,
        parent_frame,
        child_frame,
    ) in transform_data.transforms:
        registry.add_transform(
            *translation, *rotation, timestamp, parent_frame, child_frame
        )
    end_time = time.time()
    print(f"Inserted transforms in {end_time - start_time:.2f} seconds")

    # Measure retrieval time
    start_time = time.time()
    for timestamp in transform_data.query_timestamps:
        for parent_frame, child_frame in transform_data.links:
            transform = registry.get_transform(parent_frame, child_frame, timestamp)

    end_time = time.time()
    print(f"Retrieved transforms in {end_time - start_time:.2f} seconds")

    pose_tree = TransformsPoseTree(registry)
    start_time = time.time()
    for timestamp in transform_data.query_timestamps:
        for parent_frame, child_frame in transform_data.links:
            transform = pose_tree.get_transform(
                parent_frame, child_frame, timestamp
            )
    end_time = time.time()
    print(f"PoseTree retrieved transforms in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    bench_transforms_py()
