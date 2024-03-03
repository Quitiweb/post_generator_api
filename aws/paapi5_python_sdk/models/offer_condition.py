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

from aws.paapi5_python_sdk.models.offer_condition_note import OfferConditionNote  # noqa: F401,E501
from aws.paapi5_python_sdk.models.offer_sub_condition import OfferSubCondition  # noqa: F401,E501


class OfferCondition(object):
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
        'display_value': 'str',
        'label': 'str',
        'locale': 'str',
        'value': 'str',
        'sub_condition': 'OfferSubCondition',
        'condition_note': 'OfferConditionNote'
    }

    attribute_map = {
        'display_value': 'DisplayValue',
        'label': 'Label',
        'locale': 'Locale',
        'value': 'Value',
        'sub_condition': 'SubCondition',
        'condition_note': 'ConditionNote'
    }

    def __init__(self, display_value=None, label=None, locale=None, value=None, sub_condition=None, condition_note=None):  # noqa: E501
        """OfferCondition - a model defined in Swagger"""  # noqa: E501

        self._display_value = None
        self._label = None
        self._locale = None
        self._value = None
        self._sub_condition = None
        self._condition_note = None
        self.discriminator = None

        if display_value is not None:
            self.display_value = display_value
        if label is not None:
            self.label = label
        if locale is not None:
            self.locale = locale
        if value is not None:
            self.value = value
        if sub_condition is not None:
            self.sub_condition = sub_condition
        if condition_note is not None:
            self.condition_note = condition_note

    @property
    def display_value(self):
        """Gets the display_value of this OfferCondition.  # noqa: E501


        :return: The display_value of this OfferCondition.  # noqa: E501
        :rtype: str
        """
        return self._display_value

    @display_value.setter
    def display_value(self, display_value):
        """Sets the display_value of this OfferCondition.


        :param display_value: The display_value of this OfferCondition.  # noqa: E501
        :type: str
        """

        self._display_value = display_value

    @property
    def label(self):
        """Gets the label of this OfferCondition.  # noqa: E501


        :return: The label of this OfferCondition.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this OfferCondition.


        :param label: The label of this OfferCondition.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def locale(self):
        """Gets the locale of this OfferCondition.  # noqa: E501


        :return: The locale of this OfferCondition.  # noqa: E501
        :rtype: str
        """
        return self._locale

    @locale.setter
    def locale(self, locale):
        """Sets the locale of this OfferCondition.


        :param locale: The locale of this OfferCondition.  # noqa: E501
        :type: str
        """

        self._locale = locale

    @property
    def value(self):
        """Gets the value of this OfferCondition.  # noqa: E501


        :return: The value of this OfferCondition.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this OfferCondition.


        :param value: The value of this OfferCondition.  # noqa: E501
        :type: str
        """

        self._value = value

    @property
    def sub_condition(self):
        """Gets the sub_condition of this OfferCondition.  # noqa: E501


        :return: The sub_condition of this OfferCondition.  # noqa: E501
        :rtype: OfferSubCondition
        """
        return self._sub_condition

    @sub_condition.setter
    def sub_condition(self, sub_condition):
        """Sets the sub_condition of this OfferCondition.


        :param sub_condition: The sub_condition of this OfferCondition.  # noqa: E501
        :type: OfferSubCondition
        """

        self._sub_condition = sub_condition

    @property
    def condition_note(self):
        """Gets the condition_note of this OfferCondition.  # noqa: E501


        :return: The condition_note of this OfferCondition.  # noqa: E501
        :rtype: OfferConditionNote
        """
        return self._condition_note

    @condition_note.setter
    def condition_note(self, condition_note):
        """Sets the condition_note of this OfferCondition.


        :param condition_note: The condition_note of this OfferCondition.  # noqa: E501
        :type: OfferConditionNote
        """

        self._condition_note = condition_note

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
        if issubclass(OfferCondition, dict):
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
        if not isinstance(other, OfferCondition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other