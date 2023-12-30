# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import fnmatch
import os
from typing import Type

from pydantic import BaseModel, Field

from nextpy.ai.tools.basetool import BaseTool
from nextpy.ai.tools.toolkits.file_toolkit.file.utils import (
    INVALID_PATH_TEMPLATE,
    BaseFileToolMixin,
    FileValidationError,
)


class FileSearchInput(BaseModel):
    """Input for FileSearchTool."""

    dir_path: str = Field(
        default=".",
        description="Subdirectory to search in.",
    )
    pattern: str = Field(
        ...,
        description="Unix shell regex, where * matches everything.",
    )


class FileSearchTool(BaseFileToolMixin, BaseTool):
    name: str = "file_search"
    args_schema: Type[BaseModel] = FileSearchInput
    description: str = (
        "Recursively search for files in a subdirectory that match the regex pattern"
    )

    def run(
        self,
        pattern: str,
        dir_path: str = ".",
    ) -> str:
        try:
            dir_path_ = self.get_relative_path(dir_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(arg_name="dir_path", value=dir_path)
        matches = []
        try:
            for root, _, filenames in os.walk(dir_path_):
                for filename in fnmatch.filter(filenames, pattern):
                    absolute_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(absolute_path, dir_path_)
                    matches.append(relative_path)
            if matches:
                return "\n".join(matches)
            else:
                return f"No files found for pattern {pattern} in directory {dir_path}"
        except Exception as e:
            return "Error: " + str(e)

    async def _arun(
        self,
        dir_path: str,
        pattern: str,
    ) -> str:
        # TODO: Add aiofiles method
        raise NotImplementedError
