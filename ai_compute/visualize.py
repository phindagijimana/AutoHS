"""Optional overlay PNG generation for AI-compute."""

from __future__ import annotations

from pathlib import Path


def generate_overlays_if_possible(
    t1_path: Path,
    aseg_mgz: Path | None,
    output_dir: Path,
) -> list[Path]:
    """Generate coronal overlays when nibabel, numpy, and matplotlib are available."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import nibabel as nib
        import numpy as np
    except ImportError:
        return []

    if not t1_path.exists() or aseg_mgz is None or not aseg_mgz.exists():
        return []

    t1 = nib.load(str(t1_path)).get_fdata()
    seg = nib.load(str(aseg_mgz)).get_fdata()
    overlay_dir = output_dir / "visualizations" / "coronal"
    overlay_dir.mkdir(parents=True, exist_ok=True)

    paths: list[Path] = []
    mask = np.isin(seg, [17, 53])
    mid = t1.shape[1] // 2
    start = max(0, mid - 5)
    end = min(t1.shape[1], mid + 5)

    for idx, y in enumerate(range(start, end)):
        fig, ax = plt.subplots(figsize=(4, 4))
        base = np.rot90(t1[:, y, :])
        ax.imshow(base, cmap="gray")
        overlay = np.rot90(mask[:, y, :].astype(float))
        ax.imshow(np.ma.masked_where(overlay == 0, overlay), cmap="Blues", alpha=0.45)
        ax.axis("off")
        out = overlay_dir / f"slice_{idx:02d}.png"
        fig.savefig(out, bbox_inches="tight", dpi=120)
        plt.close(fig)
        paths.append(out)

    return paths
