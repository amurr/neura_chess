# generated from rosidl_generator_py/resource/_idl.py.em
# with input from moveit_master:msg/MotionStep.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MotionStep(type):
    """Metaclass of message 'MotionStep'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'ARM_POSE': 0,
        'ARM_NAMED': 1,
        'GRIPPER_NAMED': 2,
        'WAIT': 3,
        'GRIPPER_JOINT': 4,
        'ARM_CARTESIAN': 5,
        'ATTACH': 6,
        'DETACH': 7,
        'ALLOW_COLLISION': 8,
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('moveit_master')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'moveit_master.msg.MotionStep')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__motion_step
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__motion_step
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__motion_step
            cls._TYPE_SUPPORT = module.type_support_msg__msg__motion_step
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__motion_step

            from geometry_msgs.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

            from geometry_msgs.msg import Vector3
            if Vector3.__class__._TYPE_SUPPORT is None:
                Vector3.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'ARM_POSE': cls.__constants['ARM_POSE'],
            'ARM_NAMED': cls.__constants['ARM_NAMED'],
            'GRIPPER_NAMED': cls.__constants['GRIPPER_NAMED'],
            'WAIT': cls.__constants['WAIT'],
            'GRIPPER_JOINT': cls.__constants['GRIPPER_JOINT'],
            'ARM_CARTESIAN': cls.__constants['ARM_CARTESIAN'],
            'ATTACH': cls.__constants['ATTACH'],
            'DETACH': cls.__constants['DETACH'],
            'ALLOW_COLLISION': cls.__constants['ALLOW_COLLISION'],
        }

    @property
    def ARM_POSE(self):
        """Message constant 'ARM_POSE'."""
        return Metaclass_MotionStep.__constants['ARM_POSE']

    @property
    def ARM_NAMED(self):
        """Message constant 'ARM_NAMED'."""
        return Metaclass_MotionStep.__constants['ARM_NAMED']

    @property
    def GRIPPER_NAMED(self):
        """Message constant 'GRIPPER_NAMED'."""
        return Metaclass_MotionStep.__constants['GRIPPER_NAMED']

    @property
    def WAIT(self):
        """Message constant 'WAIT'."""
        return Metaclass_MotionStep.__constants['WAIT']

    @property
    def GRIPPER_JOINT(self):
        """Message constant 'GRIPPER_JOINT'."""
        return Metaclass_MotionStep.__constants['GRIPPER_JOINT']

    @property
    def ARM_CARTESIAN(self):
        """Message constant 'ARM_CARTESIAN'."""
        return Metaclass_MotionStep.__constants['ARM_CARTESIAN']

    @property
    def ATTACH(self):
        """Message constant 'ATTACH'."""
        return Metaclass_MotionStep.__constants['ATTACH']

    @property
    def DETACH(self):
        """Message constant 'DETACH'."""
        return Metaclass_MotionStep.__constants['DETACH']

    @property
    def ALLOW_COLLISION(self):
        """Message constant 'ALLOW_COLLISION'."""
        return Metaclass_MotionStep.__constants['ALLOW_COLLISION']


class MotionStep(metaclass=Metaclass_MotionStep):
    """
    Message class 'MotionStep'.

    Constants:
      ARM_POSE
      ARM_NAMED
      GRIPPER_NAMED
      WAIT
      GRIPPER_JOINT
      ARM_CARTESIAN
      ATTACH
      DETACH
      ALLOW_COLLISION
    """

    __slots__ = [
        '_type',
        '_pose',
        '_named_target',
        '_duration',
        '_joint_value',
        '_offset',
        '_object_id',
        '_touch_links',
        '_allow',
    ]

    _fields_and_field_types = {
        'type': 'uint8',
        'pose': 'geometry_msgs/Pose',
        'named_target': 'string',
        'duration': 'double',
        'joint_value': 'double',
        'offset': 'geometry_msgs/Vector3',
        'object_id': 'string',
        'touch_links': 'sequence<string>',
        'allow': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Vector3'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.type = kwargs.get('type', int())
        from geometry_msgs.msg import Pose
        self.pose = kwargs.get('pose', Pose())
        self.named_target = kwargs.get('named_target', str())
        self.duration = kwargs.get('duration', float())
        self.joint_value = kwargs.get('joint_value', float())
        from geometry_msgs.msg import Vector3
        self.offset = kwargs.get('offset', Vector3())
        self.object_id = kwargs.get('object_id', str())
        self.touch_links = kwargs.get('touch_links', [])
        self.allow = kwargs.get('allow', bool())

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
        if self.type != other.type:
            return False
        if self.pose != other.pose:
            return False
        if self.named_target != other.named_target:
            return False
        if self.duration != other.duration:
            return False
        if self.joint_value != other.joint_value:
            return False
        if self.offset != other.offset:
            return False
        if self.object_id != other.object_id:
            return False
        if self.touch_links != other.touch_links:
            return False
        if self.allow != other.allow:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property  # noqa: A003
    def type(self):  # noqa: A003
        """Message field 'type'."""
        return self._type

    @type.setter  # noqa: A003
    def type(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'type' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'type' field must be an unsigned integer in [0, 255]"
        self._type = value

    @builtins.property
    def pose(self):
        """Message field 'pose'."""
        return self._pose

    @pose.setter
    def pose(self, value):
        if __debug__:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'pose' field must be a sub message of type 'Pose'"
        self._pose = value

    @builtins.property
    def named_target(self):
        """Message field 'named_target'."""
        return self._named_target

    @named_target.setter
    def named_target(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'named_target' field must be of type 'str'"
        self._named_target = value

    @builtins.property
    def duration(self):
        """Message field 'duration'."""
        return self._duration

    @duration.setter
    def duration(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'duration' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'duration' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._duration = value

    @builtins.property
    def joint_value(self):
        """Message field 'joint_value'."""
        return self._joint_value

    @joint_value.setter
    def joint_value(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'joint_value' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'joint_value' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._joint_value = value

    @builtins.property
    def offset(self):
        """Message field 'offset'."""
        return self._offset

    @offset.setter
    def offset(self, value):
        if __debug__:
            from geometry_msgs.msg import Vector3
            assert \
                isinstance(value, Vector3), \
                "The 'offset' field must be a sub message of type 'Vector3'"
        self._offset = value

    @builtins.property
    def object_id(self):
        """Message field 'object_id'."""
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'object_id' field must be of type 'str'"
        self._object_id = value

    @builtins.property
    def touch_links(self):
        """Message field 'touch_links'."""
        return self._touch_links

    @touch_links.setter
    def touch_links(self, value):
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
                "The 'touch_links' field must be a set or sequence and each value of type 'str'"
        self._touch_links = value

    @builtins.property
    def allow(self):
        """Message field 'allow'."""
        return self._allow

    @allow.setter
    def allow(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'allow' field must be of type 'bool'"
        self._allow = value
