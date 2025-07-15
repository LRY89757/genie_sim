# Scene Image Capture Tools

This directory contains tools for loading Isaac Sim scenes and capturing images from different viewpoints. These tools are useful for visualizing scenes, creating reference images, and debugging.

## Quick Start

### Method 1: Task Variant Capture (NEW - Recommended for Environment Variations)

Capture scene images from multiple randomly generated task variants:

```bash
# Generate 5 variants (default)
bash scripts/scene_capture/capture_task_variants.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json

# Generate 10 variants with custom output directory
bash scripts/scene_capture/capture_task_variants.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json 10 my_variants

# Generate 3 variants quickly
bash scripts/scene_capture/capture_task_variants.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json 3
```

This will:
1. Start Isaac Sim server on GPU 0
2. Load the base task configuration
3. **Generate multiple layout variants** with objects placed in different positions
4. For each variant: reset scene, place objects, capture images
5. Save images organized by variant (variant_0/, variant_1/, etc.)
6. Each variant contains: head.jpg, hand_left.jpg, hand_right.jpg + depth images
7. Clean up automatically

### Method 2: Single Task Scene Capture

Capture scene images directly from task JSON files (single layout):

```bash
# Basic usage - capture from task JSON
bash scripts/scene_capture/capture_task_scene.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json

# With custom output directory
bash scripts/scene_capture/capture_task_scene.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json my_task_images
```

This will:
1. Start Isaac Sim server on GPU 0
2. Load the scene and robot configuration from the JSON file
3. Position the robot at the initial pose
4. Capture images from robot cameras (head, left gripper, right gripper)
5. Save images as JPG files with depth as PNG
6. Clean up automatically

### Method 3: Generic Scene Capture

The easiest way to capture scene images from predefined tasks:

```bash
# Basic usage
bash scripts/scene_capture/capture_scene_images.sh 0 iros_pack_in_the_supermarket

# With custom output directory
bash scripts/scene_capture/capture_scene_images.sh 0 iros_pack_in_the_supermarket my_scene_images
```

This will:
1. Start Isaac Sim server on GPU 0
2. Load the specified task scene
3. Capture images from multiple viewpoints
4. Save images to the specified directory
5. Clean up automatically

### Method 4: Using Python Scripts Directly

For more control, you can run the Python scripts directly:

```bash
# Task variant capture (multiple random layouts)
python scripts/scene_capture/task_scene_capture_variants.py \
    --task_json benchmark/ader/eval_tasks/iros_stamp_the_seal.json \
    --num_variants 5 \
    --output_dir my_variants

# Task scene capture from JSON file (single layout)
python scripts/scene_capture/task_scene_capture.py \
    --task_json benchmark/ader/eval_tasks/iros_stamp_the_seal.json \
    --output_dir my_task_images

# Generic scene capture from predefined tasks
python scripts/scene_capture/scene_image_capture.py \
    --task_name iros_pack_in_the_supermarket \
    --output_dir my_images

# Simple scene capture
python scripts/scene_capture/simple_scene_capture.py
```

Note: Make sure Isaac Sim server is running before running Python scripts directly:
```bash
CUDA_VISIBLE_DEVICES=0 omni_python server/source/genie.sim.lab/raise_standalone_sim.py --headless &
sleep 40  # Wait for server to start
```

### Method 3: Simple Example

For basic understanding of the process:

```bash
# Start server first
/isaac-sim/python.sh server/source/genie.sim.lab/raise_standalone_sim.py --headless &
sleep 90

# Run simple example
/isaac-sim/python.sh scripts/scene_capture/simple_scene_capture.py
```

## Available Scripts

### 1. `task_scene_capture_variants.py` (NEW)
**Task variant capture tool with TaskGenerator**

Features:
- Uses TaskGenerator to create multiple random layout variants
- Generates different object placements for the same task
- Captures images from each variant showing environment diversity
- Perfect for seeing how tasks look with different object arrangements
- Saves organized by variant directories (variant_0/, variant_1/, etc.)
- Generates comprehensive metadata for each variant

Usage:
```bash
python scripts/scene_capture/task_scene_capture_variants.py --task_json <json_file> --num_variants <num> --output_dir <output_dir>
```

### 2. `task_scene_capture.py`
**Task-based scene capture tool (single layout)**

Features:
- Loads scene configuration directly from task JSON files
- Positions robot at correct initial pose from task configuration
- Captures from robot cameras (head, left gripper, right gripper)
- Saves RGB images as JPG and depth as PNG
- Generates metadata with camera parameters and task info
- Handles different robot configurations automatically

Usage:
```bash
python scripts/scene_capture/task_scene_capture.py --task_json <json_file> --output_dir <output_dir>
```

### 3. `capture_task_variants.sh` (NEW)
**Automated shell script for task variant capture**

Features:
- Automatically starts Isaac Sim server with GPU selection
- Handles variant generation and image capture
- Provides progress feedback and result summary
- Manages server lifecycle and cleanup
- Shows generated variants and sample images

Usage:
```bash
bash scripts/scene_capture/capture_task_variants.sh <gpu_num> <task_json> [num_variants] [output_dir]
```

### 4. `scene_image_capture.py`
**Full-featured scene capture tool**

Features:
- Loads any task scene from `benchmark/ader/eval_tasks/`
- Captures from multiple predefined viewpoints (front, top, side, robot perspective)
- Captures from robot's built-in cameras (head, left gripper, right gripper)
- Saves images as PNG files with camera metadata
- Generates summary JSON with capture details

Usage:
```bash
python scripts/scene_capture/scene_image_capture.py --task_name <task_name> --output_dir <output_dir>
```

### 6. `simple_scene_capture.py`
**Basic example for learning**

Features:
- Simple demonstration of core functionality
- Hardcoded scene loading
- Single camera viewpoint
- Minimal dependencies

Usage:
```bash
python scripts/scene_capture/simple_scene_capture.py
```

### 5. `capture_scene_images.sh`
**Automated shell script for predefined tasks**

Features:
- Automatically starts Isaac Sim server
- Handles GPU selection
- Automatic cleanup
- Error handling

Usage:
```bash
bash scripts/scene_capture/capture_scene_images.sh <gpu_num> <task_name> [output_dir]
```

## Output Structure

### Task Variant Capture Output

The variant capture tools create the following output structure:

```
task_variants/iros_stamp_the_seal/
├── variant_0/
│   ├── head.jpg                    # Head camera RGB
│   ├── head_depth.png              # Head camera depth
│   ├── hand_left.jpg               # Left gripper RGB
│   ├── hand_left_depth.png         # Left gripper depth
│   ├── hand_right.jpg              # Right gripper RGB
│   ├── hand_right_depth.png        # Right gripper depth
│   └── variant_metadata.json       # Variant info and object positions
├── variant_1/
│   ├── head.jpg                    # Same cameras, different object layout
│   ├── head_depth.png
│   ├── hand_left.jpg
│   ├── hand_left_depth.png
│   ├── hand_right.jpg
│   ├── hand_right_depth.png
│   └── variant_metadata.json
├── variant_2/
│   └── ... (similar structure)
└── capture_summary.json            # Overall capture summary
```

### Single Task Capture Output

The single task capture tools create the following output structure:

```
output_directory/
├── task_name_front_view.png           # Front viewpoint
├── task_name_front_view_info.json     # Camera metadata
├── task_name_top_view.png             # Top-down viewpoint
├── task_name_top_view_info.json       # Camera metadata
├── task_name_side_view.png            # Side viewpoint
├── task_name_side_view_info.json      # Camera metadata
├── task_name_robot_head_view.png      # Robot perspective
├── task_name_robot_head_view_info.json
├── task_name_Head_Camera.png          # Robot head camera
├── task_name_Head_Camera_info.json
├── task_name_Left_Camera.png          # Left gripper camera
├── task_name_Left_Camera_info.json
├── task_name_Right_Camera.png         # Right gripper camera
├── task_name_Right_Camera_info.json
└── capture_summary.json               # Overall summary
```

## Camera Viewpoints

The script captures images from several predefined viewpoints:

1. **Front View**: 2m in front of origin, 1.5m high, looking down slightly
2. **Top View**: 3m above origin, looking straight down
3. **Side View**: 2m to the side, 1.5m high, looking toward center
4. **Robot Head View**: At robot head height, looking forward
5. **Robot Cameras**: Head, left gripper, and right gripper cameras

## Available Tasks

You can capture images from any task in `benchmark/ader/eval_tasks/`:

- `iros_pack_in_the_supermarket`
- `iros_clear_table_in_the_restaurant`
- `iros_make_a_sandwich`
- `genie_task_home_clean_desktop`
- `genie_task_home_pour_water`
- `curobo_restock_supermarket_items`
- And many more...

## Customization

### Adding Custom Viewpoints

Edit the `viewpoints` list in `scene_image_capture.py`:

```python
viewpoints = [
    {
        "name": "my_custom_view",
        "position": [1.0, 1.0, 2.0],  # [x, y, z] in meters
        "rotation": [0.7071, 0.0, 0.0, 0.7071],  # [w, x, y, z] quaternion
    },
    # ... add more viewpoints
]
```

### Changing Image Resolution

Modify the `width` and `height` parameters in `add_camera_viewpoint()`:

```python
response = self.robot.client.AddCamera(
    camera_prim_path,
    position,
    rotation,
    width=1920,   # Change resolution
    height=1080,  # Change resolution
    # ... other parameters
)
```

### Using Different Scenes

You can modify `simple_scene_capture.py` to use different scene files:

```python
rpc_client.InitRobot(
    robot_cfg="G1_120s.json",
    robot_usd="G1_120s/G1_120s.usd",
    scene_usd="your_custom_scene.usd"  # Change scene
)
```

## Troubleshooting

### Common Issues

1. **Server connection failed**: Make sure Isaac Sim server is running and accessible
2. **Scene not found**: Check that the task name exists in `benchmark/ader/eval_tasks/`
3. **Images are black**: Wait longer for the scene to load (increase sleep time)
4. **Permission errors**: Check that output directory is writable

### Debug Mode

For debugging, you can run the server in non-headless mode:

```bash
/isaac-sim/python.sh server/source/genie.sim.lab/raise_standalone_sim.py --record_img
```

This will show the Isaac Sim GUI window.

## Integration with Task Generation

The scene capture tools work with the existing task generation system:

1. `task_generate.py` creates task variants with different object positions
2. Scene capture tools can visualize these generated tasks
3. Images can be used to verify task setup and object placement

## Performance Tips

- Use `--headless` mode for faster rendering
- Reduce image resolution for faster capture
- Use GPU acceleration with `CUDA_VISIBLE_DEVICES`
- Process multiple tasks in batch for efficiency

## Examples

### Capture all available tasks:
```bash
for task in $(ls benchmark/ader/eval_tasks/*.json | xargs -n1 basename -s .json); do
    bash scripts/scene_capture/capture_scene_images.sh 0 $task "images_$task"
done
```

### Capture with specific GPU:
```bash
bash scripts/scene_capture/capture_scene_images.sh 1 iros_make_a_sandwich sandwich_images
```

### Custom output directory:
```bash
bash scripts/scene_capture/capture_scene_images.sh 0 genie_task_home_pour_water /tmp/scene_refs
``` 
