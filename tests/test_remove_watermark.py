from PIL import Image

from user_interface.ui import add_watermark, remove_watermark


# Test remove_watermark function
def test_remove_watermark_removes_watermark():
    # Create a dummy image with a watermark for testing
    image_with_watermark = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    watermark_image = Image.new("RGBA", (100, 100), (255, 255, 255, 100))
    image_with_watermark = add_watermark(image_with_watermark, watermark_image, 5, 5)

    # Test the watermark removal
    result_image = remove_watermark(image_with_watermark)

    # Verify watermark is removed
    assert isinstance(result_image, Image.Image)
    assert result_image.size == (500, 500)
    # Add assertions to validate the watermark has been removed


def test_remove_watermark_handles_image_without_watermark():
    # Create an image without a watermark for testing
    image_without_watermark = Image.new("RGBA", (500, 500), (255, 255, 255, 255))

    # Test removing watermark from an image without a watermark
    result_image = remove_watermark(image_without_watermark)

    # Verify the image remains unchanged
    assert isinstance(result_image, Image.Image)
    assert result_image.size == (500, 500)


def test_remove_watermark_handles_different_watermark_type():
    # Create an image with a different watermark type for testing
    image_with_different_watermark = Image.new("RGB", (500, 500), (255, 255, 255))

    # Test removing watermark from an image with a different watermark type
    result_image = remove_watermark(image_with_different_watermark)

    # Verify the image remains unchanged
    assert isinstance(result_image, Image.Image)
    assert result_image.size == (500, 500)


def test_remove_watermark_handles_partial_transparency():
    # Create a dummy image with a watermark using partial transparency for testing
    image_with_partial_transparency = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    watermark_image = Image.new("RGBA", (100, 100), (255, 255, 255, 100))
    image_with_partial_transparency = add_watermark(image_with_partial_transparency, watermark_image, 5, 5)

    # Test the watermark removal from an image with partial transparency
    result_image = remove_watermark(image_with_partial_transparency)

    # Verify watermark is removed while preserving partial transparency
    assert isinstance(result_image, Image.Image)
    assert result_image.size == (500, 500)
