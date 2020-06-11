def image_preprocess(image_path):
    # Load modules
    from PIL import Image, ImageChops, ImageOps
    import math
    import numpy as np

    # Load target image
    im = Image.open(image_path)

    # Trim edges
    border = "white"
    bg = Image.new(im.mode, im.size, border)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    im_trim = im.crop(bbox)

    # Rescale to 64
    scale_ratio = im_trim.size[0] / im_trim.size[1]
    im_scale = im_trim.resize((round(64 * scale_ratio), 64), 3)
    tall_thin = im_trim.size[1] > im_trim.size[0]

    if tall_thin:
        # If image is taller than wide
        scale_ratio = im_trim.size[0] / im_trim.size[1]
        im_scale = im_trim.resize((round(64 * scale_ratio), 64), 3)
    else:
        # If image is wider than tall
        scale_ratio = im_trim.size[1] / im_trim.size[0]
        im_scale = im_trim.resize((64, round(64 * scale_ratio)), 3)

    # Building pad area
    min_dim = np.argmin(im_scale.size)
    half_pad = math.floor((64 - im_scale.size[min_dim]) / 2)

    # Padding to 64x64
    im_scale = im_scale.convert("RGB")
    pad_img = Image.new(im_scale.mode, (64, 64), "white")
    if tall_thin:
        pad_img.paste(im_scale, (half_pad, 0))
    else:
        pad_img.paste(im_scale, (0, half_pad))

    # Whitespace to 86x86
    image_out = ImageOps.expand(pad_img, 11, "white")

    # Export to temporary directory
    # image_out.save('_temp/input/Oak_input.png')
    return(image_out)
