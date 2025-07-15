#!/usr/bin/env python3
"""
Debug H5 Data Structure

This script investigates the H5 file to understand:
1. Joint name mappings
2. Quaternion format
3. Coordinate frame conventions
4. Data ranges and sanity checks
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import os

def analyze_h5_structure(h5_file_path):
    """Detailed analysis of H5 file structure and data"""
    print("="*80)
    print("🔍 DETAILED H5 DATA ANALYSIS")
    print("="*80)
    
    with h5py.File(h5_file_path, 'r') as f:
        # 1. Print complete structure
        print("1. COMPLETE H5 STRUCTURE:")
        def print_structure(name, obj):
            indent = "  " * (name.count('/') - 1)
            if isinstance(obj, h5py.Dataset):
                print(f"{indent}{name}: {obj.shape} {obj.dtype}")
            else:
                print(f"{indent}{name}/")
        
        f.visititems(print_structure)
        
        # 2. Compare ACTION vs STATE data
        print("\n2. ACTION vs STATE COMPARISON:")
        
        # Joint positions
        action_joints = f['action/joint/position'][()]  # [697, 34]
        state_joints = f['state/joint/position'][()]    # [697, 34]
        
        print(f"Action joints shape: {action_joints.shape}")
        print(f"State joints shape: {state_joints.shape}")
        
        # Compare a few samples
        print("\nSample joint comparison (first 3 timesteps, first 10 joints):")
        print("Timestep | Joint | Action    | State     | Diff")
        print("-" * 50)
        for t in range(3):
            for j in range(10):
                action_val = action_joints[t, j]
                state_val = state_joints[t, j]
                diff = abs(action_val - state_val)
                print(f"{t:8d} | {j:5d} | {action_val:8.4f} | {state_val:8.4f} | {diff:8.4f}")
        
        # 3. End-effector data analysis
        print("\n3. END-EFFECTOR DATA ANALYSIS:")
        
        # Action end-effector
        action_ee_pos = f['action/end/position'][()]      # [697, 2, 3]
        action_ee_orient = f['action/end/orientation'][()]  # [697, 2, 4]
        
        # State end-effector  
        state_ee_pos = f['state/end/position'][()]        # [697, 2, 3]
        state_ee_orient = f['state/end/orientation'][()]    # [697, 2, 4]
        
        print(f"Action EE position shape: {action_ee_pos.shape}")
        print(f"State EE position shape: {state_ee_pos.shape}")
        
        print("\n=== ACTION EE Position ranges ===")
        print(f"Action EE pos - X: [{np.min(action_ee_pos[:,:,0]):.3f}, {np.max(action_ee_pos[:,:,0]):.3f}]")
        print(f"Action EE pos - Y: [{np.min(action_ee_pos[:,:,1]):.3f}, {np.max(action_ee_pos[:,:,1]):.3f}]") 
        print(f"Action EE pos - Z: [{np.min(action_ee_pos[:,:,2]):.3f}, {np.max(action_ee_pos[:,:,2]):.3f}]")
        
        print("\n=== STATE EE Position ranges ===")
        print(f"State EE pos - X: [{np.min(state_ee_pos[:,:,0]):.3f}, {np.max(state_ee_pos[:,:,0]):.3f}]")
        print(f"State EE pos - Y: [{np.min(state_ee_pos[:,:,1]):.3f}, {np.max(state_ee_pos[:,:,1]):.3f}]") 
        print(f"State EE pos - Z: [{np.min(state_ee_pos[:,:,2]):.3f}, {np.max(state_ee_pos[:,:,2]):.3f}]")
        
        print("\n=== ACTION EE Orientation ranges ===")
        print(f"Action EE orient component 0: [{np.min(action_ee_orient[:,:,0]):.3f}, {np.max(action_ee_orient[:,:,0]):.3f}]")
        print(f"Action EE orient component 1: [{np.min(action_ee_orient[:,:,1]):.3f}, {np.max(action_ee_orient[:,:,1]):.3f}]")
        print(f"Action EE orient component 2: [{np.min(action_ee_orient[:,:,2]):.3f}, {np.max(action_ee_orient[:,:,2]):.3f}]")
        print(f"Action EE orient component 3: [{np.min(action_ee_orient[:,:,3]):.3f}, {np.max(action_ee_orient[:,:,3]):.3f}]")
        
        print("\n=== STATE EE Orientation ranges ===")
        print(f"State EE orient component 0: [{np.min(state_ee_orient[:,:,0]):.3f}, {np.max(state_ee_orient[:,:,0]):.3f}]")
        print(f"State EE orient component 1: [{np.min(state_ee_orient[:,:,1]):.3f}, {np.max(state_ee_orient[:,:,1]):.3f}]")
        print(f"State EE orient component 2: [{np.min(state_ee_orient[:,:,2]):.3f}, {np.max(state_ee_orient[:,:,2]):.3f}]")
        print(f"State EE orient component 3: [{np.min(state_ee_orient[:,:,3]):.3f}, {np.max(state_ee_orient[:,:,3]):.3f}]")
        
        # Check if quaternions are normalized
        action_quat_norms = np.linalg.norm(action_ee_orient, axis=2)
        state_quat_norms = np.linalg.norm(state_ee_orient, axis=2)
        print(f"\nAction Quaternion norms: [{np.min(action_quat_norms):.6f}, {np.max(action_quat_norms):.6f}]")
        print(f"State Quaternion norms: [{np.min(state_quat_norms):.6f}, {np.max(state_quat_norms):.6f}]")
        
        # Compare ACTION vs STATE end-effector data
        print("\n=== ACTION vs STATE EE COMPARISON ===")
        ee_pos_diff = np.abs(action_ee_pos - state_ee_pos)
        ee_orient_diff = np.abs(action_ee_orient - state_ee_orient)
        
        print(f"Max EE position difference: {np.max(ee_pos_diff):.6f}")
        print(f"Max EE orientation difference: {np.max(ee_orient_diff):.6f}")
        print(f"Mean EE position difference: {np.mean(ee_pos_diff):.6f}")
        print(f"Mean EE orientation difference: {np.mean(ee_orient_diff):.6f}")
        
        if np.max(ee_pos_diff) > 0.001 or np.max(ee_orient_diff) > 0.001:
            print("🎯 STATE EE data is DIFFERENT from ACTION EE data!")
            print("   → STATE data might contain real end-effector poses!")
        else:
            print("⚠️  STATE EE data is identical to ACTION EE data")
            print("   → Both are likely placeholder values")
        
        # 4. Joint position analysis
        print("\n4. JOINT POSITION ANALYSIS:")
        print(f"Action joint ranges per index:")
        for i in range(min(20, action_joints.shape[1])):  # First 20 joints
            joint_min = np.min(action_joints[:, i])
            joint_max = np.max(action_joints[:, i])
            joint_std = np.std(action_joints[:, i])
            print(f"  Joint {i:2d}: [{joint_min:7.4f}, {joint_max:7.4f}] (std: {joint_std:.4f})")
        
        # 5. Look for patterns in left/right arm indices
        print("\n5. ARM JOINT PATTERN ANALYSIS:")
        
        # Check if joints 5-11 (left) and 12-18 (right) show coordinated movement
        left_indices = list(range(5, 12))
        right_indices = list(range(12, 19))
        
        print("Left arm joints (5-11) sample values:")
        for t in [0, 100, 200, 300]:
            left_vals = action_joints[t, left_indices]
            print(f"  Timestep {t}: {[f'{v:.3f}' for v in left_vals]}")
            
        print("Right arm joints (12-18) sample values:")
        for t in [0, 100, 200, 300]:
            right_vals = action_joints[t, right_indices]
            print(f"  Timestep {t}: {[f'{v:.3f}' for v in right_vals]}")
        
        # 6. Sample transformation matrices
        print("\n6. SAMPLE TRANSFORMATION MATRIX ANALYSIS:")
        
        # Show a few sample end-effector poses
        for t in [0, 100, 200]:
            print(f"\nTimestep {t}:")
            for arm in [0, 1]:  # left, right
                arm_name = "LEFT" if arm == 0 else "RIGHT"
                
                action_pos = action_ee_pos[t, arm]
                action_quat = action_ee_orient[t, arm]
                state_pos = state_ee_pos[t, arm]
                state_quat = state_ee_orient[t, arm]
                
                print(f"  {arm_name} arm:")
                print(f"    ACTION - Position: [{action_pos[0]:.4f}, {action_pos[1]:.4f}, {action_pos[2]:.4f}]")
                print(f"    ACTION - Quaternion: [{action_quat[0]:.4f}, {action_quat[1]:.4f}, {action_quat[2]:.4f}, {action_quat[3]:.4f}]")
                print(f"    STATE  - Position: [{state_pos[0]:.4f}, {state_pos[1]:.4f}, {state_pos[2]:.4f}]")
                print(f"    STATE  - Quaternion: [{state_quat[0]:.4f}, {state_quat[1]:.4f}, {state_quat[2]:.4f}, {state_quat[3]:.4f}]")
        
        return {
            'action_joints': action_joints,
            'state_joints': state_joints,
            'action_ee_pos': action_ee_pos,
            'action_ee_orient': action_ee_orient,
            'state_ee_pos': state_ee_pos,
            'state_ee_orient': state_ee_orient
        }


def check_quaternion_format(action_orientations, state_orientations):
    """Check if quaternions are in [w,x,y,z] or [x,y,z,w] format"""
    print("\n7. QUATERNION FORMAT DETECTION:")
    
    # Sample some quaternions from ACTION data
    sample_action_quats = action_orientations[:10, :, :]  # First 10 timesteps, both arms
    sample_state_quats = state_orientations[:10, :, :]
    
    print("ACTION quaternions (first 5 timesteps, both arms):")
    for t in range(5):
        for arm in range(2):
            q = sample_action_quats[t, arm]
            print(f"  T{t} Arm{arm}: [{q[0]:.4f}, {q[1]:.4f}, {q[2]:.4f}, {q[3]:.4f}]")
    
    print("\nSTATE quaternions (first 5 timesteps, both arms):")
    for t in range(5):
        for arm in range(2):
            q = sample_state_quats[t, arm]
            print(f"  T{t} Arm{arm}: [{q[0]:.4f}, {q[1]:.4f}, {q[2]:.4f}, {q[3]:.4f}]")
    
    # Check ACTION quaternion format
    print("\n=== ACTION Quaternion Analysis ===")
    abs_means_action = np.mean(np.abs(action_orientations), axis=(0, 1))
    print(f"Mean absolute values per component: {abs_means_action}")
    print(f"Likely 'w' component index: {np.argmax(abs_means_action)}")
    
    w_candidates_action = []
    for i in range(4):
        component_vals = action_orientations[:, :, i].flatten()
        large_vals = np.sum(np.abs(component_vals) > 0.7)  # Count values suggesting w component
        w_candidates_action.append(large_vals)
    
    print(f"Components with |value| > 0.7 (suggesting w): {w_candidates_action}")
    print(f"Most likely w index: {np.argmax(w_candidates_action)}")
    
    # Check STATE quaternion format
    print("\n=== STATE Quaternion Analysis ===")
    abs_means_state = np.mean(np.abs(state_orientations), axis=(0, 1))
    print(f"Mean absolute values per component: {abs_means_state}")
    print(f"Likely 'w' component index: {np.argmax(abs_means_state)}")
    
    w_candidates_state = []
    for i in range(4):
        component_vals = state_orientations[:, :, i].flatten()
        large_vals = np.sum(np.abs(component_vals) > 0.7)  # Count values suggesting w component
        w_candidates_state.append(large_vals)
    
    print(f"Components with |value| > 0.7 (suggesting w): {w_candidates_state}")
    print(f"Most likely w index: {np.argmax(w_candidates_state)}")


def plot_joint_trajectories(joint_data, joint_indices, title):
    """Plot joint trajectories for specific indices"""
    plt.figure(figsize=(15, 10))
    
    for i, joint_idx in enumerate(joint_indices):
        plt.subplot(3, 3, i+1)
        plt.plot(joint_data[:, joint_idx])
        plt.title(f'Joint {joint_idx}')
        plt.xlabel('Timestep')
        plt.ylabel('Position (rad)')
        plt.grid(True)
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()


def main():
    # Default H5 file path
    # h5_file_path = "output/recording_data/curobo_restock_supermarket_items/5/aligned_joints.h5"
    h5_file_path = "output/recording_data/iros_pack_in_the_supermarket/1/aligned_joints.h5"
    
    if len(sys.argv) > 1:
        h5_file_path = sys.argv[1]
    
    if not os.path.exists(h5_file_path):
        print(f"❌ H5 file not found: {h5_file_path}")
        return
    
    print(f"🔍 Analyzing H5 file: {h5_file_path}")
    
    # Perform detailed analysis
    data = analyze_h5_structure(h5_file_path)
    
    # Check quaternion format
    check_quaternion_format(data['action_ee_orient'], data['state_ee_orient'])
    
    # Plot joint trajectories
    left_indices = list(range(5, 12))
    right_indices = list(range(12, 19))
    
    print(f"\n📊 Plotting joint trajectories...")
    plot_joint_trajectories(data['action_joints'], left_indices, "Left Arm Joints (5-11)")
    plot_joint_trajectories(data['action_joints'], right_indices, "Right Arm Joints (12-18)")


if __name__ == "__main__":
    main() 
