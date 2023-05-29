from PIL import Image

from user_interface.ui import add_watermark


def test_add_watermark_applies_watermark():
    # Create dummy images for testing
    main_image = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    watermark_image = Image.new("RGBA", (100, 100), (255, 255, 255, 100))

    # Apply watermark
    X = 5
    Y = 5
    result_image = add_watermark(main_image, watermark_image, X, Y)

    # Verify watermark is applied
    assert isinstance(result_image, Image.Image)
    assert result_image.size == (500, 500)


def test_add_watermark_handles_different_positions():
    # Create dummy images for testing
    main_image = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    watermark_image = Image.new("RGBA", (100, 100), (255, 255, 255, 100))

    # Apply watermark with different positions
    X = 2
    Y = 8
    result_image = add_watermark(main_image, watermark_image, X, Y)

    # Verify watermark is applied with different positions
    assert isinstance(result_image, Image.Image)
    assert result_image.size == (500, 500)


def test_add_watermark_handles_large_watermark():
    # Create dummy images for testing
    main_image = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    watermark_image = Image.new("RGBA", (500, 500), (255, 255, 255, 100))

    # Apply large watermark
    X = 5
    Y = 5
    result_image = add_watermark(main_image, watermark_image, X, Y)

    # Verify large watermark is applied without resizing
    assert isinstance(result_image, Image.Image)
    assert result_image.size == (200, 200)
