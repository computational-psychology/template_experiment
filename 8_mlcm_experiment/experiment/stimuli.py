import stimupy

TARGET_SIZE = 1

resolution = {
    "visual_size": (TARGET_SIZE * 5, TARGET_SIZE * 5),
    "ppd": 48,
}


# %% SBC circular
def sbc_circular(intensity_target, intensity_surround, intensity_background):
    return stimupy.sbcs.circular(
        **resolution,
        target_radius=TARGET_SIZE,
        surround_radius=TARGET_SIZE * 2,
        intensity_target=intensity_target,
        intensity_surround=intensity_surround,
        intensity_background=intensity_background,
    )


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    im1 = sbc_circular(0.5, 0.0, intensity_background=0.3)
    im2 = sbc_circular(0.5, 1.0, intensity_background=0.3)

    print(im1.keys())

    fig, axes = plt.subplots(1, 2, figsize=(8, 16))
    axes[0].imshow(im1["img"], cmap="gray", vmin=0, vmax=1.0)
    axes[1].imshow(im2["img"], cmap="gray", vmin=0, vmax=1.0)
    plt.show()

    print(im1["img"].shape)
