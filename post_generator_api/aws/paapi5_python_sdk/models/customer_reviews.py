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

from aws.paapi5_python_sdk.models.rating import Rating  # noqa: F401,E501


class CustomerReviews(object):
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
        'count': 'int',
        'star_rating': 'Rating'
    }

    attribute_map = {
        'count': 'Count',
        'star_rating': 'StarRating'
    }

    def __init__(self, count=None, star_rating=None):  # noqa: E501
        """CustomerReviews - a model defined in Swagger"""  # noqa: E501

        self._count = None
        self._star_rating = None
        self.discriminator = None

        if count is not None:
            self.count = count
        if star_rating is not None:
            self.star_rating = star_rating

    @property
    def count(self):
        """Gets the count of this CustomerReviews.  # noqa: E501


        :return: The count of this CustomerReviews.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this CustomerReviews.


        :param count: The count of this CustomerReviews.  # noqa: E501
        :type: int
        """

        self._count = count

    @property
    def star_rating(self):
        """Gets the star_rating of this CustomerReviews.  # noqa: E501


        :return: The star_rating of this CustomerReviews.  # noqa: E501
        :rtype: Rating
        """
        return self._star_rating

    @star_rating.setter
    def star_rating(self, star_rating):
        """Sets the star_rating of this CustomerReviews.


        :param star_rating: The star_rating of this CustomerReviews.  # noqa: E501
        :type: Rating
        """

        self._star_rating = star_rating

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
        if issubclass(CustomerReviews, dict):
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
        if not isinstance(other, CustomerReviews):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
