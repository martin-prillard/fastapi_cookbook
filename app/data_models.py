from typing import List

from pydantic import BaseModel, Field


class IrisInput(BaseModel):
    """
    Input model for Iris flower classification.

    This model represents the four features required for predicting
    the Iris flower species: sepal and petal dimensions.

    Attributes:
        sepal_length: Length of the sepal in centimeters.
        sepal_width: Width of the sepal in centimeters.
        petal_length: Length of the petal in centimeters.
        petal_width: Width of the petal in centimeters.

    Example:
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    """

    sepal_length: float = Field(
        ...,
        description="Sepal length in centimeters",
        gt=0,
    )
    sepal_width: float = Field(
        ...,
        description="Sepal width in centimeters",
        gt=0,
    )
    petal_length: float = Field(
        ...,
        description="Petal length in centimeters",
        gt=0,
    )
    petal_width: float = Field(
        ...,
        description="Petal width in centimeters",
        gt=0,
    )
