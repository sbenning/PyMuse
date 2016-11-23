import pytest
from struct import pack
from Utils.Osc import *

class TestClassOscMsgRaise:
    def test_raise_if_frame_is_None(self):
        frame = None
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'Invalid frame for' in str(info.value)

    def test_raise_if_frame_type_is_invalid(self):
        frame = 42
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'Invalid frame for' in str(info.value)

    def test_raise_if_frame_type_is_invalid_suite(self):
        frame = str(pack('>4s4si', b'ttt\0', b',i\0\0', 42))
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'Invalid frame for' in str(info.value)

    def test_raise_if_frame_is_empty(self):
        frame = b''
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'Invalid frame for' in str(info.value)

    def test_raise_if_frame_path_is_empty(self):
        frame = pack('>4s4s', b'\0\0\0\0', b',i\0\0')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame path' in str(info.value)

    def test_raise_if_frame_path_is_not_terminated(self):
        frame = pack('>4s', b'test')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame path' in str(info.value)

    def test_raise_if_frame_typetag_is_empty_0(self):
        frame = pack('>4s', b'ttt\0')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_is_empty_1(self):
        frame = pack('>4s4s', b'ttt\0', b'\0\0\0\0')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_is_not_terminated(self):
        frame = pack('>4s4s', b'ttt\0', b',iii')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_terminate_the_frame(self):
        frame = pack('>4s4s', b'ttt\0', b',ii\0')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_is_not_well_formated_0(self):
        frame = pack('>4s4si', b'ttt\0', b'i\0\0\0', 42)
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_is_not_well_formated_1(self):
        frame = pack('>4s4si', b'ttt\0', b',i,\0', 42)
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_is_not_well_formated_2(self):
        frame = pack('>4s4si', b'ttt\0', b',,\0\0', 42)
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_is_not_well_formated_3(self):
        frame = pack('>4s4si', b'ttt\0', b'i,\0\0', 42)
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_mismatch_the_handled_ones_0(self):
        frame = pack('>4s4si', b'ttt\0', b',j\0\0', 42)
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_mismatch_the_handled_ones_1(self):
        frame = pack('>4s4si', b'ttt\0', b',ji\0', 42)
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_frame_typetag_mismatch_the_handled_ones_2(self):
        frame = pack('>4s4si', b'ttt\0', b',ij\0', 42)
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'frame typetag' in str(info.value)

    def test_raise_if_str_arg_is_empty(self):
        frame = pack('>4s4si', b'ttt\0', b',is\0', 42)
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'string syntax' in str(info.value)

    def test_raise_if_str_arg_is_not_terminated(self):
        frame = pack('>4s4s4s', b'ttt\0', b',s\0\0', b'tttt')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'string syntax' in str(info.value)

    def test_raise_if_int_arg_is_empty(self):
        frame = pack('>4s4s4s', b'ttt\0', b',si\0', b'abc\0')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'int syntax' in str(info.value)

    def test_raise_if_float_arg_is_empty(self):
        frame = pack('>4s4s4s', b'ttt\0', b',sf\0', b'abc\0')
        with pytest.raises(OscError) as info:
            osc = OscMsg(frame)
        assert 'float syntax' in str(info.value)


class TestClassOscMsg:
    def test_type_path(self):
        frame = pack('>4s4si', b'ttt\0', b',i\0\0', 42)
        osc = OscMsg(frame)
        assert type(osc.path) == str

    def test_equal_path(self):
        frame = pack('>4s4si', b'ttt\0', b',i\0\0', 42)
        osc = OscMsg(frame)
        assert osc.path == 'ttt'

    def test_type_typetag(self):
        frame = pack('>4s4si4s', b'ttt\0', b',is\0', 42, b'abc\0')
        osc = OscMsg(frame)
        assert type(osc.typetag) == str

    def test_equal_typetag(self):
        frame = pack('>4s4si4s', b'ttt\0', b',is\0', 42, b'abc\0')
        osc = OscMsg(frame)
        assert osc.typetag == 'is'

    def test_type_str_arg(self):
        frame = pack('>4s4s4s', b'ttt\0', b',s\0\0', b'abc\0')
        osc = OscMsg(frame)
        assert type(osc.args[0]) == str

    def test_equal_str_arg(self):
        frame = pack('>4s4s4s', b'ttt\0', b',s\0\0', b'abc\0')
        osc = OscMsg(frame)
        assert osc.args[0] == 'abc'

    def test_type_int_arg(self):
        frame = pack('>4s4si', b'ttt\0', b',i\0\0', 42)
        osc = OscMsg(frame)
        assert type(osc.args[0]) == int

    def test_equal_int_arg(self):
        frame = pack('>4s4si', b'ttt\0', b',i\0\0', 42)
        osc = OscMsg(frame)
        assert osc.args[0] == 42

    def test_type_float_arg(self):
        frame = pack('>4s4sf', b'ttt\0', b',f\0\0', 42.0)
        osc = OscMsg(frame)
        assert type(osc.args[0]) == float

    def test_equal_float_arg(self):
        frame = pack('>4s4sf', b'ttt\0', b',f\0\0', 42.0)
        osc = OscMsg(frame)
        assert osc.args[0] == 42.0

    def test_type_strint_arg(self):
        frame = pack('>4s4s4si', b'ttt\0', b',si\0', b'abc\0', 42)
        osc = OscMsg(frame)
        assert type(osc.args[0]) == str and type(osc.args[1]) == int

    def test_equal_strint_arg(self):
        frame = pack('>4s4s4si', b'ttt\0', b',si\0', b'abc\0', 42)
        osc = OscMsg(frame)
        assert osc.args[0] == 'abc' and osc.args[1] == 42

    def test_type_intstr_arg(self):
        frame = pack('>4s4si4s', b'ttt\0', b',is\0', 42, b'abc\0')
        osc = OscMsg(frame)
        assert type(osc.args[0]) == int and type(osc.args[1]) == str

    def test_equal_intstr_arg(self):
        frame = pack('>4s4si4s', b'ttt\0', b',is\0', 42, b'abc\0')
        osc = OscMsg(frame)
        assert osc.args[0] == 42 and osc.args[1] == 'abc'
    
    def test_type_strintfloat_arg(self):
        frame = pack('>4s8s4sif', b'ttt\0', b',sif\0\0\0\0', b'abc\0', 42, 42.0)
        osc = OscMsg(frame)
        assert type(osc.args[0]) == str and type(osc.args[1]) == int and type(osc.args[2]) == float

    def test_equal_strintfloat_arg(self):
        frame = pack('>4s8s4sif', b'ttt\0', b',sif\0\0\0\0', b'abc\0', 42, 42.0)
        osc = OscMsg(frame)
        assert osc.args[0] == 'abc'
        assert osc.args[1] == 42
        assert osc.args[2] == 42.0

    def test_type_bigframe(self):
        INT_MIN = ~(1 << 31) + 1
        INT_MAX = (1 << 31) - 1
        FLOAT_MIN = float((1 << 31) - 1)
        FLOAT_MAX = float(~(1 << 31) + 1)
        frame = pack('>20s28siiifff8si8si8si12sf8sf12sf8s4s4s4s4s4s8s4s',
                b'/test/valid/path\0\0\0\0', b',iiifffsisisisfsfsfssssssss\0\0\0',
                INT_MAX, 0, INT_MIN,
                FLOAT_MAX, 0.0, FLOAT_MIN,
                b'Max_Int\0', INT_MAX, b'Zero\0\0\0\0', 0, b'Min_Int\0', INT_MIN,
                b'Max_Float\0\0\0', FLOAT_MAX, b'Zero\0\0\0\0', 0.0, b'Min_Float\0\0\0', FLOAT_MIN,
                b'Empty\0\0\0', b'\0\0\0\0',
                b'Str\0', b'OK\0\0', b'Int\0', b'OK\0\0', b'Float\0\0\0', b'OK\0\0'
                )
        osc = OscMsg(frame)
        assert type(osc.path) == str
        assert type(osc.typetag) == str
        assert type(osc.args[0]) == int
        assert type(osc.args[1]) == int
        assert type(osc.args[2]) == int
        assert type(osc.args[3]) == float
        assert type(osc.args[4]) == float
        assert type(osc.args[5]) == float
        assert type(osc.args[6]) == str
        assert type(osc.args[7]) == int
        assert type(osc.args[8]) == str
        assert type(osc.args[9]) == int
        assert type(osc.args[10]) == str
        assert type(osc.args[11]) == int
        assert type(osc.args[12]) == str
        assert type(osc.args[13]) == float
        assert type(osc.args[14]) == str
        assert type(osc.args[15]) == float
        assert type(osc.args[16]) == str
        assert type(osc.args[17]) == float
        assert type(osc.args[18]) == str
        assert type(osc.args[19]) == str
        assert type(osc.args[20]) == str
        assert type(osc.args[21]) == str
        assert type(osc.args[22]) == str
        assert type(osc.args[23]) == str
        assert type(osc.args[24]) == str
        assert type(osc.args[25]) == str

    def test_equal_bigframe(self):
        INT_MIN = ~(1 << 31) + 1
        INT_MAX = (1 << 31) - 1
        FLOAT_MIN = float((1 << 31) - 1)
        FLOAT_MAX = float(~(1 << 31) + 1)
        frame = pack('>20s28siiifff8si8si8si12sf8sf12sf8s4s4s4s4s4s8s4s',
                b'/test/valid/path\0\0\0\0', b',iiifffsisisisfsfsfssssssss\0\0\0',
                INT_MAX, 0, INT_MIN,
                FLOAT_MAX, 0.0, FLOAT_MIN,
                b'Max_Int\0', INT_MAX, b'Zero\0\0\0\0', 0, b'Min_Int\0', INT_MIN,
                b'Max_Float\0\0\0', FLOAT_MAX, b'Zero\0\0\0\0', 0.0, b'Min_Float\0\0\0', FLOAT_MIN,
                b'Empty\0\0\0', b'\0\0\0\0',
                b'Str\0', b'OK\0\0', b'Int\0', b'OK\0\0', b'Float\0\0\0', b'OK\0\0'
                )
        osc = OscMsg(frame)
        assert osc.path == '/test/valid/path'
        assert osc.typetag == 'iiifffsisisisfsfsfssssssss'
        assert osc.args[0] == INT_MAX
        assert osc.args[1] == 0
        assert osc.args[2] == INT_MIN
        assert osc.args[3] == pytest.approx(FLOAT_MAX)
        assert osc.args[4] == 0.0
        assert osc.args[5] == pytest.approx(FLOAT_MIN)
        assert osc.args[6] == 'Max_Int'
        assert osc.args[7] == INT_MAX
        assert osc.args[8] == 'Zero'
        assert osc.args[9] == 0
        assert osc.args[10] == 'Min_Int'
        assert osc.args[11] == INT_MIN
        assert osc.args[12] == 'Max_Float'
        assert osc.args[13] == pytest.approx(FLOAT_MAX)
        assert osc.args[14] == 'Zero'
        assert osc.args[15] == 0.0
        assert osc.args[16] == 'Min_Float'
        assert osc.args[17] == pytest.approx(FLOAT_MIN)
        assert osc.args[18] == 'Empty'
        assert osc.args[19] == ''
        assert osc.args[20] == 'Str'
        assert osc.args[21] == 'OK'
        assert osc.args[22] == 'Int'
        assert osc.args[23] == 'OK'
        assert osc.args[24] == 'Float'
        assert osc.args[25] == 'OK'
