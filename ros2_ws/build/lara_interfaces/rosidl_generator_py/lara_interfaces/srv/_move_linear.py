# generated from rosidl_generator_py/resource/_idl.py.em
# with input from lara_interfaces:srv/MoveLinear.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'target_pose'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MoveLinear_Request(type):
    """Metaclass of message 'MoveLinear_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('lara_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'lara_interfaces.srv.MoveLinear_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__move_linear__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__move_linear__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__move_linear__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__move_linear__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__move_linear__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MoveLinear_Request(metaclass=Metaclass_MoveLinear_Request):
    """Message class 'MoveLinear_Request'."""

    __slots__ = [
        '_target_pose',
        '_speed',
        '_acceleration',
        '_enable_safety',
        '_use_relative',
        '_offset_frame',
    ]

    _fields_and_field_types = {
        'target_pose': 'sequence<double>',
        'speed': 'double',
        'acceleration': 'double',
        'enable_safety': 'boolean',
        'use_relative': 'boolean',
        'offset_frame': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.target_pose = array.array('d', kwargs.get('target_pose', []))
        self.speed = kwargs.get('speed', float())
        self.acceleration = kwargs.get('acceleration', float())
        self.enable_safety = kwargs.get('enable_safety', bool())
        self.use_relative = kwargs.get('use_relative', bool())
        self.offset_frame = kwargs.get('offset_frame', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.target_pose != other.target_pose:
            return False
        if self.speed != other.speed:
            return False
        if self.acceleration != other.acceleration:
            return False
        if self.enable_safety != other.enable_safety:
            return False
        if self.use_relative != other.use_relative:
            return False
        if self.offset_frame != other.offset_frame:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def target_pose(self):
        """Message field 'target_pose'."""
        return self._target_pose

    @target_pose.setter
    def target_pose(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'target_pose' array.array() must have the type code of 'd'"
            self._target_pose = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'target_pose' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._target_pose = array.array('d', value)

    @builtins.property
    def speed(self):
        """Message field 'speed'."""
        return self._speed

    @speed.setter
    def speed(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'speed' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'speed' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._speed = value

    @builtins.property
    def acceleration(self):
        """Message field 'acceleration'."""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'acceleration' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'acceleration' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._acceleration = value

    @builtins.property
    def enable_safety(self):
        """Message field 'enable_safety'."""
        return self._enable_safety

    @enable_safety.setter
    def enable_safety(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'enable_safety' field must be of type 'bool'"
        self._enable_safety = value

    @builtins.property
    def use_relative(self):
        """Message field 'use_relative'."""
        return self._use_relative

    @use_relative.setter
    def use_relative(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'use_relative' field must be of type 'bool'"
        self._use_relative = value

    @builtins.property
    def offset_frame(self):
        """Message field 'offset_frame'."""
        return self._offset_frame

    @offset_frame.setter
    def offset_frame(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'offset_frame' field must be of type 'str'"
        self._offset_frame = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_MoveLinear_Response(type):
    """Metaclass of message 'MoveLinear_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('lara_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'lara_interfaces.srv.MoveLinear_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__move_linear__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__move_linear__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__move_linear__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__move_linear__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__move_linear__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MoveLinear_Response(metaclass=Metaclass_MoveLinear_Response):
    """Message class 'MoveLinear_Response'."""

    __slots__ = [
        '_success',
        '_message',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'message': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.message = kwargs.get('message', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.success != other.success:
            return False
        if self.message != other.message:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value


class Metaclass_MoveLinear(type):
    """Metaclass of service 'MoveLinear'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('lara_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'lara_interfaces.srv.MoveLinear')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__move_linear

            from lara_interfaces.srv import _move_linear
            if _move_linear.Metaclass_MoveLinear_Request._TYPE_SUPPORT is None:
                _move_linear.Metaclass_MoveLinear_Request.__import_type_support__()
            if _move_linear.Metaclass_MoveLinear_Response._TYPE_SUPPORT is None:
                _move_linear.Metaclass_MoveLinear_Response.__import_type_support__()


class MoveLinear(metaclass=Metaclass_MoveLinear):
    from lara_interfaces.srv._move_linear import MoveLinear_Request as Request
    from lara_interfaces.srv._move_linear import MoveLinear_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
