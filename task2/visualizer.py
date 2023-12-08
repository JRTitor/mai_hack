import pyvista
import os
from typing import Union, List
from pathlib import Path

def plot_slices(solver_path: Union[str, os.PathLike, Path],
                base_path: Union[str, os.PathLike, Path],
                show_edges: bool = False,
                body_name_of: str = 'motorBike_0',
                body_name_scene: str = 'Body') -> None:
    """Построение графиков с распределением давления на теле.

    Args:
        solver_path (Union[str, os.PathLike, Path]): Путь до папки с кейсом.
        base_path (Union[str, os.PathLike, Path]): Путь до папки с финальным временем расчета.
        show_edges (bool, optional): Нужно ли визуализировать расчетную область. Defaults to False.
        body_name_of (str, optional):  Имя тела в сцене (как в OF). Defaults to 'motorBike_0'.
        body_name_scene (str, optional):  Имя тела в сцене (как в config). Defaults to 'motorBike_0'.
    """
    # Step 1: prepare case for reading
    path_to_case = solver_path / Path('foam.foam')
    save_path_body = base_path / Path(f'p_on_surface_{body_name_scene}.png')
    
    if not os.path.exists(path_to_case):
        open(path_to_case, 'w').close()

    # Step 2: read case and make z slise
    reader = pyvista.POpenFOAMReader(path_to_case)

    block = reader.read()
    body = block['boundary'][body_name_of]


    # Step 3: plot pressure on body surface
    pl = pyvista.Plotter(off_screen=True)
    pl.add_mesh(body,
                scalars='p',
                lighting=False,
                scalar_bar_args={'title': 'Flow Preassure'},
                cmap = 'jet',
                show_edges=show_edges)

    pl.enable_anti_aliasing()
    pl.enable_parallel_projection()
    pl.show_axes()
    pl.camera.focal_point = body.center
    pl.camera.position = (-10, 10, -10)
    pl.camera.up = (0, 1, 0)

    _ = pl.screenshot(save_path_body)