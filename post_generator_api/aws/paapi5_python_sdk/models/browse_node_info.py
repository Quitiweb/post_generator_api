# coding: utf-8

"""
  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Licensed under the Apache License, Version 2.0 (the "License").
  You may not use this file except in compliance with the License.
  A copy of the License is located at

      http://www.apache.org/licenses/LICENSE-2.0

  or in the "license" file accompanying this file. This file is distributed
  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
  express or implied. See the License for the specific language governing
  permissions and limitations under the License.
"""


"""
    ProductAdvertisingAPI

    https://webservices.amazon.com/paapi5/documentation/index.html  # noqa: E501
"""


import pprint
import re  # noqa: F401

import six

from aws.paapi5_python_sdk.models.browse_node import BrowseNode  # noqa: F401,E501
from aws.paapi5_python_sdk.models.website_sales_rank import WebsiteSalesRank  # noqa: F401,E501


class BrowseNodeInfo(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'browse_nodes': 'list[BrowseNode]',
        'website_sales_rank': 'WebsiteSalesRank'
    }

    attribute_map = {
        'browse_nodes': 'BrowseNodes',
        'website_sales_rank': 'WebsiteSalesRank'
    }

    def __init__(self, browse_nodes=None, website_sales_rank=None):  # noqa: E501
        """BrowseNodeInfo - a model defined in Swagger"""  # noqa: E501

        self._browse_nodes = None
        self._website_sales_rank = None
        self.discriminator = None

        if browse_nodes is not None:
            self.browse_nodes = browse_nodes
        if website_sales_rank is not None:
            self.website_sales_rank = website_sales_rank

    @property
    def browse_nodes(self):
        """Gets the browse_nodes of this BrowseNodeInfo.  # noqa: E501


        :return: The browse_nodes of this BrowseNodeInfo.  # noqa: E501
        :rtype: list[BrowseNode]
        """
        return self._browse_nodes

    @browse_nodes.setter
    def browse_nodes(self, browse_nodes):
        """Sets the browse_nodes of this BrowseNodeInfo.


        :param browse_nodes: The browse_nodes of this BrowseNodeInfo.  # noqa: E501
        :type: list[BrowseNode]
        """

        self._browse_nodes = browse_nodes

    @property
    def website_sales_rank(self):
        """Gets the website_sales_rank of this BrowseNodeInfo.  # noqa: E501


        :return: The website_sales_rank of this BrowseNodeInfo.  # noqa: E501
        :rtype: WebsiteSalesRank
        """
        return self._website_sales_rank

    @website_sales_rank.setter
    def website_sales_rank(self, website_sales_rank):
        """Sets the website_sales_rank of this BrowseNodeInfo.


        :param website_sales_rank: The website_sales_rank of this BrowseNodeInfo.  # noqa: E501
        :type: WebsiteSalesRank
        """

        self._website_sales_rank = website_sales_rank

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(BrowseNodeInfo, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BrowseNodeInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
