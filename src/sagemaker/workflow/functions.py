# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""The step definitions for workflow."""
from __future__ import absolute_import

from typing import List

import attr

from sagemaker.workflow.entities import Expression


@attr.s
class Join(Expression):
    """Join together properties.

    Examples:
    Build a Amazon S3 Uri with bucket name parameter and pipeline execution Id and use it
    as training input::

        bucket = ParameterString('bucket', default_value='my-bucket')

        TrainingInput(
            s3_data=Join(on='/', ['s3:/', bucket, ExecutionVariables.PIPELINE_EXECUTION_ID]),
            content_type="text/csv")

    Attributes:
        values (List[Union[PrimitiveType, Parameter, Expression]]):
            The primitive type values, parameters, step properties, expressions to join.
        on_str (str): The string to join the values on (Defaults to "").
    """

    on: str = attr.ib(factory=str)
    values: List = attr.ib(factory=list)

    @property
    def expr(self):
        """The expression dict for a `Join` function."""
        return {
            "Std:Join": {
                "On": self.on,
                "Values": [
                    value.expr if hasattr(value, "expr") else value for value in self.values
                ],
            },
        }
