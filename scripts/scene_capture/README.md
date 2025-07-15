# Scene Image Capture Tools

This directory contains tools for loading Isaac Sim scenes and capturing images from different viewpoints. These tools are useful for visualizing scenes, creating reference images, and debugging.

## 🆕 Enhanced Camera System

The latest version includes **automatic strategic camera positioning** that calculates optimal viewpoints based on object locations in the scene. This ensures you capture the objects you actually want to see, not just random background!

### 📸 Camera Views Available:

#### Robot-Mounted Cameras:
- **`head.jpg`** - Robot's head camera view  
- **`hand_left.jpg`** - Left gripper camera view
- **`hand_right.jpg`** - Right gripper camera view

#### Strategic Scene Cameras:
- **`front_fisheye.jpg`** - ⭐ **NEW!** Wide-angle fisheye view from front of scene (120° FOV)
- **`overview.jpg`** - Isometric overview showing entire scene layout
- **`top_down.jpg`** - Bird's-eye view perfect for understanding object placement
- **`side_view.jpg`** - Profile view showing depth relationships

All cameras automatically include depth maps saved as `*_depth.png` files.

### How it Works:
1. **Scene Analysis**: Calculates bounding box of all objects in each variant
2. **Strategic Positioning**: Places cameras around the scene center at optimal distances  
3. **Smart Orientation**: Cameras automatically look at the center of object activity
4. **Adaptive Distance**: Camera distance scales with scene size for optimal framing
5. **Fisheye View**: Front fisheye provides ultra-wide perspective perfect for scene overview

## Tools

### 1. Task Variant Capture (`task_scene_capture_variants.py`)

Generates multiple randomized variants of a task and captures images from each variant showing different object layouts.

```bash
# Generate 5 variants with all camera views including front fisheye
python task_scene_capture_variants.py --task_json benchmark/ader/eval_tasks/iros_stamp_the_seal.json --num_variants 5

# Custom output directory
python task_scene_capture_variants.py --task_json my_task.json --num_variants 3 --output_dir my_captures
```

**Output Structure:**
```
task_variants/iros_stamp_the_seal/
├── variant_0/
│   ├── head.jpg + head_depth.png
│   ├── hand_left.jpg + hand_left_depth.png  
│   ├── hand_right.jpg + hand_right_depth.png
│   ├── front_fisheye.jpg + front_fisheye_depth.png  ⭐ NEW!
│   ├── overview.jpg + overview_depth.png
│   ├── top_down.jpg + top_down_depth.png
│   ├── side_view.jpg + side_view_depth.png
│   └── variant_metadata.json
├── variant_1/
│   └── (same structure, different object layout)
└── capture_summary.json
```

### 2. Shell Script Automation (`capture_task_variants.sh`)

```bash
# Usage: bash capture_task_variants.sh <GPU_ID> <TASK_JSON> [NUM_VARIANTS]
bash scripts/scene_capture/capture_task_variants.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json 5
```

## 🔧 Technical Details

### Camera Specifications:
- **Resolution**: 512x512 for all cameras
- **Front Fisheye FOV**: 120° (ultra-wide)
- **Other Cameras FOV**: 60-90° (standard)
- **Depth Format**: 16-bit PNG (millimeter precision)
- **RGB Format**: 8-bit JPG

### Automatic Positioning:
- **Front Fisheye**: Positioned 1.5x scene size in front, elevated slightly above objects
- **Overview**: Isometric angle (70% front, 70% side, 50% height relative to scene size)
- **Top-Down**: Directly above scene center at adaptive height
- **Side View**: Perpendicular to front view at scene edge

### Scene Analysis:
- Calculates object bounding boxes automatically
- Determines optimal camera distances based on scene size
- Centers all views on the area of object activity
- Handles empty scenes with sensible defaults

## 🚀 Use Cases

- **Dataset Creation**: Generate diverse training data with multiple viewpoints
- **Scene Debugging**: Verify object placement and scene setup
- **Progress Documentation**: Capture before/after states of tasks
- **Presentation Material**: Create compelling scene visualizations
- **Research**: Study object interactions from multiple perspectives

## 📋 Requirements

- Isaac Sim server running (`raise_standalone_sim.py`)
- Task JSON files with proper object definitions
- CUDA-compatible GPU for rendering

## 🔧 Configuration

Camera settings can be customized by modifying the `create_strategic_cameras()` function:

```python
# Example: Adjust fisheye FOV
rsp = rpc_client.CreateCamera(
    prim_path="/World/Cameras/FrontFisheye",
    fov=140.0,  # Even wider fisheye
    resolution=[1024, 1024]  # Higher resolution
)
``` 
