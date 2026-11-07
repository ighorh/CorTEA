from typing import Tuple

import cv2
import numpy as np


class CalibrationMath:
    """Mathematical utilities for projection / keystone calibration."""

    @classmethod
    def calculate_projection_area(
        cls,
        screen_width: int,
        screen_height: int,
        aspect_ratio: Tuple[int, int],  # ex: (4, 3), (16, 9)
    ) -> Tuple[int, int]:
        """Calculates content area while maintaining the desired aspect ratio,
        prioritizing height."""
        if not (
            isinstance(aspect_ratio, tuple)
            and len(aspect_ratio) == 2
            and all(x > 0 for x in aspect_ratio)
        ):
            raise ValueError(
                "The parameter aspect_ratio must be a tuple of two positive "
                "integers (e.g., (4, 3))"
            )

        ratio_w, ratio_h = aspect_ratio
        content_height = screen_height
        content_width = (screen_height * ratio_w) // ratio_h

        # If the calculated width is greater than the screen width
        # (rare in 16:9), the size is adjust accordingly.
        if content_width > screen_width:
            content_width = screen_width
            content_height = (screen_width * ratio_h) // ratio_w

        return content_width, content_height

    @classmethod
    def calculate_centered_destination_points(
        cls,
        screen_width: int,
        screen_height: int,
        content_width: int,
        content_height: int,
        center_horizontally: bool = True,
        center_vertically: bool = True,
    ) -> np.ndarray:
        """
        Calculates the destination points (coordinates) by centering
        the usable area within the monitor's total resolution.
        """
        left = (
            (screen_width - content_width) // 2 if center_horizontally else 0
        )
        top = (screen_height - content_height) // 2 if center_vertically else 0

        return np.float32(
            [
                [left, top],  # TL
                [left + content_width, top],  # TR
                [left, top + content_height],  # BL
                [left + content_width, top + content_height],  # BR
            ]
        )

    @classmethod
    def calculate_destination_points_with_flip(
        cls,
        screen_width: int,
        screen_height: int,
        content_width: int,
        content_height: int,
        flip_h: bool = False,
        flip_v: bool = False,
        center_horizontally: bool = True,
        center_vertically: bool = True,
    ) -> np.ndarray:
        """
        Returns destination points with optional horizontal/vertical mirroring,
        while keeping the content centered (when requested).
        Order of points: TL → TR → BL → BR (before flip).
        """
        points = cls.calculate_centered_destination_points(
            screen_width,
            screen_height,
            content_width,
            content_height,
            center_horizontally,
            center_vertically,
        )

        if not (flip_h or flip_v):
            return points

        # Indices: 0=TL, 1=TR, 2=BL, 3=BR
        order = [0, 1, 2, 3]

        if flip_h:
            order = [1, 0, 3, 2]  # horizontal mirror
        if flip_v:
            order = [2, 3, 0, 1]  # vertical mirror
            if flip_h:
                order = [3, 2, 1, 0]  # both

        return points[np.array(order)]

    @classmethod
    def get_perspective_transform(
        cls,
        content_size: Tuple[int, int],
        dst_points: np.ndarray,
    ) -> np.ndarray:
        """Generates a 3x3 homography matrix (source -> destination)."""
        src_points = np.float32(
            [
                [0, 0],
                [content_size[0], 0],
                [0, content_size[1]],
                [content_size[0], content_size[1]],
            ]
        )
        return cv2.getPerspectiveTransform(src_points, dst_points)

    @classmethod
    def get_inverse_transform(cls, matrix: np.ndarray) -> np.ndarray:
        """Returns the inverse matrix to map screen/camera
        points back to the game."""
        return np.linalg.inv(matrix)
