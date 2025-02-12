import os
import re
import sys
from extract_structs import *
from extract_object_fields import *
from common import *
from vec_types import *

in_files = [
    "include/types.h",
    "src/game/area.h",
    "src/game/camera.h",
    "src/game/characters.h",
    "src/engine/surface_collision.h",
    "src/pc/network/network_player.h",
    "src/pc/djui/djui_hud_utils.h",
    "src/pc/djui/djui_theme.h",
    "src/game/object_helpers.h",
    "src/game/mario_step.h",
    "src/pc/lua/utils/smlua_anim_utils.h",
    "src/pc/lua/utils/smlua_misc_utils.h",
    "src/pc/lua/utils/smlua_camera_utils.h",
    "src/pc/lua/utils/smlua_collision_utils.h",
    "src/pc/lua/utils/smlua_level_utils.h",
    "src/game/spawn_sound.h",
    "src/pc/network/network.h",
    "src/game/hardcoded.h",
    "src/pc/mods/mod.h",
    "src/pc/lua/utils/smlua_audio_utils.h",
    "src/game/paintings.h",
    "src/pc/djui/djui_types.h",
    "src/game/first_person_cam.h",
    "src/game/player_palette.h",
    "src/engine/graph_node.h"
]

out_filename_c = 'src/pc/lua/smlua_cobject_autogen.c'
out_filename_h = 'src/pc/lua/smlua_cobject_autogen.h'
out_filename_docs = 'docs/lua/structs.md'
out_filename_defs = 'autogen/lua_definitions/structs.lua'

c_template = """/* THIS FILE IS AUTOGENERATED */
/* SHOULD NOT BE MANUALLY CHANGED */
$[INCLUDES]
#include "include/object_fields.h"

$[BODY]
struct LuaObjectField* smlua_get_object_field_autogen(u16 lot, const char* key) {
    struct LuaObjectTable* ot = &sLuaObjectAutogenTable[lot - LOT_AUTOGEN_MIN - 1];
    return smlua_get_object_field_from_ot(ot, key);
}

"""

h_template = """/* THIS FILE IS AUTOGENERATED */
/* SHOULD NOT BE MANUALLY CHANGED */
#ifndef SMLUA_COBJECT_AUTOGEN_H
#define SMLUA_COBJECT_AUTOGEN_H

$[BODY]
struct LuaObjectField* smlua_get_object_field_autogen(u16 lot, const char* key);

#endif
"""

override_field_names = {
}

override_field_types = {
    "Surface": { "normal": "Vec3f" },
    "Object": { "oAnimations": "ObjectAnimPointer*" },
}

override_field_mutable = {
    "NetworkPlayer": [
        "overrideModelIndex",
        "overridePalette",
        "overridePaletteIndex"
    ],
    "Animation": [
        "values",
        "index",
    ],
}

override_field_invisible = {
    "Mod": [ "files", "showedScriptWarning" ],
    "MarioState": [ "visibleToEnemies" ],
    "NetworkPlayer": [ "gag", "moderator", "discordId" ],
    "GraphNode": [ "_guard1", "_guard2" ],
    "FnGraphNode": [ "luaTokenIndex" ],
    "Object": [ "firstSurface" ],
    "ModAudio": [ "sound", "decoder", "buffer", "bufferSize", "sampleCopiesTail" ],
}

override_field_deprecated = {
    "NetworkPlayer": [ "paletteIndex", "overridePaletteIndex", "overridePaletteIndexLp" ]
}

override_field_immutable = {
    "MarioState": [ "playerIndex", "controller", "marioObj", "marioBodyState", "statusForCamera", "area", "dialogId" ],
    "MarioAnimation": [ "animDmaTable" ],
    "ObjectNode": [ "next", "prev" ],
    "Character": [ "*" ],
    "NetworkPlayer": [ "*" ],
    "TextureInfo": [ "*" ],
    "Object": ["oSyncID", "coopFlags", "oChainChompSegments", "oWigglerSegments", "oHauntedChairUnk100", "oTTCTreadmillBigSurface", "oTTCTreadmillSmallSurface", "bhvStackIndex", "respawnInfoType", "numSurfaces" ],
    "GlobalObjectAnimations": [ "*"],
    "SpawnParticlesInfo": [ "model" ],
    "MarioBodyState": [ "updateTorsoTime" ],
    "Area": [ "localAreaTimer", "nextSyncID", "unk04", "objectSpawnInfos", "paintingWarpNodes", "warpNodes" ],
    "Mod": [ "*" ],
    "ModFile": [ "*" ],
    "Painting": [ "id", "imageCount", "textureType", "textureWidth", "textureHeight" ],
    "SpawnInfo": [ "syncID", "next", "unk18" ],
    "CustomLevelInfo": [ "next" ],
    "GraphNode": [ "children", "next", "parent", "prev", "type" ],
    "GraphNodeBackground": [ "prevCameraTimestamp", "unused" ],
    "GraphNodeCamera": [ "matrixPtrPrev", "prevTimestamp" ],
    "GraphNodeHeldObject": [ "prevShadowPosTimestamp" ],
    "GraphNodeObject": [ "angle", "animInfo", "cameraToObject", "node", "pos", "prevAngle", "prevPos", "prevScale", "prevScaleTimestamp", "prevShadowPos", "prevShadowPosTimestamp", "prevThrowMatrix", "prevThrowMatrixTimestamp", "prevTimestamp", "scale", "shadowPos", "sharedChild", "skipInterpolationTimestamp", "throwMatrixPrev", "unk4C", ],
    "GraphNodeObjectParent": [ "sharedChild" ],
    "GraphNodePerspective": [ "unused" ],
    "GraphNodeSwitchCase": [ "fnNode", "numCases", "unused" ],
    "ObjectWarpNode": [ "next "],
    "Animation": [ "length" ],
    "AnimationTable": [ "count" ],
    "Controller": [ "controllerData", "statusData" ],
    "FirstPersonCamera": [ "enabled" ],
    "ModAudio": [ "isStream", "loaded" ],
}

override_field_version_excludes = {
    "oCameraLakituUnk104": "VERSION_JP",
    "oCoinUnk1B0": "VERSION_JP"
}

override_allowed_structs = {
    "src/pc/network/network.h": [ "ServerSettings", "NametagsSettings" ],
    "src/pc/djui/djui_types.h": [ "DjuiColor" ],
    "src/game/player_palette.h": [ "PlayerPalette" ]
}

sLuaManuallyDefinedStructs = [{
    'path': 'n/a',
    'structs': [
        *['struct %s { %s }' % (
            type_name,
            ' '.join([
                '%s %s;' % (vec_type['field_c_type'], lua_field)
                for lua_field in vec_type['fields_mapping'].keys()
            ])
        ) for type_name, vec_type in VEC_TYPES.items()]
    ]
}]

total_structs = 0
total_fields = 0

############################################################################

def promote_block(before_block, after_block):
    inside = 1
    idx = -1

    for character in after_block:
        idx += 1
        if character == '{':
            inside += 1
        elif character == '}':
            inside -= 1
            if inside <= 0:
                break
    if inside == 0 and idx > -1 and after_block[idx+1] == ';':
        return before_block + after_block[:idx] + after_block[idx+2:]

    return None

def strip_anonymous_blocks(body):
    while 'union {' in body:
        before_union = body.split('union {', 1)[0]
        after_union = body.split('union {', 1)[-1]
        promoted = promote_block(before_union, after_union)
        if promoted == None:
            break
        body = promoted

    while 'struct {' in body:
        before_union = body.split('struct {', 1)[0]
        after_union = body.split('struct {', 1)[-1]
        promoted = promote_block(before_union, after_union)
        if promoted == None:
            break
        body = promoted

    return body

def strip_internal_blocks(body):
    # strip internal structs/enums/etc
    tmp = body
    body = ''
    inside = 0
    stripped = ''
    for character in tmp:
        if character == '{':
            body += '{ ... }'
            inside += 1

        if inside == 0:
            body += character
        else:
            stripped += character

        if character == '}':
            inside -= 1

    return body

def identifier_to_caps(identifier):
    caps = ''
    was_cap = True
    for c in identifier:
        if c >= 'A' and c <= 'Z':
            if not was_cap:
                caps += '_'
            was_cap = True
        else:
            was_cap = False
        caps += c.upper()
    return caps

def table_to_string(table):
    count = 0
    columns = 0
    column_width = []
    for c in table[0]:
        column_width.append(0)
        columns += 1

    for row in table:
        for i in range(columns):
            if '#' in row[i]:
                continue
            if len(row[i]) > column_width[i]:
                column_width[i] = len(row[i])

    s = ''
    for row in table:
        line = ''
        for i in range(columns):
            line += row[i].ljust(column_width[i])
        if '???' in line:
            line = '//' + line[2:] + ' <--- UNIMPLEMENTED'
        else:
            count += 1
        s += line + '\n'
    return s, count

############################################################################

def parse_struct(struct_str, sortFields = True):
    struct = {}
    match = re.match(r"struct\s*(\w+)?\s*{(.*?)}\s*(\w+)?\s*", struct_str.replace("typedef ", ""), re.DOTALL)
    struct_name, body, trailing_name = match.groups()
    identifier = struct_name if struct_name else trailing_name
    struct['identifier'] = identifier

    body = struct_str.split('{', 1)[1].rsplit('}', 1)[0]
    body = strip_anonymous_blocks(body)
    body = strip_internal_blocks(body)

    struct['fields'] = []
    field_strs = body.split(';')
    for field_str in field_strs:
        if len(field_str.strip()) == 0:
            continue

        if '*' in field_str:
            field_type, field_id = field_str.strip().rsplit('*', 1)
            field_type = field_type.strip() + '*'
        else:
            split_parts = re.split(r'\s+', field_str.strip())
            field_type = ' '.join(split_parts[:-1])
            field_id = split_parts[-1]

        if '[' in field_id:
            array_str = '[' + field_id.split('[', 1)[1]
            field_id = field_id.split('[', 1)[0]
            if array_str != '[1]':
                field_type += ' ' + array_str

        field = {}
        field['type'] = field_type.strip()
        field['identifier'] = field_id.strip()
        field['field_str'] = field_str

        struct['fields'].append(field)

    if identifier == 'Object':
        struct['fields'] += extract_object_fields()

    if sortFields:
        struct['fields'] = sorted(struct['fields'], key=lambda d: d['identifier'])

    return struct

def parse_structs(extracted, sortFields = True):
    structs = []
    for e in extracted:
        for struct in e['structs']:
            parsed = parse_struct(struct, sortFields)
            if e['path'] in override_allowed_structs:
                if parsed['identifier'] not in override_allowed_structs[e['path']]:
                    continue
            structs.append(parsed)
    return structs

############################################################################

fuzz_from = ""
fuzz_to = ""
fuzz_structs = ""
fuzz_structs_calls = ""
fuzz_template_str = None

def output_fuzz_struct_calls(struct):
    sid = struct['identifier']
    global fuzz_template_str
    if fuzz_template_str == None:
        with open(fuzz_from) as f:
            fuzz_template_str = f.read()

    global fuzz_structs_calls

    rnd_call = 'rnd_' + sid + '()'
    if rnd_call in fuzz_template_str:
        fuzz_structs_calls += '        function() Fuzz' + sid + '(rnd_' + sid + '()) end,\n'
    else:
        fuzz_structs_calls += '        -- function() Fuzz' + sid + '(rnd_' + sid + '()) end,\n'

def output_fuzz_struct(struct):
    output_fuzz_struct_calls(struct)
    sid = struct['identifier']

    s_out = 'function Fuzz' + sid + "(struct)\n"

    s_out += '    local funcs = {\n'
    for field in struct['fields']:
        fid, ftype, fimmutable, lvt, lot, size = get_struct_field_info(struct, field)
        if fimmutable == 'true':
            continue
        if sid in override_field_invisible:
            if fid in override_field_invisible[sid]:
                continue

        if '(' in fid or '[' in fid or ']' in fid:
            continue

        ptype, plink = translate_type_to_lua(ftype)
        rnd_line = translate_type_to_rnd(ptype)

        s_out += '        function() '

        if lvt == 'LVT_COBJECT':
            s_out += 'Fuzz' + ftype.replace('struct ', '') + '(struct.' + fid + ')'
        elif lvt == 'LVT_COBJECT_P':
            s_out += 'struct.' + fid + ' = ' + rnd_line + ''
        else:
            s_out += 'struct.' + fid + ' = ' + rnd_line + ''

        s_out += ' end,\n'
    s_out += '    }\n'

    s_out += """
    for i = #funcs, 2, -1 do
      local j = math.random(i)
      funcs[i], funcs[j] = funcs[j], funcs[i]
    end

    for k,v in pairs(funcs) do
        v()
    end
"""

    s_out += 'end\n\n'

    global fuzz_structs
    fuzz_structs += s_out

def output_fuzz_file():
    global fuzz_structs
    global fuzz_structs_calls
    with open(fuzz_from) as f:
        file_str = f.read()
    with open(fuzz_to, 'w') as f:
        f.write(file_str.replace('-- $[STRUCTS]', fuzz_structs).replace('-- $[FUZZ-STRUCTS]', fuzz_structs_calls))

############################################################################

def build_vec_types():
    s = gen_comment_header("vec types")

    for type_name, vec_type in VEC_TYPES.items():
        optional_fields = vec_type.get('optional_fields_mapping', {})
        s += '#define LUA_%s_FIELD_COUNT %d\n' % (type_name.upper(), len(vec_type['fields_mapping']) + len(optional_fields))
        s += 'static struct LuaObjectField s%sFields[LUA_%s_FIELD_COUNT] = {\n' % (type_name, type_name.upper())

        field_c_type = vec_type['field_c_type']
        combined_fields = [
            (index, field_name)
            for mapping in [vec_type['fields_mapping'], optional_fields]
            for index, field_name in enumerate(mapping.keys())
        ]
        sorted_fields_with_order = sorted(combined_fields, key=lambda x: x[1]) # sort alphabetically
        for original_index, lua_field in sorted_fields_with_order:
            s += '    { "%s", LVT_%s, sizeof(%s) * %d, false, LOT_NONE, 1, sizeof(%s) },\n' % (lua_field, field_c_type.upper(), field_c_type, original_index, field_c_type)

        s += '};\n\n'

    s += 'struct LuaObjectTable sLuaObjectTable[LOT_MAX] = {\n'
    s += '    [LOT_NONE] = { LOT_NONE, NULL, 0 },\n'

    for type_name in VEC_TYPES.keys():
        s += '    [LOT_%s] = { LOT_%s, s%sFields, LUA_%s_FIELD_COUNT },\n' % (type_name.upper(), type_name.upper(), type_name, type_name.upper())

    s += '    [LOT_POINTER] = { LOT_POINTER, NULL, 0 },\n'
    s += '};\n\n'

    return s

############################################################################

sLuaObjectTable = []
sLotAutoGenList = []

def get_struct_field_info(struct, field):
    sid = struct['identifier']
    fid = field['identifier']
    ftype = field['type']
    size = 1

    if sid in override_field_names and fid in override_field_names[sid]:
        fid = override_field_names[sid][fid]

    if sid in override_field_types and fid in override_field_types[sid]:
        ftype = override_field_types[sid][fid]

    lvt = translate_type_to_lvt(ftype, allowArrays=True)
    lot = translate_type_to_lot(ftype, allowArrays=True)
    fimmutable = str(lvt == 'LVT_COBJECT' or 'const ' in ftype).lower()
    if lvt.startswith('LVT_') and lvt.endswith('_P') and 'OBJECT' not in lvt and 'COLLISION' not in lvt and 'TRAJECTORY' not in lvt:
        fimmutable = 'true'

    if sid in override_field_immutable:
        if fid in override_field_immutable[sid] or '*' in override_field_immutable[sid]:
            fimmutable = 'true'

    if sid in override_field_mutable:
        if fid in override_field_mutable[sid] or '*' in override_field_mutable[sid]:
            fimmutable = 'false'

    if not ('char' in ftype and '[' in ftype):
        array_match = re.search(r'\[([^\]]+)\]', ftype)
        if array_match:
            array_size = array_match.group(1).strip()
            if array_size.isdigit():
                size = int(array_size)
            elif array_size.startswith("0x") and all(c in "0123456789abcdef" for c in array_size[2:]):
                size = int(array_size, 16)
            else:
                lvt, lot = 'LVT_???', "LOT_???" # array size not provided, so not supported

    return fid, ftype, fimmutable, lvt, lot, size

def build_struct(struct):
    # debug print out lua fuzz functions
    if len(sys.argv) >= 2 and sys.argv[1] == 'fuzz':
        output_fuzz_struct(struct)

    sid = struct['identifier']

    # build up table and track column width
    field_table = []
    for field in struct['fields']:
        fid, ftype, fimmutable, lvt, lot, size = get_struct_field_info(struct, field)

        if re.search(r'\[([^\]]+)\]', ftype):
            ftype = re.sub(r'\[[^\]]*\]', '', ftype).strip()

        if sid in override_field_invisible:
            if fid in override_field_invisible[sid]:
                continue

        version = None

        row = []

        startStr = ''
        endStr = ' },'
        if fid in override_field_version_excludes:
            startStr += '#ifndef ' + override_field_version_excludes[fid] + '\n'
            endStr += '\n#endif'
        startStr += '    { '
        row.append(startStr                                                 )
        row.append('"%s", '                    % fid                        )
        row.append('%s, '                      % lvt                        )
        row.append('offsetof(struct %s, %s), ' % (sid, field['identifier']) )
        row.append('%s, '                      % fimmutable                 )
        row.append('%s, '                      % lot                        )
        row.append('%s, '                      % size                       )
        row.append('sizeof(%s)'                % ftype                      )
        row.append(endStr                                                   )
        field_table.append(row)

    field_table_str, field_count = table_to_string(field_table)
    field_count_define = 'LUA_%s_FIELD_COUNT' % identifier_to_caps(sid)
    struct_lot = 'LOT_%s' % sid.upper()

    s  = "#define %s $[STRUCTFIELDCOUNT]\n" % field_count_define
    s += "static struct LuaObjectField s%sFields[%s] = {\n" % (sid, field_count_define)
    s += field_table_str
    s += '};\n'

    s = s.replace('$[STRUCTFIELDCOUNT]', str(field_count))

    global sLuaObjectTable
    struct_row = []
    struct_row.append('    { '                           )
    struct_row.append('%s, '        % struct_lot         )
    struct_row.append('s%sFields, ' % sid                )
    struct_row.append('%s '         % field_count_define )
    struct_row.append('},'                               )
    sLuaObjectTable.append(struct_row)

    global sLotAutoGenList
    sLotAutoGenList.append(struct_lot)

    return s

def build_structs(structs):
    global sLuaObjectTable
    sLuaObjectTable = []

    global sLotAutoGenList
    sLotAutoGenList = []

    s = ''
    for struct in structs:
        if struct['identifier'] in exclude_structs:
            continue
        s += build_struct(struct) + '\n'
    return s

def build_body(parsed):
    built = build_vec_types()
    built += gen_comment_header("autogen types")
    built += build_structs(parsed)
    obj_table_row_built, obj_table_count = table_to_string(sLuaObjectTable)

    obj_table_built = 'struct LuaObjectTable sLuaObjectAutogenTable[LOT_AUTOGEN_MAX - LOT_AUTOGEN_MIN] = {\n'
    obj_table_built += obj_table_row_built
    obj_table_built += '};\n'

    return built + obj_table_built

def build_lot_enum():
    s = ''

    s += 'enum LuaObjectType {\n'
    s += '    LOT_NONE = 0,\n'

    for type_name in VEC_TYPES.keys():
        s += '    LOT_%s,\n' % (type_name.upper())

    s += '    LOT_POINTER,\n'
    s += '    LOT_MAX,\n'
    s += '};\n\n'

    s += 'enum LuaObjectAutogenType {\n'
    s += '    LOT_AUTOGEN_MIN = 1000,\n'

    global sLotAutoGenList
    for lot in sLotAutoGenList:
        s += '    ' + lot + ',\n'

    s += '    LOT_AUTOGEN_MAX,\n'
    s += '};\n'
    return s

def build_includes():
    s = '#include "smlua.h"\n'
    for in_file in in_files:
        s += '#include "%s"\n' % in_file
    return s


############################################################################

def doc_struct_index(structs):
    s = '# Supported Structs\n'
    for struct in structs:
        sid = struct['identifier']
        s += '- [%s](#%s)\n' % (sid, sid)
        global total_structs
        total_structs += 1
    s += '\n<br />\n\n'
    return s

def doc_struct_field(struct, field):
    fid, ftype, fimmutable, lvt, lot, size = get_struct_field_info(struct, field)

    sid = struct['identifier']
    if sid in override_field_invisible:
        if fid in override_field_invisible[sid]:
            return ''

    if sid in override_field_deprecated:
        if fid in override_field_deprecated[sid]:
            return ''

    if '???' in lvt or '???' in lot:
        return ''

    ftype, flink = translate_type_to_lua(ftype)

    restrictions = ('', 'read-only')[fimmutable == 'true']

    global total_fields
    total_fields += 1

    if flink:
        return '| %s | [%s](%s) | %s |\n'  % (fid, ftype, flink, restrictions)

    return '| %s | %s | %s |\n'  % (fid, ftype, restrictions)


def doc_struct_object_fields(struct):
    fields = extract_object_fields()

    s = '\n### Object-Independent Data Fields\n'
    s += "| Field | Type | Access |\n"
    s += "| ----- | ---- | ------ |\n"
    for field in fields:
        if field['identifier'] == 'oPathedStartWaypoint':
            s += '\n### Object-Dependent Data Fields\n'
            s += "| Field | Type | Access |\n"
            s += "| ----- | ---- | ------ |\n"

        s += doc_struct_field(struct, field)

    return s


def doc_struct(struct):
    sid = struct['identifier']
    s = '## [%s](#%s)\n\n' % (sid, sid)
    s += "| Field | Type | Access |\n"
    s += "| ----- | ---- | ------ |\n"


    # build doc table
    field_table = []
    for field in struct['fields']:
        if 'object_field' in field and field['object_field'] == True:
            continue
        s += doc_struct_field(struct, field)

    if sid == 'Object':
        s += doc_struct_object_fields(struct)

    s += '\n[:arrow_up_small:](#)\n\n<br />\n'

    return s

def doc_structs(structs):
    structs.extend(parse_structs(sLuaManuallyDefinedStructs, False)) # Don't sort fields for vec types in the documentation
    structs = sorted(structs, key=lambda d: d['identifier'])

    s = '## [:rewind: Lua Reference](lua.md)\n\n'
    s += doc_struct_index(structs)
    for struct in structs:
        if struct['identifier'] in exclude_structs:
            continue
        s += doc_struct(struct) + '\n'

    with open(get_path(out_filename_docs), 'w', newline='\n') as out:
        out.write(s)

############################################################################

def_pointers = []

def def_struct(struct):
    sid = struct['identifier']

    stype = translate_to_def(sid)
    if stype.startswith('Pointer_') and stype not in def_pointers:
        def_pointers.append(stype)

    s = '\n--- @class %s\n' % stype

    for field in struct['fields']:
        fid, ftype, fimmutable, lvt, lot, size = get_struct_field_info(struct, field)

        if sid in override_field_invisible:
            if fid in override_field_invisible[sid]:
                continue

        if '???' in lvt or '???' in lot:
            continue

        ftype, flink = translate_type_to_lua(ftype)

        ftype = translate_to_def(ftype)
        if ftype.startswith('Pointer_') and ftype not in def_pointers:
            def_pointers.append(ftype)

        s += '--- @field public %s %s\n' % (fid, ftype)

    return s

def def_structs(structs):
    s = '-- AUTOGENERATED FOR CODE EDITORS --\n'

    for struct in structs:
        if struct['identifier'] in exclude_structs:
            continue
        s += def_struct(struct)

    s += '\n'
    for def_pointer in def_pointers:
        s += '--- @class %s\n' % def_pointer

    with open(get_path(out_filename_defs), 'w', newline='\n') as out:
        out.write(s)

############################################################################

def build_files():
    extracted = []
    for in_file in in_files:
        path = get_path(in_file)
        extracted.append({
            'path': in_file,
            'structs': extract_structs(path)
        })

    parsed = parse_structs(extracted)
    parsed = sorted(parsed, key=lambda d: d['identifier'])

    built_body = build_body(parsed)
    built_enum = build_lot_enum()
    built_include = build_includes()

    out_c_filename = get_path(out_filename_c)
    with open(out_c_filename, 'w', newline='\n') as out:
        out.write(c_template.replace("$[BODY]", built_body).replace('$[INCLUDES]', built_include))

    out_h_filename = get_path(out_filename_h)
    with open(out_h_filename, 'w', newline='\n') as out:
        out.write(h_template.replace("$[BODY]", built_enum))

    doc_structs(parsed)
    def_structs(parsed)

    if len(sys.argv) >= 2 and sys.argv[1] == 'fuzz':
        output_fuzz_file()

    global total_structs
    global total_fields

    print("Total structs: " + str(total_structs))
    print("Total fields: " + str(total_fields))

############################################################################

if __name__ == '__main__':
   build_files()
