import stimupy

resolution = {
    "visual_size": (5, 5),
    "ppd": 48,
}

target_size = resolution["visual_size"][1] / 3


# %% SBC circular
def sbc_circular(intensity_target, intensity_background, bg):
    return stimupy.bullseyes.circular(
        **resolution,
        intensity_target=intensity_target,
        intensity_background=bg,
        intensity_rings=[intensity_background, intensity_background, intensity_background],
        n_rings=3,
    )


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    im1 = sbc_circular(0.5, 0.0, bg=0.3)
    im2 = sbc_circular(0.5, 1.0, bg=0.3)

    print(im1.keys())

    fig, axes = plt.subplots(1, 2, figsize=(8, 16))
    axes[0].imshow(im1["img"], cmap="gray", vmin=0, vmax=1.0)
    axes[1].imshow(im2["img"], cmap="gray", vmin=0, vmax=1.0)
    plt.show()

    print(im1["img"].shape)
