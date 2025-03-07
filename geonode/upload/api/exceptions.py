#########################################################################
#
# Copyright (C) 2024 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class GeneralUploadException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Exception during resource upload"
    default_code = "upload_exception"
    category = "upload"


class FileUploadLimitException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Total upload size exceeded. Please try again with smaller files.")
    default_code = "total_upload_size_exceeded"
    category = "upload"


class UploadParallelismLimitException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("The number of active parallel uploads exceeds. Wait for the pending ones to finish.")
    default_code = "upload_parallelism_limit_exceeded"
    category = "upload"


class ImportException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Exception during resource upload"
    default_code = "importer_exception"
    category = "importer"


class InvalidInputFileException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The provided files are invalid"
    default_code = "importer_exception"
    category = "importer"


class PublishResourceException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Error during the resource publishing"
    default_code = "publishing_exception"
    category = "importer"


class ResourceCreationException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Error during the creation of the geonode resource"
    default_code = "gn_resource_exception"
    category = "importer"


class CopyResourceException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Error during the copy of the geonode resource"
    default_code = "gn_resource_exception"
    category = "importer"


class StartImportException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Error during start of the import session"
    default_code = "start_import_exception"
    category = "importer"


class HandlerException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "base handler exception"
    default_code = "handler_exception"
    category = "handler"
