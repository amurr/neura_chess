# generated from rosidl_generator_py/resource/_idl.py.em
# with input from lara_interfaces:srv/ComputeIK.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'seed_joint_positions'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ComputeIK_Request(type):
    """Metaclass of message 'ComputeIK_Request'."""

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
                'lara_interfaces.srv.ComputeIK_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__compute_ik__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__compute_ik__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__compute_ik__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__compute_ik__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__compute_ik__request

            from geometry_msgs.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ComputeIK_Request(metaclass=Metaclass_ComputeIK_Request):
    """Message class 'ComputeIK_Request'."""

    __slots__ = [
        '_target_pose',
        '_seed_joint_positions',
        '_timeout_sec',
        '_position_tolerance',
        '_orientation_tolerance',
        '_enforce_joint_limits_mode',
    ]

    _fields_and_field_types = {
        'target_pose': 'geometry_msgs/Pose',
        'seed_joint_positions': 'sequence<double>',
        'timeout_sec': 'double',
        'position_tolerance': 'double',
        'orientation_tolerance': 'double',
        'enforce_joint_limits_mode': 'int8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from geometry_msgs.msg import Pose
        self.target_pose = kwargs.get('target_pose', Pose())
        self.seed_joint_positions = array.array('d', kwargs.get('seed_joint_positions', []))
        self.timeout_sec = kwargs.get('timeout_sec', float())
        self.position_tolerance = kwargs.get('position_tolerance', float())
        self.orientation_tolerance = kwargs.get('orientation_tolerance', float())
        self.enforce_joint_limits_mode = kwargs.get('enforce_joint_limits_mode', int())

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
        if self.seed_joint_positions != other.seed_joint_positions:
            return False
        if self.timeout_sec != other.timeout_sec:
            return False
        if self.position_tolerance != other.position_tolerance:
            return False
        if self.orientation_tolerance != other.orientation_tolerance:
            return False
        if self.enforce_joint_limits_mode != other.enforce_joint_limits_mode:
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
        if __debug__:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'target_pose' field must be a sub message of type 'Pose'"
        self._target_pose = value

    @builtins.property
    def seed_joint_positions(self):
        """Message field 'seed_joint_positions'."""
        return self._seed_joint_positions

    @seed_joint_positions.setter
    def seed_joint_positions(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'seed_joint_positions' array.array() must have the type code of 'd'"
            self._seed_joint_positions = value
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
                "The 'seed_joint_positions' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._seed_joint_positions = array.array('d', value)

    @builtins.property
    def timeout_sec(self):
        """Message field 'timeout_sec'."""
        return self._timeout_sec

    @timeout_sec.setter
    def timeout_sec(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'timeout_sec' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'timeout_sec' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._timeout_sec = value

    @builtins.property
    def position_tolerance(self):
        """Message field 'position_tolerance'."""
        return self._position_tolerance

    @position_tolerance.setter
    def position_tolerance(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'position_tolerance' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'position_tolerance' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._position_tolerance = value

    @builtins.property
    def orientation_tolerance(self):
        """Message field 'orientation_tolerance'."""
        return self._orientation_tolerance

    @orientation_tolerance.setter
    def orientation_tolerance(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'orientation_tolerance' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'orientation_tolerance' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._orientation_tolerance = value

    @builtins.property
    def enforce_joint_limits_mode(self):
        """Message field 'enforce_joint_limits_mode'."""
        return self._enforce_joint_limits_mode

    @enforce_joint_limits_mode.setter
    def enforce_joint_limits_mode(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'enforce_joint_limits_mode' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'enforce_joint_limits_mode' field must be an integer in [-128, 127]"
        self._enforce_joint_limits_mode = value


# Import statements for member types

# Member 'joint_positions'
# already imported above
# import array

# already imported above
# import builtins

# already imported above
# import math

# already imported above
# import rosidl_parser.definition


class Metaclass_ComputeIK_Response(type):
    """Metaclass of message 'ComputeIK_Response'."""

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
                'lara_interfaces.srv.ComputeIK_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__compute_ik__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__compute_ik__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__compute_ik__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__compute_ik__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__compute_ik__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ComputeIK_Response(metaclass=Metaclass_ComputeIK_Response):
    """Message class 'ComputeIK_Response'."""

    __slots__ = [
        '_success',
        '_message',
        '_joint_names',
        '_joint_positions',
        '_position_error',
        '_orientation_error',
        '_iterations',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'message': 'string',
        'joint_names': 'sequence<string>',
        'joint_positions': 'sequence<double>',
        'position_error': 'double',
        'orientation_error': 'double',
        'iterations': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.message = kwargs.get('message', str())
        self.joint_names = kwargs.get('joint_names', [])
        self.joint_positions = array.array('d', kwargs.get('joint_positions', []))
        self.position_error = kwargs.get('position_error', float())
        self.orientation_error = kwargs.get('orientation_error', float())
        self.iterations = kwargs.get('iterations', int())

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
        if self.joint_names != other.joint_names:
            return False
        if self.joint_positions != other.joint_positions:
            return False
        if self.position_error != other.position_error:
            return False
        if self.orientation_error != other.orientation_error:
            return False
        if self.iterations != other.iterations:
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

    @builtins.property
    def joint_names(self):
        """Message field 'joint_names'."""
        return self._joint_names

    @joint_names.setter
    def joint_names(self, value):
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
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'joint_names' field must be a set or sequence and each value of type 'str'"
        self._joint_names = value

    @builtins.property
    def joint_positions(self):
        """Message field 'joint_positions'."""
        return self._joint_positions

    @joint_positions.setter
    def joint_positions(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'joint_positions' array.array() must have the type code of 'd'"
            self._joint_positions = value
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
                "The 'joint_positions' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._joint_positions = array.array('d', value)

    @builtins.property
    def position_error(self):
        """Message field 'position_error'."""
        return self._position_error

    @position_error.setter
    def position_error(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'position_error' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'position_error' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._position_error = value

    @builtins.property
    def orientation_error(self):
        """Message field 'orientation_error'."""
        return self._orientation_error

    @orientation_error.setter
    def orientation_error(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'orientation_error' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'orientation_error' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._orientation_error = value

    @builtins.property
    def iterations(self):
        """Message field 'iterations'."""
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'iterations' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'iterations' field must be an integer in [-2147483648, 2147483647]"
        self._iterations = value


class Metaclass_ComputeIK(type):
    """Metaclass of service 'ComputeIK'."""

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
                'lara_interfaces.srv.ComputeIK')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__compute_ik

            from lara_interfaces.srv import _compute_ik
            if _compute_ik.Metaclass_ComputeIK_Request._TYPE_SUPPORT is None:
                _compute_ik.Metaclass_ComputeIK_Request.__import_type_support__()
            if _compute_ik.Metaclass_ComputeIK_Response._TYPE_SUPPORT is None:
                _compute_ik.Metaclass_ComputeIK_Response.__import_type_support__()


class ComputeIK(metaclass=Metaclass_ComputeIK):
    from lara_interfaces.srv._compute_ik import ComputeIK_Request as Request
    from lara_interfaces.srv._compute_ik import ComputeIK_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
