VEC_TYPES = {
    "Vec2f": {
        "field_c_type": "f32",
        "field_lua_type": "number",
        "fields_mapping": {
            "x": "[0]",
            "y": "[1]",
        },
    },
    "Vec3f": {
        "field_c_type": "f32",
        "field_lua_type": "number",
        "fields_mapping": {
            "x": "[0]",
            "y": "[1]",
            "z": "[2]",
        },
    },
    "Vec4f": {
        "field_c_type": "f32",
        "field_lua_type": "number",
        "fields_mapping": {
            "x": "[0]",
            "y": "[1]",
            "z": "[2]",
            "w": "[3]",
        },
    },
    "Vec3s": {
        "field_c_type": "s16",
        "field_lua_type": "integer",
        "fields_mapping": {
            "x": "[0]",
            "y": "[1]",
            "z": "[2]",
        },
    },
    "Vec4s": {
        "field_c_type": "s16",
        "field_lua_type": "integer",
        "fields_mapping": {
            "x": "[0]",
            "y": "[1]",
            "z": "[2]",
            "w": "[3]",
        },
    },
    "Mat4": {
        "field_c_type": "f32",
        "field_lua_type": "number",
        "fields_mapping": {
            "m00": "[0][0]",
            "m01": "[0][1]",
            "m02": "[0][2]",
            "m03": "[0][3]",
            "m10": "[1][0]",
            "m11": "[1][1]",
            "m12": "[1][2]",
            "m13": "[1][3]",
            "m20": "[2][0]",
            "m21": "[2][1]",
            "m22": "[2][2]",
            "m23": "[2][3]",
            "m30": "[3][0]",
            "m31": "[3][1]",
            "m32": "[3][2]",
            "m33": "[3][3]",
            "a": "[0][0]",
            "b": "[0][1]",
            "c": "[0][2]",
            "d": "[0][3]",
            "e": "[1][0]",
            "f": "[1][1]",
            "g": "[1][2]",
            "h": "[1][3]",
            "i": "[2][0]",
            "j": "[2][1]",
            "k": "[2][2]",
            "l": "[2][3]",
            "m": "[3][0]",
            "n": "[3][1]",
            "o": "[3][2]",
            "p": "[3][3]",
        },
    },
    "Color": {
        "field_c_type": "u8",
        "field_lua_type": "integer",
        "fields_mapping": {
            "r": "[0]",
            "g": "[1]",
            "b": "[2]",
        },
    },
}
