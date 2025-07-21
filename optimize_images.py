#!/usr/bin/env python3
"""
Image optimization script for ZEYLANKA website
Reduces file sizes while maintaining acceptable quality
"""

import os
import shutil
from pathlib import Path

def optimize_with_ffmpeg(input_path, output_path, quality=75):
    """Optimize image using ffmpeg (available on most systems)"""
    try:
        cmd = f'ffmpeg -i "{input_path}" -q:v {quality} -y "{output_path}"'
        result = os.system(cmd)
        return result == 0
    except Exception as e:
        print(f"Error with ffmpeg: {e}")
        return False

def optimize_with_imagemagick(input_path, output_path, quality=75):
    """Optimize image using ImageMagick convert"""
    try:
        cmd = f'convert "{input_path}" -quality {quality} "{output_path}"'
        result = os.system(cmd)
        return result == 0
    except Exception as e:
        print(f"Error with ImageMagick: {e}")
        return False

def optimize_with_jpegoptim(input_path, output_path, quality=75):
    """Optimize image using jpegoptim"""
    try:
        # Copy first, then optimize in place
        shutil.copy2(input_path, output_path)
        cmd = f'jpegoptim --max={quality} "{output_path}"'
        result = os.system(cmd)
        return result == 0
    except Exception as e:
        print(f"Error with jpegoptim: {e}")
        return False

def get_file_size_kb(file_path):
    """Get file size in KB"""
    return os.path.getsize(file_path) / 1024

def optimize_image(input_path, backup_dir="backups"):
    """
    Optimize a single image file
    Creates backup and optimizes the original
    """
    file_path = Path(input_path)
    
    # Create backup directory if it doesn't exist
    backup_path = Path(backup_dir)
    backup_path.mkdir(exist_ok=True)
    
    # Create backup
    backup_file = backup_path / f"{file_path.stem}_backup{file_path.suffix}"
    shutil.copy2(input_path, backup_file)
    
    original_size = get_file_size_kb(input_path)
    print(f"Optimizing: {input_path} ({original_size:.1f}KB)")
    
    # Try different optimization methods
    temp_file = f"{input_path}.tmp"
    
    # Method 1: Try ffmpeg first (most common)
    if optimize_with_ffmpeg(input_path, temp_file, quality=78):
        shutil.move(temp_file, input_path)
        new_size = get_file_size_kb(input_path)
        print(f"  ✓ Optimized with ffmpeg: {new_size:.1f}KB ({((original_size-new_size)/original_size*100):.1f}% reduction)")
        return True
    
    # Method 2: Try ImageMagick
    if optimize_with_imagemagick(input_path, temp_file, quality=78):
        shutil.move(temp_file, input_path)
        new_size = get_file_size_kb(input_path)
        print(f"  ✓ Optimized with ImageMagick: {new_size:.1f}KB ({((original_size-new_size)/original_size*100):.1f}% reduction)")
        return True
    
    # Method 3: Try jpegoptim
    if optimize_with_jpegoptim(input_path, temp_file, quality=78):
        new_size = get_file_size_kb(input_path)
        print(f"  ✓ Optimized with jpegoptim: {new_size:.1f}KB ({((original_size-new_size)/original_size*100):.1f}% reduction)")
        return True
    
    # If all methods fail, restore from backup
    shutil.move(backup_file, input_path)
    print(f"  ✗ Could not optimize - restored original")
    return False

def main():
    """Main optimization function"""
    print("🎯 ZEYLANKA Image Optimization Script")
    print("=" * 50)
    
    # List of large images to optimize (over 100KB)
    large_images = [
        "images/1.jpg",
        "images/destinations/galle-fort/banner-image.jpg",
        "images/destinations/destinations-main.jpg",
        "images/destinations/ella/gallery2.jpg",
        "images/destinations/ella/gallery3.jpg",
        "images/destinations/ella/gallery1.jpg",
        "images/destinations/kandy/gallery3.jpg",
        "images/destinations/anuradhapura/banner-image.jpg",
        "images/destinations/sigiriya/gallery2.jpg",
        "images/destinations/galle-fort/gallery3.jpg",
        "images/destinations/mirissa/gallery2.jpg",
        "images/destinations/hikkaduwa/banner-image.jpg",
        "images/destinations/nuwara-eliya/banner-image.jpg",
        "images/destinations/wilpattu/banner-image.jpg",
        "images/destinations/polonnaruwa/banner-image.jpg",
        "images/destinations/yala/gallery1.jpg",
        "images/destinations/sinharaja/banner-image.jpg",
        "images/destinations/kithulgala/banner-image.jpg",
        "images/destinations/sigiriya/banner-image.jpg",
        "images/destinations/kandy/gallery1.jpg",
        "images/destinations/dambulla/banner-image.jpg",
        "images/destinations/yala/banner.image.jpg",
        "images/destinations/sigiriya/gallery4.jpg",
        "images/destinations/galle-fort/gallery2.jpg",
        "images/destinations/passikudah/banner-image.jpg",
        "images/destinations/udawalawe/banner-image.jpg",
        "images/destinations/mirissa/banner-image.jpg",
        "images/destinations/galle/gallery3.jpg",
        "images/destinations/yala/gallery3.jpg",
        "images/destinations/sigiriya/gallery3.jpg",
        "images/destinations/minneriya/banner-image.jpg",
        "images/destinations/galle-fort/gallery4.jpg",
        "images/destinations/belihuloya/banner-image.jpg"
    ]
    
    optimized_count = 0
    failed_count = 0
    
    for image_path in large_images:
        if os.path.exists(image_path):
            if optimize_image(image_path):
                optimized_count += 1
            else:
                failed_count += 1
        else:
            print(f"⚠️  File not found: {image_path}")
            failed_count += 1
        print()
    
    print("=" * 50)
    print(f"🎉 Optimization Complete!")
    print(f"✅ Successfully optimized: {optimized_count} images")
    print(f"❌ Failed to optimize: {failed_count} images")
    print(f"📁 Backups saved in: backups/")
    print()
    print("🔧 Tools tried: ffmpeg → ImageMagick → jpegoptim")
    print("🎯 Target quality: 78% (good balance of quality vs size)")

if __name__ == "__main__":
    main()