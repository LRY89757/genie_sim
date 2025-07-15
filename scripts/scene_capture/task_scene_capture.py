#!/usr/bin/env python3
"""
Script to capture scene images from task JSON files
Usage: python task_scene_capture.py --task_json <path_to_json> --output_dir <output_dir>
"""

import argparse
import os
import sys
import json
import cv2
import numpy as np
import time
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from robot.isaac_sim.client import Rpc_Client
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
    path_parts = prim_path.split("/")
    if "Head_Camera" in prim_path:
        return "head"
    elif "Right_Camera" in prim_path:
        return "hand_right"
    elif "Left_Camera" in prim_path:
        return "hand_left"
    else:
        return path_parts[-1].lower()

def capture_scene_images(task_json_path, output_dir="scene_images", client_host="localhost:50051"):
    """
    Capture scene images from task JSON configuration
    
    Args:
        task_json_path: Path to task JSON file
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
        
        # Reset to ensure clean state
        print("Resetting scene...")
        rpc_client.reset()
        time.sleep(2)
        
        # Get camera list
        camera_list = extract_camera_list(task_config)
        print(f"Capturing from cameras: {camera_list}")
        
        # Capture images from each camera
        captured_images = {}
        for camera_prim in camera_list:
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
                    rgb_path = os.path.join(output_path, rgb_filename)
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
                    depth_path = os.path.join(output_path, depth_filename)
                    cv2.imwrite(depth_path, depth_image_16)
                    print(f"Saved depth image: {depth_path}")
                    
                    captured_images[camera_name]["depth_path"] = depth_path
                
            except Exception as e:
                print(f"Error capturing from {camera_prim}: {e}")
                continue
        
        # Save metadata
        metadata = {
            "task_name": task_name,
            "task_json_path": task_json_path,
            "robot_config": robot_cfg,
            "scene_usd": scene_usd,
            "robot_init_position": init_position,
            "robot_init_rotation": init_rotation,
            "cameras": captured_images,
            "capture_time": time.time()
        }
        
        metadata_path = os.path.join(output_path, "capture_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nScene capture completed!")
        print(f"Images saved to: {output_path}")
        print(f"Metadata saved to: {metadata_path}")
        
        # Display summary
        print(f"\nCaptured {len(captured_images)} camera views:")
        for camera_name, info in captured_images.items():
            print(f"  - {camera_name}: {info['rgb_path']}")
            if 'depth_path' in info:
                print(f"    Depth: {info['depth_path']}")
        
        return True
        
    except Exception as e:
        print(f"Error during scene capture: {e}")
        return False
    
    finally:
        # Clean up
        try:
            rpc_client.Exit()
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description="Capture scene images from task JSON files")
    parser.add_argument("--task_json", required=True, help="Path to task JSON file")
    parser.add_argument("--output_dir", default="scene_images", help="Output directory for images")
    parser.add_argument("--client_host", default="localhost:50051", help="gRPC server host")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.task_json):
        print(f"Error: Task JSON file not found: {args.task_json}")
        return 1
    
    success = capture_scene_images(
        task_json_path=args.task_json,
        output_dir=args.output_dir,
        client_host=args.client_host
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 
