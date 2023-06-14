import numpy as np
from PIL import Image

from user_interface.pages.api_and_functions.add_remove_watermark import add_watermark


def test_size_is_correct():
    main_image = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    watermark_image = Image.new("RGBA", (100, 100), (255, 255, 255, 100))
    X = 100
    Y = 100

    result_image = add_watermark(main_image, watermark_image, X, Y)

    assert result_image.size == main_image.size


def test_add_watermark_handles_large_watermark():
    main_image = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    watermark_image = Image.new("RGBA", (600, 600), (255, 255, 255, 100))
    X = 100
    Y = 100

    result_image = add_watermark(main_image, watermark_image, X, Y)

    # Assuming add_watermark handles large watermark by scaling it down to fit within the main image
    # Check if the resulting image has the same size as the main image
    assert result_image.size == main_image.size


def test_add_watermark_applies_watermark():
    main_image = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    watermark_image = Image.new("RGBA", (100, 100), (255, 255, 255, 100))
    X = 1
    Y = 1

    result_image = add_watermark(main_image, watermark_image, X, Y)

    # Assuming add_watermark applies the watermark at the given position (X, Y)
    # Check if the watermark is applied correctly in the result image

    # Calculate the expected position based on the formula provided
    expected_pos_x = int((main_image.width - watermark_image.width) * X / 10)
    expected_pos_y = int((main_image.height - watermark_image.height) * (10 - Y) / 10)

    # Verify watermark is added at the calculated position
    for x in range(watermark_image.width):
        for y in range(watermark_image.height):
            watermark_pixel = watermark_image.getpixel((x, y))
            result_pixel = result_image.getpixel((expected_pos_x + x, expected_pos_y + y))
            assert (0, 0, 0, 0) != result_pixel
