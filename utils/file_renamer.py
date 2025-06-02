import os
import shutil

def rename_photos(rankings, output_dir=None):
    """
    Rename photos according to their rankings and save to output directory.
    
    Args:
        rankings: List of tuples (photo_path, score) sorted by score (highest first)
        output_dir: Output directory path. If None, uses a subfolder "ranked_list" in the input directory
    """
    if not rankings:
        return
        
    # If output_dir is None, use a "ranked_list" subfolder in the input directory
    if output_dir is None:
        input_dir = os.path.dirname(rankings[0][0])
        output_dir = os.path.join(input_dir, "ranked_list")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for i, (photo_path, _) in enumerate(rankings):
        # Get original filename
        filename = os.path.basename(photo_path)
        
        # Split filename into name and extension
        name_parts = os.path.splitext(filename)
        ext = name_parts[1]  # File extension
        
        # Create new filename with rank
        rank_str = f"{i+1:03d}"  # Zero-padded rank (e.g., 001, 002, ...)
        new_filename = f"{rank_str}_{filename}"
        new_path = os.path.join(output_dir, new_filename)
        
        # If the new filename already exists, try with a different name
        counter = 1
        while os.path.exists(new_path):
            new_filename = f"{rank_str}_{counter}_{filename}"
            new_path = os.path.join(output_dir, new_filename)
            counter += 1
        
        try:
            # Use copy2 instead of rename to maintain original files
            shutil.copy2(photo_path, new_path)
            print(f"Copied and renamed: {filename} -> {new_filename}")
        except Exception as e:
            print(f"Error copying {filename}: {str(e)}")
