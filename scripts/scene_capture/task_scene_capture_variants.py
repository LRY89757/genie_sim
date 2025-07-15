#!/usr/bin/env python3
"""
Script to capture scene images from multiple task variants using TaskGenerator
Usage: python task_scene_capture_variants.py --task_json <path_to_json> --num_variants <number> --output_dir <output_dir>
"""

import argparse
import os
import sys
import json
import cv2
import numpy as np
import time
import tempfile
import shutil
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from robot.isaac_sim.client import Rpc_Client
from layout.task_generate import TaskGenerator
import base_utils

def load_task_json(json_path):
    """Load and parse task JSON file"""
    with open(json_path, 'r') as f:
        task_config = json.load(f)
    return task_config

def extract_camera_list(task_config):
    """Extract camera list from task configuration"""
    camera_list = []
    
    # Try to get from recording_setting first
    if "recording_setting" in task_config and "camera_list" in task_config["recording_setting"]:
        camera_list = task_config["recording_setting"]["camera_list"]
    else:
        # Default camera list for G1 robot
        camera_list = [
            "/G1/head_link2/Head_Camera",
            "/G1/gripper_r_base_link/Right_Camera", 
            "/G1/gripper_l_base_link/Left_Camera"
        ]
    
    return camera_list

def get_camera_name(prim_path):
    """Convert camera prim path to file name"""
    if "Head_Camera" in prim_path:
        return "head"
    elif "Right_Camera" in prim_path:
        return "hand_right"
    elif "Left_Camera" in prim_path:
        return "hand_left"
    elif "FrontFisheye" in prim_path:
        return "front_fisheye"
    elif "Overview" in prim_path:
        return "overview"
    elif "TopDown" in prim_path:
        return "top_down"
    elif "SideView" in prim_path:
        return "side_view"
    else:
        return prim_path.split("/")[-1].lower()

def calculate_scene_bounds(rpc_client, objects_added):
    """Calculate bounding box of all objects in the scene"""
    if not objects_added:
        # Default bounds if no objects
        return np.array([-2, -2, 0]), np.array([2, 2, 2])
    
    min_bounds = np.array([float('inf')] * 3)
    max_bounds = np.array([float('-inf')] * 3)
    
    for obj_id in objects_added:
        try:
            prim_path = f"/World/Objects/{obj_id}"
            response = rpc_client.GetObjectAABB(prim_path)
            
            obj_min = np.array([response.bbox[0], response.bbox[1], response.bbox[2]])
            obj_max = np.array([response.bbox[3], response.bbox[4], response.bbox[5]])
            
            min_bounds = np.minimum(min_bounds, obj_min)
            max_bounds = np.maximum(max_bounds, obj_max)
            
        except Exception as e:
            print(f"Warning: Could not get bounds for object {obj_id}: {e}")
            continue
    
    # If no valid bounds found, use defaults
    if np.any(np.isinf(min_bounds)) or np.any(np.isinf(max_bounds)):
        return np.array([-2, -2, 0]), np.array([2, 2, 2])
    
    return min_bounds, max_bounds

def create_strategic_cameras(rpc_client, objects_added):
    """Create strategic camera viewpoints around the scene"""
    
    # Calculate scene bounds
    min_bounds, max_bounds = calculate_scene_bounds(rpc_client, objects_added)
    scene_center = (min_bounds + max_bounds) / 2
    scene_size = max_bounds - min_bounds
    max_dimension = np.max(scene_size)
    
    print(f"Scene center: {scene_center}")
    print(f"Scene size: {scene_size}")
    print(f"Max dimension: {max_dimension}")
    
    strategic_cameras = []
    
    # Front Fisheye Camera - positioned in front of scene with wide FOV
    front_distance = max(3.0, max_dimension * 1.5)
    front_position = scene_center + np.array([front_distance, 0, scene_size[2] * 0.3])
    front_target = scene_center
    
    try:
        # Create fisheye camera with wide field of view
        rsp = rpc_client.CreateCamera(
            prim_path="/World/Cameras/FrontFisheye",
            position=front_position.tolist(),
            target=front_target.tolist(),
            fov=120.0,  # Wide fisheye field of view
            resolution=[512, 512]
        )
        strategic_cameras.append("/World/Cameras/FrontFisheye")
        print(f"Created front fisheye camera at position: {front_position}")
    except Exception as e:
        print(f"Warning: Could not create front fisheye camera: {e}")
    
    # Overview Camera - isometric view
    overview_distance = max(4.0, max_dimension * 2.0)
    overview_position = scene_center + np.array([overview_distance * 0.7, overview_distance * 0.7, overview_distance * 0.5])
    
    try:
        rsp = rpc_client.CreateCamera(
            prim_path="/World/Cameras/Overview",
            position=overview_position.tolist(),
            target=scene_center.tolist(),
            fov=60.0,
            resolution=[512, 512]
        )
        strategic_cameras.append("/World/Cameras/Overview")
        print(f"Created overview camera at position: {overview_position}")
    except Exception as e:
        print(f"Warning: Could not create overview camera: {e}")
    
    # Top-Down Camera
    topdown_height = max(3.0, scene_size[2] + max_dimension * 1.0)
    topdown_position = scene_center + np.array([0, 0, topdown_height])
    
    try:
        rsp = rpc_client.CreateCamera(
            prim_path="/World/Cameras/TopDown",
            position=topdown_position.tolist(),
            target=scene_center.tolist(),
            fov=90.0,
            resolution=[512, 512]
        )
        strategic_cameras.append("/World/Cameras/TopDown")
        print(f"Created top-down camera at position: {topdown_position}")
    except Exception as e:
        print(f"Warning: Could not create top-down camera: {e}")
    
    # Side View Camera
    side_distance = max(3.0, max_dimension * 1.5)
    side_position = scene_center + np.array([0, side_distance, scene_size[2] * 0.5])
    
    try:
        rsp = rpc_client.CreateCamera(
            prim_path="/World/Cameras/SideView", 
            position=side_position.tolist(),
            target=scene_center.tolist(),
            fov=60.0,
            resolution=[512, 512]
        )
        strategic_cameras.append("/World/Cameras/SideView")
        print(f"Created side view camera at position: {side_position}")
    except Exception as e:
        print(f"Warning: Could not create side view camera: {e}")
    
    print(f"Created {len(strategic_cameras)} strategic cameras")
    return strategic_cameras

def generate_task_variants(task_config, num_variants, temp_dir):
    """Generate multiple task variants using TaskGenerator"""
    print(f"Generating {num_variants} task variants...")
    
    # Create TaskGenerator
    task_generator = TaskGenerator(task_config)
    
    # Generate variants
    task_generator.generate_tasks(
        save_path=temp_dir,
        task_num=num_variants,
        task_name="variant"
    )
    
    # Load generated variant files
    variant_files = []
    for i in range(num_variants):
        variant_file = os.path.join(temp_dir, f"variant_{i}.json")
        if os.path.exists(variant_file):
            variant_files.append(variant_file)
    
    print(f"Successfully generated {len(variant_files)} variants")
    return variant_files

def setup_scene_for_variant(rpc_client, variant_config):
    """Setup scene with objects from variant configuration"""
    print("Setting up scene with variant objects...")
    
    # Reset scene first
    rpc_client.reset()
    time.sleep(2)
    
    # Add objects from variant
    objects_added = []
    if "objects" in variant_config:
        for obj in variant_config["objects"]:
            if obj["object_id"] == "fix_pose":
                continue  # Skip fix_pose objects
            
            try:
                # Get object info
                obj_id = obj["object_id"]
                position = obj["position"]
                quaternion = obj["quaternion"]
                
                # Get object path from data_info_dir
                data_info_dir = obj.get("data_info_dir", "")
                if data_info_dir:
                    # Extract relative path for USD
                    rel_path = data_info_dir.replace(os.path.dirname(os.path.dirname(__file__)) + "/assets/", "")
                    usd_path = f"{rel_path}/Aligned.usd"
                else:
                    # Fallback to generic object
                    usd_path = f"objects/generic/{obj_id}.usd"
                
                prim_path = f"/World/Objects/{obj_id}"
                
                # Get object properties
                color = obj.get("color", [0.8, 0.8, 0.8])
                scale = obj.get("scale", [1.0, 1.0, 1.0])
                mass = obj.get("mass", 1.0)
                
                print(f"Adding object: {obj_id} at position {position}")
                
                # Add object to scene
                response = rpc_client.add_object(
                    usd_path=usd_path,
                    prim_path=prim_path,
                    label_name=obj_id,
                    target_position=position,
                    target_quaternion=quaternion,
                    target_scale=scale,
                    color=color,
                    material="Plastic",
                    mass=mass
                )
                
                objects_added.append(obj_id)
                
            except Exception as e:
                print(f"Warning: Failed to add object {obj_id}: {e}")
                continue
    
    # Wait for objects to settle
    time.sleep(3)
    print(f"Added {len(objects_added)} objects to scene")
    return objects_added

def capture_variant_images(rpc_client, variant_config, variant_idx, output_dir):
    """Capture images from a specific task variant"""
    
    # Setup scene with variant objects
    objects_added = setup_scene_for_variant(rpc_client, variant_config)
    
    # Create strategic cameras based on object positions
    strategic_cameras = create_strategic_cameras(rpc_client, objects_added)
    
    # Create variant output directory
    variant_dir = os.path.join(output_dir, f"variant_{variant_idx}")
    os.makedirs(variant_dir, exist_ok=True)
    
    # Get robot camera list
    robot_camera_list = extract_camera_list(variant_config)
    
    # Combine robot cameras with strategic cameras
    all_cameras = robot_camera_list + strategic_cameras
    print(f"Capturing from cameras: {all_cameras}")
    
    # Capture images from each camera
    captured_images = {}
    for camera_prim in all_cameras:
        try:
            print(f"Capturing image from: {camera_prim}")
            
            # Capture frame
            response = rpc_client.capture_frame(camera_prim_path=camera_prim)
            
            # Get camera info
            cam_info = {
                "width": response.color_info.width,
                "height": response.color_info.height,
                "fx": response.color_info.fx,
                "fy": response.color_info.fy,
                "ppx": response.color_info.ppx,
                "ppy": response.color_info.ppy,
            }
            
            # Convert RGB image
            if response.color_image.data:
                rgb_data = np.frombuffer(response.color_image.data, dtype=np.uint8)
                rgb_image = rgb_data.reshape(cam_info["height"], cam_info["width"], 4)[:, :, :3]
                
                # Convert BGR to RGB for OpenCV
                rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                
                # Save RGB image
                camera_name = get_camera_name(camera_prim)
                rgb_filename = f"{camera_name}.jpg"
                rgb_path = os.path.join(variant_dir, rgb_filename)
                cv2.imwrite(rgb_path, rgb_image)
                print(f"Saved RGB image: {rgb_path}")
                
                captured_images[camera_name] = {
                    "rgb_path": rgb_path,
                    "camera_info": cam_info,
                    "prim_path": camera_prim
                }
            
            # Convert depth image if available
            if response.depth_image.data:
                depth_data = np.frombuffer(response.depth_image.data, dtype=np.float32)
                depth_image = depth_data.reshape(cam_info["height"], cam_info["width"])
                
                # Convert to 16-bit for saving
                depth_image_16 = (depth_image * 1000).astype(np.uint16)
                
                # Save depth image
                depth_filename = f"{camera_name}_depth.png"
                depth_path = os.path.join(variant_dir, depth_filename)
                cv2.imwrite(depth_path, depth_image_16)
                print(f"Saved depth image: {depth_path}")
                
                captured_images[camera_name]["depth_path"] = depth_path
            
        except Exception as e:
            print(f"Error capturing from {camera_prim}: {e}")
            continue
    
    # Save variant metadata
    variant_metadata = {
        "variant_index": variant_idx,
        "objects_added": objects_added,
        "cameras": captured_images,
        "variant_config": variant_config,
        "capture_time": time.time()
    }
    
    metadata_path = os.path.join(variant_dir, "variant_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(variant_metadata, f, indent=2)
    
    print(f"Variant {variant_idx} captured successfully")
    return captured_images

def capture_task_variants(task_json_path, num_variants=5, output_dir="task_variants", client_host="localhost:50051"):
    """
    Capture scene images from multiple task variants
    
    Args:
        task_json_path: Path to task JSON file
        num_variants: Number of variants to generate
        output_dir: Directory to save images
        client_host: gRPC server host
    """
    
    # Load task configuration
    print(f"Loading task configuration from: {task_json_path}")
    task_config = load_task_json(task_json_path)
    
    task_name = task_config.get("task", "unknown_task")
    print(f"Task: {task_name}")
    
    # Create output directory
    output_path = os.path.join(output_dir, task_name)
    os.makedirs(output_path, exist_ok=True)
    
    # Connect to Isaac Sim server
    print("Connecting to Isaac Sim server...")
    try:
        rpc_client = Rpc_Client(client_host)
    except Exception as e:
        print(f"Failed to connect to Isaac Sim server: {e}")
        print("Please make sure the server is running:")
        print("CUDA_VISIBLE_DEVICES=0 omni_python server/source/genie.sim.lab/raise_standalone_sim.py --headless")
        return False
    
    # Create temporary directory for variant files
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Get robot configuration
        robot_cfg = task_config.get("robot", {}).get("robot_cfg", "G1_120s.json")
        scene_usd = task_config.get("scene", {}).get("scene_usd", "")
        
        # Get robot initial pose
        robot_init_pose = task_config.get("robot", {}).get("robot_init_pose", {})
        
        # Handle different robot init pose formats
        if isinstance(robot_init_pose, dict):
            # Check for workspace-based positioning
            if "workspace_00" in robot_init_pose:
                init_position = robot_init_pose["workspace_00"]["position"]
                init_rotation = robot_init_pose["workspace_00"]["quaternion"]
            else:
                init_position = robot_init_pose.get("position", [0, 0, 0])
                init_rotation = robot_init_pose.get("quaternion", [1, 0, 0, 0])
        else:
            init_position = [0, 0, 0]
            init_rotation = [1, 0, 0, 0]
        
        print(f"Robot config: {robot_cfg}")
        print(f"Scene USD: {scene_usd}")
        print(f"Robot position: {init_position}")
        print(f"Robot rotation: {init_rotation}")
        
        # Initialize robot and scene
        print("Initializing robot and scene...")
        rpc_client.InitRobot(
            robot_cfg=robot_cfg,
            robot_usd=robot_cfg.replace('.json', '.usd'),
            scene_usd=scene_usd,
            init_position=init_position,
            init_rotation=init_rotation
        )
        
        # Wait for initialization
        time.sleep(3)
        
        # Generate task variants
        variant_files = generate_task_variants(task_config, num_variants, temp_dir)
        
        if not variant_files:
            print("Error: No variants were generated")
            return False
        
        # Capture images from each variant
        all_captured_images = {}
        for i, variant_file in enumerate(variant_files):
            print(f"\n--- Processing Variant {i+1}/{len(variant_files)} ---")
            
            # Load variant configuration
            with open(variant_file, 'r') as f:
                variant_config = json.load(f)
            
            # Capture images from this variant
            captured_images = capture_variant_images(
                rpc_client, variant_config, i, output_path
            )
            
            all_captured_images[f"variant_{i}"] = captured_images
        
        # Save overall summary
        summary_metadata = {
            "task_name": task_name,
            "task_json_path": task_json_path,
            "num_variants": len(variant_files),
            "robot_config": robot_cfg,
            "scene_usd": scene_usd,
            "robot_init_position": init_position,
            "robot_init_rotation": init_rotation,
            "variants": all_captured_images,
            "capture_time": time.time()
        }
        
        summary_path = os.path.join(output_path, "capture_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary_metadata, f, indent=2)
        
        print(f"\n=== Task Variant Capture Completed! ===")
        print(f"Task: {task_name}")
        print(f"Variants generated: {len(variant_files)}")
        print(f"Images saved to: {output_path}")
        print(f"Summary saved to: {summary_path}")
        
        # Display directory structure
        print(f"\nDirectory structure:")
        for i in range(len(variant_files)):
            variant_dir = os.path.join(output_path, f"variant_{i}")
            print(f"  {variant_dir}/")
            # Check for all possible camera types
            for camera_name in ["head", "hand_left", "hand_right", "front_fisheye", "overview", "top_down", "side_view"]:
                rgb_file = os.path.join(variant_dir, f"{camera_name}.jpg")
                if os.path.exists(rgb_file):
                    print(f"    - {camera_name}.jpg")
                    depth_file = os.path.join(variant_dir, f"{camera_name}_depth.png")
                    if os.path.exists(depth_file):
                        print(f"    - {camera_name}_depth.png")
        
        return True
        
    except Exception as e:
        print(f"Error during variant capture: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        
        # Clean up
        try:
            rpc_client.Exit()
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description="Capture scene images from multiple task variants")
    parser.add_argument("--task_json", required=True, help="Path to task JSON file")
    parser.add_argument("--num_variants", type=int, default=5, help="Number of variants to generate")
    parser.add_argument("--output_dir", default="task_variants", help="Output directory for images")
    parser.add_argument("--client_host", default="localhost:50051", help="gRPC server host")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.task_json):
        print(f"Error: Task JSON file not found: {args.task_json}")
        return 1
    
    success = capture_task_variants(
        task_json_path=args.task_json,
        num_variants=args.num_variants,
        output_dir=args.output_dir,
        client_host=args.client_host
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 
