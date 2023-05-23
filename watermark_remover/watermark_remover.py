from tempfile import TemporaryDirectory

from pdf2image import convert_from_path
from PIL import Image, ImageEnhance

# Source:
# https://github.com/Mupati/watermark_remover_cli


def enhance_image(pil_image):
    img = ImageEnhance.Contrast(pil_image).enhance(2.8)
    enhanced_image = img.convert("RGBA")
    return enhanced_image


def remove_watermark_from_image(image_path, output_path):
    pil_image = Image.open(image_path)
    im = enhance_image(pil_image)
    R, G, B = im.convert("RGB").split()
    r = R.load()
    g = G.load()
    b = B.load()
    w, h = im.size

    # Convert non-black pixels to white
    for i in range(w):
        for j in range(h):
            if r[i, j] > 100 or g[i, j] > 100 or b[i, j] > 100:
                r[i, j] = 255  # Just change R channel

    # Merge just the R channel as all channels
    im = Image.merge("RGB", (R, R, R))
    im.save(output_path)


def remove_watermark_from_pdf(pdf_path, output_path):
    with TemporaryDirectory() as path:
        pil_images = convert_from_path(pdf_path, output_folder=path)
        processed_images = []

        for i, img in enumerate(pil_images):
            output_image_path = f"{path}/processed_image_{i}.jpg"
            remove_watermark_from_image(img.filename, output_image_path)
            processed_images.append(output_image_path)

        images = [Image.open(image_path) for image_path in processed_images]
        images[0].save(output_path, save_all=True, append_images=images[1:])


if __name__ == "__main__":
    remove_watermark_from_image("resources/1.jpeg", "output.jpg")
    # remove_watermark_from_pdf("resources/1.pdf", "output.jpg")
